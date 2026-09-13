# 🔍 Automated Digital Forensic Image Triage System
### Multi-Modal AI & Classical Computer Vision for Rapid Contraband Evidence Discovery

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-blue?logo=python)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c?logo=pytorch)](https://pytorch.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?logo=opencv)](https://opencv.org)
[![License](https://img.shields.io/badge/License-Academic%20Use-green)](#license)

---

## 📌 Executive Summary

Modern law enforcement agencies face severe **digital forensics backlogs**, with forensic laboratories often taking 12 to 24 months to analyze seized digital storage media (hard drives, mobile phones, SD cards). A single forensic image may contain hundreds of thousands of irrelevant system and cache images, burying critical evidence of illicit activity.

This repository presents an **Automated Forensic Image Triage System** designed to rapidly scan, classify, and prioritize evidentiary media before deep forensic examination. Developed as part of an MSc Digital Forensics dissertation, the platform combines **Deep Convolutional Neural Networks (CNNs)**, **Deterministic OpenCV Spatial/Color Feature Extractors**, and **Hybrid Optical Character Recognition (OCR) Semantic Overrides** to detect contraband categories with high recall:
* 💊 **Illicit Narcotics & Prescription Drugs**
* 🔫 **Weapons & Firearms**
* 🍾 **Alcohol Contraband**

---

## 🏛️ System Architecture

```
                                  [Seized Storage Device]
                                             │
                                             ▼
                                  [Forensic Media Intake]
                                             │
                   ┌─────────────────────────┴─────────────────────────┐
                   ▼                                                   ▼
       ┌───────────────────────┐                           ┌───────────────────────┐
       │   Visual Inspection   │                           │  Text & Label Intake  │
       │   (224x224 RGB Frame) │                           │  (Upscaled Resolution)│
       └───────────┬───────────┘                           └───────────┬───────────┘
                   │                                                   │
         ┌─────────┴─────────┐                                         ▼
         ▼                   ▼                             ┌───────────────────────┐
┌─────────────────┐ ┌─────────────────┐                    │   EasyOCR Engine      │
│  Deep Learning  │ │  Classical ML   │                    │ (Text Transcription)  │
│  (MobileNetV3 / │ │  (HOG + Color   │                    └───────────┬───────────┘
│   ResNet-50)    │ │   Hist + SVM)   │                                │
└────────┬────────┘ └────────┬────────┘                                │
         │                   │                                         │
         └─────────┬─────────┘                                         │
                   ▼                                                   ▼
        ┌─────────────────────┐                            ┌───────────────────────┐
        │ Visual Probabilities│                            │ Semantic Drug/Weapons │
        │ [Alcohol, Drugs, ..]│                            │   Keyword Detection   │
        └──────────┬──────────┘                            └───────────┬───────────┘
                   │                                                   │
                   └─────────────────────────┬─────────────────────────┘
                                             ▼
                                ┌─────────────────────────┐
                                │ Hybrid Triage Decision  │
                                │   & Semantic Override   │
                                └────────────┬────────────┘
                                             │
                                             ▼
                                ┌─────────────────────────┐
                                │ Priority Evidence Queue │
                                │ (Interactive Dashboard) │
                                └─────────────────────────┘
```

### 1. Hybrid Multi-Modal Intelligence
Visual classifiers frequently struggle when pills or liquid narcotics are packaged in nondescript medical bottles or sealed syrup containers. To solve this, our pipeline deploys a **dual-stream triage engine**:
- **Computer Vision Stream**: Classifies structural contours, textures, and global color signatures.
- **OCR Semantic Override Stream**: Uses **EasyOCR** with bicubic resolution enhancement (2.5x upscale) to transcribe pharmaceutical labels, prescription codes, dosage markers (`mg`, `ml`), and known illicit drug terminology (`codeine`, `promethazine`, `fentanyl`, `morphine`, `cannabis`, etc.). If a positive keyword match occurs, the system immediately flags the artifact for priority forensic review regardless of visual background noise.

### 2. Model Architectures Implemented
* **MobileNetV3 Large (Default / Production)**: Lightweight, depthwise-separable architecture engineered specifically for low-latency CPU-constrained forensic field workstations (~35–45ms per image).
* **ResNet-50**: Deep residual network featuring skip connections for robust feature extraction on visually cluttered scenes.
* **Classical OpenCV Machine Learning**: Deterministic **Histogram of Oriented Gradients (HOG)** (9 orientations, 8x8 cells) + **3D HSV Color Histograms** (512 bins) trained with **Support Vector Machines (SVM)** and **Random Forest (RF)**.

---

## 📊 Performance & Evaluation Highlights

| Model Architecture | Parameter Size | Primary Advantage | CPU Inference Latency | Forensic Suitability |
| :--- | :---: | :--- | :---: | :---: |
| **MobileNetV3** | **18.7 MB** | Optimized latency & minimal memory footprint | **~38 ms** | ⭐ **Best for Field Triage** |
| **ResNet-50** | 94.0 MB | High feature discrimination in dense scenes | ~112 ms | Excellent for Lab Servers |
| **Random Forest (HOG+Hist)** | 5.2 MB | Lightweight deterministic baseline | ~48 ms | Fast CPU Baseline |
| **SVM (HOG+Hist)** | 78.1 MB | Non-linear boundary separation | ~62 ms | Classical Machine Learning |
| **VGG-16** | 520.2 MB | Deep feature hierarchy benchmark | ~240 ms | Research Baseline |

---

## 🖥️ Forensic Dashboard Features

The dashboard (`app.py`) provides an investigative user interface built with Streamlit:

* **Dual Intake Modes**:
  * **Single / Multi-File Upload**: Upload evidence directly for quick forensic inspection.
  * **Batch Directory Intake**: Point the dashboard at an extracted case directory or mounted forensic image for batch processing.
* **Live Architecture Switching**: Hot-swap between MobileNetV3, ResNet-50, SVM, and Random Forest to cross-validate evidentiary findings.
* **Evidence Breakdown**: Displays the raw evidence photograph, extracted OCR keywords, confidence scores per category, and the final prioritized triage decision.
* **Auditability & Traceability**: Inference times and prediction metrics are computed deterministically to assist forensic documentation and chain of custody reporting.

---

## ⚡ Quickstart & Local Installation

### Prerequisites
* Python 3.9, 3.10, or 3.11
* `git`

### 1. Clone the Repository
```bash
git clone https://github.com/ALSTONDARREN/forensic-image-triage.git
cd forensic-image-triage
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Streamlit Dashboard
```bash
streamlit run app.py
```
Open your browser at **`http://localhost:8501`**.

---

## 🐳 Docker Deployment

To deploy in an isolated, forensically sound containerized environment:

```bash
# 1. Build the Docker image
docker build -t forensic-image-triage .

# 2. Run the container on port 8501
docker run -d -p 8501:8501 --name forensic_triage forensic-image-triage
```
Access the application at `http://localhost:8501`.

---

## ☁️ Streamlit Community Cloud Deployment

This repository is pre-configured with:
- **`packages.txt`**: Declares necessary Debian shared libraries (`libgl1`, `libglib2.0-0`) for headless OpenCV execution.
- **`requirements.txt`**: Standardized dependencies using `opencv-python-headless` and `scikit-image`.
- **`models_output/`**: Includes pre-trained weights for `MobileNetV3` (18.7 MB), `ResNet-50` (94 MB), `SVM` (78 MB), and `Random Forest` (5.2 MB).

To deploy:
1. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Click **New app** and select repository `ALSTONDARREN/forensic-image-triage`.
3. Set **Branch** to `main` and **Main file path** to `app.py`.
4. Click **Deploy!**

---

## 📂 Project Structure

```
forensic-image-triage/
├── app.py                      # Interactive Streamlit Triage Dashboard
├── Dockerfile                  # Container definition for reproducible deployment
├── requirements.txt            # Python package dependencies
├── packages.txt                # Linux OS packages (libgl1, libglib2.0-0)
├── .gitignore                  # Git ignore rules (filters datasets & oversized files)
├── models_output/              # Trained AI model checkpoints
│   ├── classes.pkl             # Class index mapping
│   ├── scaler.pkl              # StandardScaler for OpenCV features
│   ├── rf_forensic_model.pkl   # Classical Random Forest model
│   ├── svm_forensic_model.pkl  # Classical SVM model
│   ├── mobilenetv3/            # MobileNetV3 PyTorch weights (.pth)
│   └── resnet50/               # ResNet-50 PyTorch weights (.pth)
├── scripts/                    # Training, benchmarking, and export utilities
│   ├── train_models_fast.py    # PyTorch training pipeline with augmentation
│   ├── train_opencv_svm.py     # OpenCV HOG + Color feature extraction & training
│   ├── benchmark_inference.py  # Latency and throughput benchmarking
│   ├── export_to_onnx.py       # ONNX runtime model export utility
│   └── verify_phase6.py        # Streamlit AppTest automated verification
└── visuals/                    # Confusion matrices, ROC curves, and system diagrams
```

---

## 🛡️ Forensic Integrity & Ethical Considerations

1. **Read-Only Media Handling**: This tool operates strictly as an evidence triage classifier. It should only be executed against bit-stream duplicate disk images or extracted read-only directories, never against primary physical evidence.
2. **Human-in-the-Loop Verification**: Triage classifications are probabilistic indicators intended to guide forensic examiner prioritization and eliminate backlog latency. Final evidentiary determinations require qualified forensic examiner review.
3. **Data Protection & Privacy**: Any training datasets and test evidence containing sensitive indicators must be handled in compliance with applicable evidentiary handling frameworks (e.g., ISO/IEC 27037 and ACPO Good Practice Guides).

---

## 👤 Author & Acknowledgments

* **Author**: Alston Darren Pereira
* **Degree**: MSc Digital Forensics
* **Institution**: University of Bedfordshire / Digital Forensics Research Group

---

## 📄 License

This repository is distributed for academic research, education, and forensic evaluation purposes.
