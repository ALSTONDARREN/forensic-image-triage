import os
import argparse
import time
import cv2
import numpy as np
import joblib
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_recall_fscore_support, matthews_corrcoef, confusion_matrix
from sklearn.preprocessing import StandardScaler
from skimage.feature import hog

# ==========================================
# 1. OPENCV FEATURE EXTRACTION PIPELINE
# ==========================================
def extract_features(img_path):
    """
    Extracts a combined feature vector of Color Histograms and HOG (Structural) features
    using pure OpenCV.
    """
    img = cv2.imread(img_path)
    if img is None:
        # Fallback for corrupt images (HOG + Hist size combined)
        return np.zeros((3780 + 512,), dtype=np.float32)

    # Resize to standard size for deterministic HOG
    img = cv2.resize(img, (128, 128))
    
    # 1. Color Histogram (Global color distribution)
    # Extract 3D color histogram (8 bins per channel) -> 8x8x8 = 512 dimensions
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([img_hsv], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    hist_features = hist.flatten()
    
    # 2. Structural Features (HOG - Histogram of Oriented Gradients)
    img_hog = cv2.resize(img, (64, 128))
    img_hog_gray = cv2.cvtColor(img_hog, cv2.COLOR_BGR2GRAY)
    hog_features = hog(img_hog_gray, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm='L2-Hys', visualize=False)
    
    # Combine features
    combined_features = np.hstack([hist_features, hog_features])
    return combined_features

# ==========================================
# 2. DATASET LOADING
# ==========================================
def load_dataset(data_dir):
    """
    Iterates through class directories, extracting features.
    """
    X = []
    y = []
    classes = sorted([d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))])
    class_to_idx = {cls_name: i for i, cls_name in enumerate(classes)}
    
    print(f"Loading data from {data_dir}...")
    for cls_name in classes:
        cls_dir = os.path.join(data_dir, cls_name)
            
        files = [f for f in os.listdir(cls_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
        print(f"  Extracting features for class '{cls_name}' ({len(files)} images)...")
        
        for img_name in files:
            img_path = os.path.join(cls_dir, img_name)
            features = extract_features(img_path)
            X.append(features)
            y.append(class_to_idx[cls_name])
            
    return np.array(X), np.array(y), classes

# ==========================================
# 3. MAIN TRAINING SCRIPT
# ==========================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="MSc Thesis OpenCV+SVM Training Pipeline")
    parser.add_argument('--data_dir', type=str, default='./data', help="Path to dataset directory (should contain train/ and val/)")
    parser.add_argument('--output_dir', type=str, default='./models_output', help="Output directory for model")
    
    args, unknown = parser.parse_known_args()
    
    DATA_DIR = args.data_dir
    OUTPUT_DIR = args.output_dir
    
    train_dir = os.path.join(DATA_DIR, 'train')
    val_dir = os.path.join(DATA_DIR, 'val')
    
    print("==========================================")
    print("Pipeline       : OpenCV + SVM")
    print(f"Train Dataset  : {train_dir}")
    print(f"Val Dataset    : {val_dir}")
    print("==========================================\n")
    
    if not os.path.exists(train_dir) or not os.path.exists(val_dir):
        print("[Error] Train or Val directories not found inside data directory.")
        exit(1)
        
    # 1. Load Training Data
    start_time = time.time()
    X_train, y_train, classes = load_dataset(train_dir)
    print(f"Training data loaded in {time.time() - start_time:.2f}s. Shape: {X_train.shape}\n")
    
    # 2. Scale Features
    print("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # 3. Train Models
    print("Training Support Vector Machine (RBF Kernel)...")
    start_time = time.time()
    svm_model = SVC(kernel='rbf', probability=True, random_state=42)
    svm_model.fit(X_train_scaled, y_train)
    print(f"SVM trained in {time.time() - start_time:.2f}s.\n")
    
    print("Training Random Forest Classifier...")
    start_time = time.time()
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    print(f"Random Forest trained in {time.time() - start_time:.2f}s.\n")
    
    print("Training K-Nearest Neighbors Classifier...")
    start_time = time.time()
    knn_model = KNeighborsClassifier(n_neighbors=5)
    knn_model.fit(X_train_scaled, y_train)
    print(f"KNN trained in {time.time() - start_time:.2f}s.\n")
    
    # 4. Load and Evaluate on Validation Data
    X_val, y_val, _ = load_dataset(val_dir)
    if len(X_val) > 0:
        X_val_scaled = scaler.transform(X_val)
        
        models_dict = {
            "SVM": svm_model,
            "Random Forest": rf_model,
            "KNN": knn_model
        }
        
        for name, model in models_dict.items():
            print(f"\nEvaluating {name} on Validation Set...")
            y_pred = model.predict(X_val_scaled)
            
            acc = np.mean(y_pred == y_val)
            precision, recall, f1, _ = precision_recall_fscore_support(y_val, y_pred, average='weighted', zero_division=0)
            mcc = matthews_corrcoef(y_val, y_pred)
            
            print(f"\n--- {name} Validation Results ---")
            print(f"Accuracy  : {acc:.4f}")
            print(f"Precision : {precision:.4f}")
            print(f"Recall    : {recall:.4f}")
            print(f"F1 Score  : {f1:.4f}")
            print(f"MCC       : {mcc:.4f}")
            print("-" * 26)
    else:
        print("\nNo validation data found. Skipping evaluation.")
    
    # 5. Save the Pipeline
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    joblib.dump(svm_model, os.path.join(OUTPUT_DIR, 'svm_forensic_model.pkl'))
    joblib.dump(rf_model, os.path.join(OUTPUT_DIR, 'rf_forensic_model.pkl'))
    joblib.dump(knn_model, os.path.join(OUTPUT_DIR, 'knn_forensic_model.pkl'))
    joblib.dump(scaler, os.path.join(OUTPUT_DIR, 'scaler.pkl'))
    joblib.dump(classes, os.path.join(OUTPUT_DIR, 'classes.pkl'))
    print(f"\n[Success] All models and scaler saved to {OUTPUT_DIR}")
