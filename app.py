import streamlit as st
import time
import torch
import torch.nn as nn
from torchvision import models, transforms
import cv2
import numpy as np
import os
import pandas as pd
import glob
import joblib
import easyocr
from skimage.feature import hog

try:
    from transformers import pipeline
    from PIL import Image
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

# --- Configuration & Setup ---
st.set_page_config(page_title="Forensic Image Triage Dashboard", page_icon="🔍", layout="wide")
CLASSES = ['alcohol', 'drugs', 'weapons']
NUM_CLASSES = len(CLASSES)
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
MODELS_DIR = "models_output"
VISUALS_DIR = "visuals"

# OCR Keywords for semantic override
DRUG_KEYWORDS = ['heroin', 'cocaine', 'lsd', 'morphine', 'fentanyl', 'cannabis', 'weed', 'meth', 'mdma', 'codeine', 'syrup', 'promethazine', 'rx', 'prescription', 'mg', 'ml', 'injection', 'syringe', 'pharmacy', 'medicine', 'tablet', 'pill', 'liquid']
ALCOHOL_KEYWORDS = ['vodka', 'whiskey', 'rum', 'beer', 'gin', 'tequila', 'liquor']

# --- UI Styling ---
st.markdown("""
<style>
    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f, #2a2a40);
        color: #ffffff;
    }
    
    h1 {
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00C9FF 0%, #92FE9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 10px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(25, 25, 35, 0.95);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Progress bars */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(90deg, #00C9FF, #92FE9D);
        border-radius: 10px;
    }

    /* Primary Button */
    .stButton>button {
        background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(142, 84, 233, 0.4);
        color: white;
    }
    
    /* Metrics font color to be visible on dark background */
    [data-testid="stMetricValue"] {
        color: #00C9FF;
    }
</style>
""", unsafe_allow_html=True)

# --- Loaders ---
@st.cache_resource
def load_ocr_reader():
    # Initialize the EasyOCR reader (loads weights into memory once)
    return easyocr.Reader(['en'], gpu=torch.cuda.is_available())

@st.cache_resource
def load_clip_override():
    if not HAS_TRANSFORMERS: return None
    return pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32")

@st.cache_resource
def load_model(model_name):
    if model_name == 'clip':
        if not HAS_TRANSFORMERS:
            st.error("Transformers not installed. Run 'pip install transformers Pillow'")
            return None
        return {"model": pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32"), "type": "clip"}

    model = None
    
    # 1. Deep Learning Models
    if model_name in ['resnet50', 'mobilenetv3', 'vgg16']:
        if model_name == 'resnet50':
            model = models.resnet50(weights=None)
            num_ftrs = model.fc.in_features
            model.fc = nn.Sequential(
                nn.Linear(num_ftrs, 512), nn.ReLU(), nn.Dropout(0.5), nn.Linear(512, NUM_CLASSES)
            )
            path = os.path.join(MODELS_DIR, "resnet50", "resnet50_forensic_model.pth")
        
        elif model_name == 'mobilenetv3':
            model = models.mobilenet_v3_large(weights=None)
            num_ftrs = model.classifier[3].in_features
            model.classifier[3] = nn.Sequential(
                nn.Linear(num_ftrs, 512), nn.ReLU(), nn.Dropout(0.5), nn.Linear(512, NUM_CLASSES)
            )
            path = os.path.join(MODELS_DIR, "mobilenetv3", "mobilenetv3_forensic_model.pth")
            
        elif model_name == 'vgg16':
            model = models.vgg16(weights=None)
            num_ftrs = model.classifier[6].in_features
            model.classifier[6] = nn.Sequential(
                nn.Linear(num_ftrs, 512), nn.ReLU(), nn.Dropout(0.5), nn.Linear(512, NUM_CLASSES)
            )
            path = os.path.join(MODELS_DIR, "vgg16", "vgg16_forensic_model.pth")

        if os.path.exists(path):
            model.load_state_dict(torch.load(path, map_location=DEVICE))
            model = model.to(DEVICE)
            model.eval()
            return {"model": model, "type": "pytorch"}
        else:
            st.error(f"PyTorch model weights not found at {path}.")
            return None

    # 2. Classical OpenCV Models
    else:
        scaler_path = os.path.join(MODELS_DIR, "scaler.pkl")
        model_paths = {
            "opencv_svm": "svm_forensic_model.pkl",
            "opencv_rf": "rf_forensic_model.pkl",
            "opencv_knn": "knn_forensic_model.pkl"
        }
        
        model_path = os.path.join(MODELS_DIR, model_paths[model_name])
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            with open(model_path, 'rb') as f:
                model = joblib.load(f)
            with open(scaler_path, 'rb') as f:
                scaler = joblib.load(f)
            return {"model": model, "scaler": scaler, "type": "sklearn"}
        else:
            st.error(f"Classical model or scaler not found at {model_path}")
            return None

# --- Pre-processing Pipeline ---
def preprocess_image_pytorch(image):
    image = cv2.resize(image, (224, 224))
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0).to(DEVICE)

def preprocess_image_opencv(img, scaler):
    img = cv2.resize(img, (224, 224))
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hist = cv2.calcHist([img_hsv], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    hist_features = hist.flatten()
    
    # Structural Features (HOG)
    img_hog = cv2.resize(img, (64, 128))
    img_hog_gray = cv2.cvtColor(img_hog, cv2.COLOR_RGB2GRAY)
    hog_features = hog(img_hog_gray, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm='L2-Hys', visualize=False)
    
    combined = np.hstack([hist_features, hog_features])
    scaled = scaler.transform([combined])
    return scaled

def perform_ocr(reader, img):
    """ Extract text from image and look for semantic overrides """
    # UPSCALING HACK: Double the image resolution so EasyOCR can read small, blurry text on medical bottles
    img_large = cv2.resize(img, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)
    
    results = reader.readtext(img_large, detail=0)
    text_found = " ".join(results).lower()
    
    # Check for drugs
    for kw in DRUG_KEYWORDS:
        if kw in text_found:
            return "drugs", text_found
            
    # Check for alcohol
    for kw in ALCOHOL_KEYWORDS:
        if kw in text_found:
            return "alcohol", text_found
            
    return None, text_found

# --- Main App ---
def main():
    st.title("🔍 Automated Digital Forensic Triage Dashboard")
    st.markdown("Developed as part of an MSc Digital Forensics Dissertation. **Now featuring Hybrid OCR Intelligence.**")
    
    # Load Models
    ocr_reader = load_ocr_reader()
    clip_override_engine = load_clip_override()
    
    # Setup Tabs
    tab_analysis, tab_analytics = st.tabs(["📂 Evidence Analysis", "📊 Model Analytics"])
    
    # ----------------------------------------
    # TAB 1: EVIDENCE ANALYSIS
    # ----------------------------------------
    with tab_analysis:
        st.markdown("### Upload seized device images to quickly identify potential evidentiary material.")
        
        with st.sidebar:
            st.header("⚙️ Classification Engine")
            st.markdown("Select the mathematical algorithm used to analyze the images:")
            model_options = {
                "Deep Learning: MobileNetV3 (Recommended / Fast)": "mobilenetv3",
                "Deep Learning: ResNet-50": "resnet50",
                "Classical ML: Random Forest": "opencv_rf",
                "Classical ML: SVM": "opencv_svm",
                "Deep Learning: VGG-16": "vgg16",
                "Classical ML: KNN": "opencv_knn",
                "Multi-Modal AI: CLIP (Zero-Shot)": "clip"
            }
            selected_display_name = st.selectbox("Select Model Architecture", list(model_options.keys()))
            model_choice = model_options[selected_display_name]
            st.info("PyTorch models utilize CNN feature extraction. Classical ML utilizes deterministic OpenCV spatial features. All models are now augmented with OCR Semantic Override.")
            
        model = load_model(model_choice)
        if model is None:
            return
            
        input_mode = st.radio("Input Mode", ["Upload Files", "Folder Path (Local)"], horizontal=True)
        files_to_process = []
        
        if input_mode == "Upload Files":
            uploaded_files = st.file_uploader("Select one or more images...", type=['jpg', 'jpeg', 'png', 'bmp'], accept_multiple_files=True)
            if uploaded_files:
                files_to_process = [{"name": f.name, "type": "upload", "file_obj": f} for f in uploaded_files]
        else:
            folder_path = st.text_input("Enter absolute folder path containing images:")
            if folder_path and os.path.isdir(folder_path):
                valid_exts = ('*.jpg', '*.jpeg', '*.png', '*.bmp')
                found_files = []
                for ext in valid_exts:
                    found_files.extend(glob.glob(os.path.join(folder_path, ext)))
                    found_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
                
                if not found_files:
                    st.warning("No supported images (.jpg, .png, .bmp) found in the provided directory.")
                else:
                    st.success(f"Found {len(found_files)} images in folder.")
                    if st.button("Process Entire Folder"):
                        files_to_process = [{"name": os.path.basename(f), "type": "path", "path": f} for f in found_files]
        
        if files_to_process:
            st.markdown(f"**Analyzing {len(files_to_process)} image(s) using {selected_display_name} + OCR...**")
            st.markdown("---")
            
            results_data = []
            
            for idx, file_item in enumerate(files_to_process):
                with st.container():
                    col_img, col_blueprint, col_stats = st.columns([1, 1, 2])
                    
                    try:
                        if file_item["type"] == "upload":
                            file_bytes = np.asarray(bytearray(file_item["file_obj"].getvalue()), dtype=np.uint8)
                            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                        else:
                            img = cv2.imread(file_item["path"])
                            
                        if img is None:
                            with col_img:
                                st.error(f"Image '{file_item['name']}' could not be decoded. It may be corrupted or in an unsupported format.")
                            continue
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    except Exception as e:
                        with col_img:
                            st.error(f"Failed to read image '{file_item['name']}'. It may be corrupted or unsupported.")
                        continue
                    
                    with col_img:
                        st.image(img, caption=file_item['name'], width="stretch")
                        
                    with col_blueprint:
                        # Generate structural blueprint (Edge Map) to show shape analysis
                        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                        edges = cv2.Canny(gray, 50, 150)
                        # Add a blueprint color tint for aesthetics
                        blueprint = np.zeros_like(img)
                        blueprint[:, :, 2] = edges  # Blue channel
                        blueprint[:, :, 1] = edges // 2 # Slightly cyan
                        st.image(blueprint, caption="Structural Edge Map", width="stretch")
                    
                    with col_stats:
                        with st.spinner("Analyzing digital evidence..."):
                            # 1. OCR Extraction (Semantic check)
                            override_class, detected_text = None, ""
                            try:
                                override_class, detected_text = perform_ocr(ocr_reader, img)
                            except Exception as e:
                                st.error(f"OCR Engine Error: {e}")
                            
                            if override_class:
                                st.warning(f"**OCR Semantic Override Triggered!** Found keywords in text: '{detected_text}'")
                                top_class = override_class
                                top_prob = 100.0
                                probs_list = [0.0, 0.0, 0.0]
                                probs_list[CLASSES.index(override_class)] = 100.0
                                status_color = "🔴 High Confidence (OCR Verified)"
                                inference_time_ms = 0.0  # Skipped visual inference
                                
                            else:
                                # 2. Visual Inference (Shape check)
                                start_time = time.time()
                                try:
                                    if model["type"] == "pytorch":
                                        input_tensor = preprocess_image_pytorch(img)
                                        with torch.no_grad():
                                            outputs = model["model"](input_tensor)
                                            probabilities = torch.nn.functional.softmax(outputs, dim=1)[0] * 100
                                            probs_list = probabilities.cpu().numpy()
                                    elif model["type"] == "clip":
                                        pil_img = Image.fromarray(img)
                                        candidate_labels = [
                                            "alcohol, beer bottles, liquor",
                                            "illicit drugs, pills, medical syrup, syringes",
                                            "weapons such as guns, knives, flails",
                                            "normal everyday benign photos, unrelated objects, animals, vehicles, scenery"
                                        ]
                                        clip_results = model["model"](pil_img, candidate_labels=candidate_labels)
                                        probs_list = [0.0, 0.0, 0.0]
                                        clip_top_label = clip_results[0]['label']
                                        for res in clip_results:
                                            label_text = res['label']
                                            score = res['score'] * 100
                                            if "alcohol" in label_text: probs_list[0] = score
                                            elif "drugs" in label_text: probs_list[1] = score
                                            elif "weapons" in label_text: probs_list[2] = score
                                    else:
                                        input_features = preprocess_image_opencv(img, model["scaler"])
                                        probs_list = model["model"].predict_proba(input_features)[0] * 100
                                    
                                    top_class_idx = np.argmax(probs_list)
                                    top_class = CLASSES[top_class_idx]
                                    top_prob = probs_list[top_class_idx]
                                    
                                    # Confidence Threshold Exclusion Filter
                                    if top_prob < 50.0:
                                        top_class = "excluded"
                                        
                                    # CLIP Primary Benign Trap
                                    if model["type"] == "clip" and "benign" in clip_top_label:
                                        top_class = "excluded"
                                        top_prob = clip_results[0]['score'] * 100
                                except Exception as e:
                                    st.error(f"Inference Error: {e}")
                                    continue
                                
                                inference_time_ms = (time.time() - start_time) * 1000
                            
                            if top_class == "excluded":
                                status_color = "🟢 Excluded (Out of Distribution)"
                            elif top_prob > 80:
                                status_color = "🔴 High Confidence Visual Evidence"
                            elif top_prob > 50:
                                status_color = "🟡 Moderate Confidence"
                            else:
                                status_color = "🟢 Low Confidence / Benign"
                                
                            # 3. Multi-Modal Semantic Override (CLIP)
                            if model["type"] != "clip" and clip_override_engine is not None and top_class != "excluded":
                                pil_img = Image.fromarray(img)
                                candidate_labels = [
                                    "alcohol, beer bottles, liquor",
                                    "illicit drugs, pills, medical syrup, syringes",
                                    "weapons such as guns, knives, flails",
                                    "normal everyday benign photos, unrelated objects, animals, vehicles, scenery"
                                ]
                                clip_results = clip_override_engine(pil_img, candidate_labels=candidate_labels)
                                best_clip = clip_results[0]
                                if best_clip['score'] > 0.85: # 85% confidence threshold for override
                                    if "benign" in best_clip['label']:
                                        clip_class = "excluded"
                                    else:
                                        clip_class = "alcohol" if "alcohol" in best_clip['label'] else ("drugs" if "drugs" in best_clip['label'] else "weapons")
                                    
                                    if clip_class != top_class:
                                        if clip_class == "excluded":
                                            st.warning(f"**Multi-Modal Override!** Semantic AI is {(best_clip['score']*100):.1f}% confident this image is unrelated to forensics.")
                                            status_color = "🟢 Excluded (Semantic AI Verified)"
                                        else:
                                            st.warning(f"**Multi-Modal Override!** Original model predicted {top_class.capitalize()}, but semantic AI is {(best_clip['score']*100):.1f}% confident this is {clip_class.capitalize()}.")
                                            status_color = "🟣 High Confidence (Semantic AI Verified)"
                                        
                                        top_class = clip_class
                                        top_prob = best_clip['score'] * 100
                                        if clip_class != "excluded":
                                            probs_list = [0.0, 0.0, 0.0]
                                            probs_list[CLASSES.index(clip_class)] = top_prob
                            
                        # -------------------------
                        # Render Premium UI Results
                        # -------------------------
                        st.subheader("Analysis Results")
                        st.markdown(f"**Verification Status:** {status_color}")
                        
                        # Top metric layout
                        metric_col1, metric_col2, metric_col3 = st.columns(3)
                        with metric_col1:
                            st.metric(label="Top Prediction", value=top_class.capitalize())
                        with metric_col2:
                            st.metric(label="Confidence", value=f"{top_prob:.1f}%")
                        with metric_col3:
                            st.metric(label="Inference Time", value=f"{inference_time_ms:.1f} ms")
                        
                        # Show Raw OCR Text for Transparency
                        if detected_text and detected_text.strip():
                            st.info(f"👁️ **OCR Scanner Caught Text:** `{detected_text}`")
                        
                        result_row = {
                            "Filename": file_item['name'],
                            "Prediction": top_class.capitalize(),
                            "Confidence (%)": f"{top_prob:.2f}",
                            "OCR Detected": detected_text if detected_text else "None"
                        }
                        
                        # Detailed Probabilities Expander
                        with st.expander("View Detailed Class Probabilities"):
                            st.markdown("#### Confidence Breakdown")
                            cat_cols = st.columns(3)
                            for i, class_name in enumerate(CLASSES):
                                prob = float(probs_list[i])
                                result_row[f"{class_name.capitalize()} Prob"] = f"{prob:.2f}"
                                with cat_cols[i]:
                                    st.write(f"**{class_name.capitalize()}**")
                                    st.write(f"{prob:.2f}%")
                                    st.progress(int(prob) if prob > 0 else 0)
                            
                        results_data.append(result_row)
                        
                st.divider()
            
            if results_data:
                st.toast("✅ Processing Complete!", icon="🎉")
                st.markdown("### Export Triage Report")
                df = pd.DataFrame(results_data)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Secure Results (CSV)",
                    data=csv,
                    file_name='forensic_hybrid_triage_report.csv',
                    mime='text/csv',
                )

    # ----------------------------------------
    # TAB 2: MODEL ANALYTICS
    # ----------------------------------------
    with tab_analytics:
        st.header("📊 Evaluation Analytics & Proof")
        st.markdown("This section validates the performance of the chosen mathematical models against the highly curated test dataset.")
        
        st.subheader("1. Dataset Distribution")
        dist_path = os.path.join(VISUALS_DIR, "dataset_distribution.png")
        if os.path.exists(dist_path):
            st.image(dist_path, width="stretch")
            
        st.subheader("2. Model Evaluation Matrices")
        analytics_model = st.selectbox("Select Model Architecture to inspect:", list(model_options.keys()), key="analytics_select")
        
        analytics_key = model_options[analytics_model]
        
        if analytics_key == "clip":
            st.info("The Multi-Modal CLIP model is a dynamic Zero-Shot semantic engine. It does not have a static confusion matrix generated from the classical training pipeline.")
        else:
            # Load Confusion Matrix
            cm_prefix = "pytorch" if "Deep Learning" in analytics_model else "opencv"
            if cm_prefix == "opencv":
                cm_suffix = analytics_key.replace("opencv_", "")
            else:
                cm_suffix = analytics_key
                
            cm_path = os.path.join(VISUALS_DIR, f"{cm_prefix}_{cm_suffix}_confusion_matrix.png")
            roc_path = os.path.join(VISUALS_DIR, f"{cm_prefix}_{cm_suffix}_roc_curve.png")
            
            col1, col2 = st.columns(2)
            with col1:
                if os.path.exists(cm_path):
                    st.markdown("**Confusion Matrix**")
                    st.image(cm_path, width="stretch")
                else:
                    st.warning("Confusion matrix not found. Please run the visualization generator script.")
                    
            with col2:
                if cm_prefix == "opencv":
                    if os.path.exists(roc_path):
                        st.markdown("**Multi-Class ROC Curve**")
                        st.image(roc_path, width="stretch")
                    else:
                        st.warning("ROC Curve not found for this classical model.")
                else:
                    st.info("ROC curves are currently only generated for the Classical OpenCV implementations. Please view the confusion matrix for Deep Learning metrics.")

if __name__ == '__main__':
    main()
