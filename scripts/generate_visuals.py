import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import torch.nn as nn
from torchvision import datasets, models, transforms
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
from sklearn.preprocessing import label_binarize
import numpy as np
import cv2
import joblib
from skimage.feature import hog

# --- Configuration ---
DATA_DIR = r"C:\Users\perei\Documents\thesis\data\dataset_split"
VISUALS_DIR = r"C:\Users\perei\Documents\thesis\visuals"
CLASSES = ['alcohol', 'drugs', 'weapons']
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

os.makedirs(VISUALS_DIR, exist_ok=True)

# ==========================================
# PHASE 1: Dataset Visualization
# ==========================================
def plot_dataset_distribution():
    print("Generating Dataset Distribution Chart...")
    splits = ['train', 'val']
    data = {'train': [], 'val': []}
    
    for split in splits:
        for cls in CLASSES:
            path = os.path.join(DATA_DIR, split, cls)
            if os.path.exists(path):
                num_files = len(glob.glob(os.path.join(path, '*.*')))
                data[split].append(num_files)
            else:
                data[split].append(0)
                
    x = np.arange(len(CLASSES))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 6))
    rects1 = ax.bar(x - width/2, data['train'], width, label='Train', color='#4C72B0')
    rects2 = ax.bar(x + width/2, data['val'], width, label='Validation', color='#DD8452')

    ax.set_ylabel('Number of Images')
    ax.set_title('Dataset Distribution by Category and Split')
    ax.set_xticks(x)
    ax.set_xticklabels([c.capitalize() for c in CLASSES])
    ax.legend()
    
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    save_path = os.path.join(VISUALS_DIR, "dataset_distribution.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved dataset visualization to {save_path}")

# ==========================================
# PHASE 2: PyTorch Deep Learning Visualization
# ==========================================
def evaluate_pytorch_model(model_name="resnet50"):
    print(f"Evaluating PyTorch Model: {model_name}...")
    model_path = os.path.join(r"C:\Users\perei\Documents\thesis\models_output", model_name, f"{model_name}_forensic_model.pth")
    if not os.path.exists(model_path):
        print(f"Model not found: {model_path}")
        return

    # Load Model Architectures
    if model_name == "resnet50":
        model = models.resnet50(weights=None)
        num_ftrs = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Linear(num_ftrs, 512), nn.ReLU(), nn.Dropout(0.5), nn.Linear(512, len(CLASSES))
        )
    elif model_name == "vgg16":
        model = models.vgg16(weights=None)
        num_ftrs = model.classifier[6].in_features
        model.classifier[6] = nn.Sequential(
            nn.Linear(num_ftrs, 512), nn.ReLU(), nn.Dropout(0.5), nn.Linear(512, len(CLASSES))
        )
    elif model_name == "mobilenetv3":
        model = models.mobilenet_v3_large(weights=None)
        num_ftrs = model.classifier[3].in_features
        model.classifier[3] = nn.Sequential(
            nn.Linear(num_ftrs, 512), nn.ReLU(), nn.Dropout(0.5), nn.Linear(512, len(CLASSES))
        )
    else:
        print("Unsupported model.")
        return

    model.load_state_dict(torch.load(model_path, map_location=DEVICE))
    model = model.to(DEVICE)
    model.eval()

    # Load Validation Data
    val_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    val_dir = os.path.join(DATA_DIR, 'val')
    val_dataset = datasets.ImageFolder(val_dir, val_transforms)
    val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=32, shuffle=False)

    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs = inputs.to(DEVICE)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())

    # Generate Confusion Matrix
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=[c.capitalize() for c in CLASSES], 
                yticklabels=[c.capitalize() for c in CLASSES])
    plt.title(f'PyTorch {model_name}: Confusion Matrix')
    plt.ylabel('True Category')
    plt.xlabel('Predicted Category')
    plt.tight_layout()
    save_path = os.path.join(VISUALS_DIR, f"pytorch_{model_name}_confusion_matrix.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    
    # Save Classification Report (False-Negative Metrics)
    report = classification_report(all_labels, all_preds, target_names=[c.capitalize() for c in CLASSES])
    report_path = os.path.join(VISUALS_DIR, f"pytorch_{model_name}_classification_report.txt")
    with open(report_path, "w") as f:
        f.write(report)
        
    print(f"Saved PyTorch visuals and report to {VISUALS_DIR}")

# ==========================================
# PHASE 3: OpenCV Machine Learning Visualization
# ==========================================
def extract_opencv_features(image_path):
    img = cv2.imread(image_path)
    if img is None: return None
    img = cv2.resize(img, (224, 224))
    
    # 1. Color Histogram
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([img_hsv], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    hist_features = hist.flatten()
    
    # 2. Structural Features (HOG)
    img_hog = cv2.resize(img, (64, 128))
    img_hog_gray = cv2.cvtColor(img_hog, cv2.COLOR_BGR2GRAY)
    hog_features = hog(img_hog_gray, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm='L2-Hys', visualize=False)
    
    return np.hstack([hist_features, hog_features])

def evaluate_opencv_models():
    print("Evaluating OpenCV Classical Models...")
    OUTPUT_DIR = r"C:\Users\perei\Documents\thesis\models_output"
    scaler_path = os.path.join(OUTPUT_DIR, 'scaler.pkl')
    
    if not os.path.exists(scaler_path):
        print("Scaler not found. Train classical models first.")
        return

    with open(scaler_path, 'rb') as f:
        scaler = joblib.load(f)

    # Load validation set
    val_dir = os.path.join(DATA_DIR, 'val')
    X_val = []
    y_val = []
    
    for idx, cls in enumerate(CLASSES):
        cls_dir = os.path.join(val_dir, cls)
        if not os.path.exists(cls_dir): continue
        valid_exts = ('*.jpg', '*.jpeg', '*.png')
        files = []
        for ext in valid_exts:
            files.extend(glob.glob(os.path.join(cls_dir, ext)))
            files.extend(glob.glob(os.path.join(cls_dir, ext.upper())))
            
        for f in files:
            feats = extract_opencv_features(f)
            if feats is not None:
                X_val.append(feats)
                y_val.append(idx)
                
    if not X_val:
        print("No validation data found for Classical Models.")
        return

    X_val = np.array(X_val)
    X_val_scaled = scaler.transform(X_val)
    
    # Define models to process
    models_to_test = {
        "svm": "svm_forensic_model.pkl",
        "random_forest": "rf_forensic_model.pkl",
        "knn": "knn_forensic_model.pkl"
    }

    for model_name, filename in models_to_test.items():
        model_path = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(model_path):
            print(f"Skipping {model_name}, not found at {model_path}")
            continue
            
        with open(model_path, 'rb') as f:
            model = joblib.load(f)
            
        preds = model.predict(X_val_scaled)
        probs = model.predict_proba(X_val_scaled)
        
        # 1. Confusion Matrix
        cm = confusion_matrix(y_val, preds)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', 
                    xticklabels=[c.capitalize() for c in CLASSES], 
                    yticklabels=[c.capitalize() for c in CLASSES])
        plt.title(f'OpenCV {model_name.upper()}: Confusion Matrix')
        plt.ylabel('True Category')
        plt.xlabel('Predicted Category')
        plt.tight_layout()
        save_path_cm = os.path.join(VISUALS_DIR, f"opencv_{model_name}_confusion_matrix.png")
        plt.savefig(save_path_cm, dpi=300)
        plt.close()
        
        # Save Classification Report
        report = classification_report(y_val, preds, target_names=[c.capitalize() for c in CLASSES])
        report_path = os.path.join(VISUALS_DIR, f"opencv_{model_name}_classification_report.txt")
        with open(report_path, "w") as f:
            f.write(report)
        
        # 2. Multi-class ROC Curve
        y_val_bin = label_binarize(y_val, classes=[0, 1, 2])
        n_classes = y_val_bin.shape[1]
        
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_val_bin[:, i], probs[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])
            
        plt.figure(figsize=(8, 6))
        colors = ['blue', 'red', 'green']
        for i, color in zip(range(n_classes), colors):
            plt.plot(fpr[i], tpr[i], color=color, lw=2,
                     label=f'ROC curve of class {CLASSES[i]} (area = {roc_auc[i]:0.2f})')
                     
        plt.plot([0, 1], [0, 1], 'k--', lw=2)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'OpenCV {model_name.upper()}: Multi-class ROC Curve')
        plt.legend(loc="lower right")
        save_path_roc = os.path.join(VISUALS_DIR, f"opencv_{model_name}_roc_curve.png")
        plt.savefig(save_path_roc, dpi=300)
        plt.close()
        print(f"Saved {model_name.upper()} visuals.")

if __name__ == "__main__":
    print("Starting Visual Generation Pipeline...")
    plot_dataset_distribution()
    evaluate_pytorch_model("resnet50")
    evaluate_pytorch_model("vgg16")
    evaluate_pytorch_model("mobilenetv3")
    evaluate_opencv_models()
    print("Done! All visuals saved to thesis/visuals/")
