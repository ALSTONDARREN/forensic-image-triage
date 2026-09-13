import time
import os
import glob
import torch
import torch.nn as nn
from torchvision import models, transforms
import cv2
import numpy as np
import joblib
from skimage.feature import hog
import warnings
warnings.filterwarnings("ignore")

# --- Config ---
DATA_DIR = r"C:\Users\perei\Documents\thesis\data\dataset_split\val"
MODELS_DIR = r"C:\Users\perei\Documents\thesis\models_output"
CLASSES = ['alcohol', 'drugs', 'weapons']
DEVICE = torch.device("cpu") # Force CPU for realistic hardware benchmarking

# Load test images
test_images = []
for cls in CLASSES:
    cls_dir = os.path.join(DATA_DIR, cls)
    if not os.path.exists(cls_dir): continue
    for ext in ('*.jpg', '*.png', '*.jpeg'):
        test_images.extend(glob.glob(os.path.join(cls_dir, ext)))
        test_images.extend(glob.glob(os.path.join(cls_dir, ext.upper())))
test_images = test_images[:100] # Use 100 images for benchmark

print(f"Benchmarking inference speed on CPU using {len(test_images)} images...")

# --- OpenCV Models ---
def benchmark_opencv():
    print("\n--- OpenCV Classical Pipeline ---")
    scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
    if not os.path.exists(scaler_path): return
    scaler = joblib.load(open(scaler_path, 'rb'))
    
    models_to_test = {
        "Random Forest": "rf_forensic_model.pkl",
        "SVM": "svm_forensic_model.pkl",
    }
    
    for name, file in models_to_test.items():
        model_path = os.path.join(MODELS_DIR, file)
        if not os.path.exists(model_path): continue
        model = joblib.load(open(model_path, 'rb'))
        
        start_time = time.time()
        for img_path in test_images:
            img = cv2.imread(img_path)
            if img is None: continue
            img = cv2.resize(img, (224, 224))
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([img_hsv], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            cv2.normalize(hist, hist)
            hist_features = hist.flatten()
            
            img_hog = cv2.resize(img, (64, 128))
            img_hog_gray = cv2.cvtColor(img_hog, cv2.COLOR_BGR2GRAY)
            hog_features = hog(img_hog_gray, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm='L2-Hys', visualize=False)
            
            combined = np.hstack([hist_features, hog_features])
            scaled = scaler.transform([combined])
            _ = model.predict(scaled)
            
        elapsed = time.time() - start_time
        print(f"{name}: {elapsed:.2f}s total | {elapsed/len(test_images)*1000:.2f}ms per image")

# --- PyTorch Models ---
def benchmark_pytorch():
    print("\n--- PyTorch Deep Learning Pipeline ---")
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    pt_models = {
        "ResNet50": "resnet50",
        "MobileNetV3": "mobilenetv3"
    }
    
    for display_name, m_name in pt_models.items():
        model_path = os.path.join(MODELS_DIR, m_name, f"{m_name}_forensic_model.pth")
        if not os.path.exists(model_path): continue
        
        if m_name == "resnet50":
            model = models.resnet50(weights=None)
            model.fc = nn.Sequential(nn.Linear(model.fc.in_features, 512), nn.ReLU(), nn.Dropout(0.5), nn.Linear(512, len(CLASSES)))
        elif m_name == "mobilenetv3":
            model = models.mobilenet_v3_large(weights=None)
            model.classifier[3] = nn.Sequential(nn.Linear(model.classifier[3].in_features, 512), nn.ReLU(), nn.Dropout(0.5), nn.Linear(512, len(CLASSES)))
            
        model.load_state_dict(torch.load(model_path, map_location=DEVICE))
        model.eval()
        
        start_time = time.time()
        with torch.no_grad():
            for img_path in test_images:
                img = cv2.imread(img_path)
                if img is None: continue
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                tensor = transform(img).unsqueeze(0)
                _ = model(tensor)
                
        elapsed = time.time() - start_time
        print(f"{display_name}: {elapsed:.2f}s total | {elapsed/len(test_images)*1000:.2f}ms per image")

if __name__ == '__main__':
    benchmark_opencv()
    benchmark_pytorch()
