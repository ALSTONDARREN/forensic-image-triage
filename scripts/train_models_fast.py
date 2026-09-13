import os
import argparse
import time
import copy
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
import cv2
import numpy as np
from sklearn.metrics import precision_recall_fscore_support, matthews_corrcoef, confusion_matrix
import warnings
import warnings

# ==========================================
# 1. OPTIMIZED FORENSIC DATASET (In-Memory Caching)
# ==========================================
class ForensicDataset(Dataset):
    """
    Loads images from folder structures with optional in-memory caching
    for dramatically faster epoch iterations on CPU.
    """
    def __init__(self, root_dir, transform=None, cache_in_memory=True):
        self.root_dir = root_dir
        self.transform = transform
        self.image_paths = []
        self.labels = []
        self.cache = {}
        self.cache_in_memory = cache_in_memory
        
        self.classes = sorted(os.listdir(root_dir))
        self.class_to_idx = {cls_name: i for i, cls_name in enumerate(self.classes)}
        
        for cls_name in self.classes:
            cls_dir = os.path.join(root_dir, cls_name)
            if not os.path.isdir(cls_dir):
                continue
            for img_name in os.listdir(cls_dir):
                if img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    self.image_paths.append(os.path.join(cls_dir, img_name))
                    self.labels.append(self.class_to_idx[cls_name])
        
        # Pre-load all images into RAM to eliminate disk I/O bottleneck
        if self.cache_in_memory:
            print(f"  [Cache] Loading {len(self.image_paths)} images into memory...", flush=True)
            for i, path in enumerate(self.image_paths):
                try:
                    img = cv2.imread(path)
                    if img is not None:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (224, 224))
                        self.cache[i] = img
                    else:
                        self.cache[i] = np.zeros((224, 224, 3), dtype=np.uint8)
                except Exception:
                    # Fallback: create a blank image if file is corrupt
                    self.cache[i] = np.zeros((224, 224, 3), dtype=np.uint8)
            print(f"  [Cache] Done! All images cached in RAM.", flush=True)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        if self.cache_in_memory and idx in self.cache:
            image = self.cache[idx].copy()
        else:
            image = cv2.imread(self.image_paths[idx])
            if image is not None:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image, (224, 224))
            else:
                image = np.zeros((224, 224, 3), dtype=np.uint8)
        
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        return image, label

# ==========================================
# 2. MULTI-MODEL INITIALIZATION FACTORY
# ==========================================
def initialize_model(model_name, num_classes, feature_extract=True):
    """
    Initializes one of three models: ResNet-50, VGG-16, or MobileNetV3-Large
    with ImageNet weights, modifying classification head for target classes.
    """
    model = None
    
    if model_name == 'resnet50':
        print("[Info] Loading pre-trained ResNet-50...", flush=True)
        model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        if feature_extract:
            for param in model.parameters():
                param.requires_grad = False
        num_ftrs = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Linear(num_ftrs, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )
        
    elif model_name == 'vgg16':
        print("[Info] Loading pre-trained VGG-16...", flush=True)
        model = models.vgg16(weights=models.VGG16_Weights.DEFAULT)
        if feature_extract:
            for param in model.parameters():
                param.requires_grad = False
        num_ftrs = model.classifier[6].in_features
        model.classifier[6] = nn.Sequential(
            nn.Linear(num_ftrs, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )
        
    elif model_name == 'mobilenetv3':
        print("[Info] Loading pre-trained MobileNetV3-Large...", flush=True)
        model = models.mobilenet_v3_large(weights=models.MobileNet_V3_Large_Weights.DEFAULT)
        if feature_extract:
            for param in model.parameters():
                param.requires_grad = False
        num_ftrs = model.classifier[3].in_features
        model.classifier[3] = nn.Sequential(
            nn.Linear(num_ftrs, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )
        
    else:
        raise ValueError("Unknown model name. Choose from 'resnet50', 'vgg16', 'mobilenetv3'")
        
    return model

# ==========================================
# 3. TRAINING WITH EARLY STOPPING & PROGRESS
# ==========================================
def train_and_evaluate(model, dataloaders, criterion, optimizer, scheduler, device, num_epochs=10, patience=4):
    since = time.time()
    best_model_wts = copy.deepcopy(model.state_dict())
    best_mcc = -1.0  # Matthews Correlation Coefficient is critical for forensic imbalance
    epochs_no_improve = 0

    for epoch in range(num_epochs):
        epoch_start = time.time()
        print(f'Epoch {epoch + 1}/{num_epochs}', flush=True)
        print('-' * 10, flush=True)

        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            all_preds = []
            all_labels = []

            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad(set_to_none=True)  # Faster than zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
                    _, preds = torch.max(outputs, 1)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())

            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            epoch_acc = np.mean(np.array(all_preds) == np.array(all_labels))
            
            # Compute classification metrics (Precision, Recall, F1, MCC)
            precision, recall, f1, _ = precision_recall_fscore_support(
                all_labels, all_preds, average='weighted', zero_division=0
            )
            mcc = matthews_corrcoef(all_labels, all_preds)

            print(f'{phase.capitalize()} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f} Prec: {precision:.4f} Rec: {recall:.4f} F1: {f1:.4f} MCC: {mcc:.4f}', flush=True)

            # Prioritize saving model weights with best val MCC/Recall to minimize false negatives
            if phase == 'val':
                if mcc > best_mcc:
                    best_mcc = mcc
                    best_model_wts = copy.deepcopy(model.state_dict())
                    epochs_no_improve = 0
                else:
                    epochs_no_improve += 1
        
        # Step the learning rate scheduler
        if scheduler:
            scheduler.step()

        epoch_time = time.time() - epoch_start
        elapsed = time.time() - since
        print(f'  Epoch time: {epoch_time:.0f}s | Total elapsed: {elapsed // 60:.0f}m {elapsed % 60:.0f}s', flush=True)
        print(flush=True)

        # Early stopping: if no improvement for `patience` epochs, stop
        if epochs_no_improve >= patience:
            print(f'[Early Stop] No improvement for {patience} epochs. Stopping training.', flush=True)
            break

    time_elapsed = time.time() - since
    print(f'Training completed in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s', flush=True)
    print(f'Best Validation MCC: {best_mcc:.4f}', flush=True)

    # Load best model weights
    model.load_state_dict(best_model_wts)
    
    # Run a final evaluation to print confusion matrix
    model.eval()
    val_preds = []
    val_labels = []
    with torch.no_grad():
        for inputs, labels in dataloaders['val']:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            val_preds.extend(preds.cpu().numpy())
            val_labels.extend(labels.cpu().numpy())
            
    cm = confusion_matrix(val_labels, val_preds)
    print("\nConfusion Matrix on Validation Set:", flush=True)
    print(cm, flush=True)
    
    return model

# ==========================================
# 4. ORCHESTRATION PIPELINE
# ==========================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="MSc Thesis Multi-Model Training Pipeline (Optimized)")
    parser.add_argument('--model', type=str, default='resnet50', 
                        choices=['resnet50', 'vgg16', 'mobilenetv3'],
                        help="Select pre-trained CNN model to train")
    parser.add_argument('--data_dir', type=str, default='./dataset', help="Path to dataset directory")
    parser.add_argument('--epochs', type=str, default='10', help="Number of training epochs")
    parser.add_argument('--output_dir', type=str, default=None, help="Output directory for model")
    parser.add_argument('--fine_tune', action='store_true', help="Unfreeze all convolutional layers for fine-tuning")
    
    # Handle environment argument parser (or default strings if run inside interactive shells)
    args, unknown = parser.parse_known_args()

    # Configuration Parameters
    MODEL_NAME = args.model
    DATA_DIR = args.data_dir
    EPOCHS = int(args.epochs)
    FEATURE_EXTRACT = not args.fine_tune
    NUM_CLASSES = len([d for d in os.listdir(os.path.join(DATA_DIR, 'train')) if os.path.isdir(os.path.join(DATA_DIR, 'train', d))])
    
    # OPTIMIZATION: Larger batch size = fewer iterations per epoch
    BATCH_SIZE = 64
    
    # OPTIMIZATION: Number of data loading workers
    NUM_WORKERS = 0  # 0 = main process (avoids multiprocessing overhead on Windows)
    
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"==========================================", flush=True)
    print(f"Model Selection  : {MODEL_NAME}", flush=True)
    print(f"Target Device    : {device}", flush=True)
    print(f"Dataset Path     : {DATA_DIR}", flush=True)
    print(f"Training Epochs  : {EPOCHS}", flush=True)
    print(f"Batch Size       : {BATCH_SIZE}", flush=True)
    print(f"Fine Tuning Mode : {not FEATURE_EXTRACT}", flush=True)
    print(f"Optimizations    : In-memory cache, early stopping, LR scheduler", flush=True)
    print(f"==========================================\n", flush=True)

    # Verify dataset exists
    if not os.path.exists(DATA_DIR):
        print(f"[Error] Dataset directory '{DATA_DIR}' not found.", flush=True)
        exit(1)

    # Standard ImageNet Transforms (optimized, OpenCV for resizing)
    data_transforms = {
        'train': transforms.Compose([
            transforms.ToTensor(),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.1),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    # Initialize Dataset loaders with in-memory caching
    try:
        print("[Phase] Loading datasets into memory...", flush=True)
        image_datasets = {
            x: ForensicDataset(os.path.join(DATA_DIR, x), data_transforms[x], cache_in_memory=True)
            for x in ['train', 'val']
        }
        dataloaders = {
            x: DataLoader(
                image_datasets[x], 
                batch_size=BATCH_SIZE, 
                shuffle=(x == 'train'),
                num_workers=NUM_WORKERS,
                pin_memory=False,
            )
            for x in ['train', 'val']
        }
        print(f"[Info] Train: {len(image_datasets['train'])} images, Val: {len(image_datasets['val'])} images", flush=True)
    except Exception as e:
        print(f"[Error] Failed to initialize Datasets: {e}", flush=True)
        exit(1)

    # Initialize Model
    model = initialize_model(model_name=MODEL_NAME, num_classes=NUM_CLASSES, feature_extract=FEATURE_EXTRACT)
    model = model.to(device)

    # Compile training criteria and parameters
    criterion = nn.CrossEntropyLoss()
    params_to_update = model.parameters()
    if FEATURE_EXTRACT:
        params_to_update = []
        for name, param in model.named_parameters():
            if param.requires_grad:
                params_to_update.append(param)
    
    # OPTIMIZATION: Higher learning rate with scheduler for faster convergence            
    optimizer = optim.Adam(params_to_update, lr=0.001)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)

    # Execute training loop with early stopping (patience=4)
    print("\n[Phase] Starting training...\n", flush=True)
    trained_model = train_and_evaluate(
        model, dataloaders, criterion, optimizer, scheduler, 
        device, num_epochs=EPOCHS, patience=4
    )
    
    # Save the trained model weights
    output_dir = args.output_dir or f"./models_output/{MODEL_NAME}"
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, f"{MODEL_NAME}_forensic_model.pth")
    torch.save(trained_model.state_dict(), save_path)
    print(f"[Success] Model saved to {save_path}", flush=True)
