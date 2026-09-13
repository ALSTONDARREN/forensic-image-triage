import os
import time
import copy
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
import cv2
import numpy as np

# ==========================================
# 1. CUSTOM FORENSIC DATASET DEFINITION
# ==========================================
class ForensicImageDataset(Dataset):
    """
    Custom Dataset class for loading forensic image categories.
    Assumes a directory structure like:
        dataset_path/
            train/
                benign/
                contraband/
                forgery/
            val/
                benign/
                ...
    """
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_paths = []
        self.labels = []
        
        # Identify target classes
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

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = cv2.imread(img_path)
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
# 2. MODEL CONFIGURATION & INITIALIZATION
# ==========================================
def initialize_model(num_classes, feature_extract=True):
    """
    Initializes a ResNet-50 model with pre-trained ImageNet weights.
    Frees weights if feature extracting, and replaces the fully connected head.
    """
    # Load ResNet-50 with default weights (ImageNet)
    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    
    # Freeze lower convolutional layers if we are doing feature extraction
    if feature_extract:
        for param in model.parameters():
            param.requires_grad = False
            
    # Replace final fully connected layer (model.fc) with target forensic classes
    num_ftrs = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Linear(num_ftrs, 256),
        nn.ReLU(),
        nn.Dropout(0.4),
        nn.Linear(256, num_classes)
    )
    
    return model

# ==========================================
# 3. MODEL TRAINING & VALIDATION LOOP
# ==========================================
def train_model(model, dataloaders, criterion, optimizer, device, num_epochs=15):
    since = time.time()
    
    val_acc_history = []
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(num_epochs):
        print(f'Epoch {epoch + 1}/{num_epochs}')
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data batches
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # Zero the parameter gradients
                optimizer.zero_grad()

                # Forward pass (track history only if training)
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
                    _, preds = torch.max(outputs, 1)

                    # Backward pass & optimize if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # Statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)

            print(f'{phase.capitalize()} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

            # Deep copy the model weights if we get the best validation accuracy
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
            if phase == 'val':
                val_acc_history.append(epoch_acc.item())

        print()

    time_elapsed = time.time() - since
    print(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
    print(f'Best Val Acc: {best_acc:4f}')

    # Load best model weights
    model.load_state_dict(best_model_wts)
    return model, val_acc_history

# ==========================================
# 4. EXECUTION ORCHESTRATOR
# ==========================================
if __name__ == '__main__':
    # Configuration parameters
    DATA_DIR = './dataset'  # Adjust path to your dataset folder
    NUM_CLASSES = 3         # e.g., benign, contraband, document_forgery
    BATCH_SIZE = 32
    EPOCHS = 10
    FEATURE_EXTRACT = True  # Set to False to fine-tune entire network
    
    # Device selection (CUDA GPU if available)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Executing training pipeline on device: {device}")

    # Standard ImageNet normalization transforms (OpenCV used for resizing)
    data_transforms = {
        'train': transforms.Compose([
            transforms.ToTensor(),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    # Initialize Datasets and Loaders
    image_datasets = {
        x: ForensicImageDataset(os.path.join(DATA_DIR, x), data_transforms[x])
        for x in ['train', 'val']
    }
    
    dataloaders = {
        x: DataLoader(image_datasets[x], batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
        for x in ['train', 'val']
    }

    # Initialize Model
    model = initialize_model(num_classes=NUM_CLASSES, feature_extract=FEATURE_EXTRACT)
    model = model.to(device)

    # Loss function and optimizer selection
    # Using weighted loss function can help if your classes are highly imbalanced
    criterion = nn.CrossEntropyLoss()
    
    # Gather parameters to update
    params_to_update = model.parameters()
    if FEATURE_EXTRACT:
        params_to_update = []
        for name, param in model.named_parameters():
            if param.requires_grad:
                params_to_update.append(param)
                
    optimizer = optim.Adam(params_to_update, lr=0.001)

    # Begin Training
    print("Initializing model training cycle...")
    trained_model, history = train_model(model, dataloaders, criterion, optimizer, device, num_epochs=EPOCHS)
    
    # Save the trained model weights
    save_path = './resnet50_forensic_model.pth'
    torch.save(trained_model.state_dict(), save_path)
    print(f"Model saved successfully to {save_path}")
