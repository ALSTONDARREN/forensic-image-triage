# Title Page

**Project Title:** Image Classification Using Machine Learning for Digital Forensic Investigations  
**University Logo:** [Insert University Logo Here]  
**Author:** Alston Darren Pereira  
**Student ID:** 24850898  
**Formal Title of Degree:** MSc Cyber Security  
**Supervisor:** Dr. Alex Akinbi  
**Department:** Department of Computing and Mathematics  
**Faculty:** Science and Engineering  
**Date:** September 2026  

---

# Table of Contents

| Section | Title |
| :--- | :--- |
| **i** | **Title Page** |
| **ii** | **Abstract** |
| **iii** | **Acknowledgements** |
| **iv** | **Declaration** |
| **v** | **Abbreviations** |
| **vi** | **List of Figures** |
| **vii** | **List of Tables** |
| | |
| **Chapter 1** | **Introduction** |
| 1.1 | Background to the Study |
| 1.2 | Motivation for the Research |
| 1.3 | Aims and Objectives |
| 1.4 | Structure of the Dissertation |
| | |
| **Chapter 2** | **Literature Review** |
| 2.1 | Introduction |
| 2.2 | The Fragility of Cryptographic Hash Matching in Forensics |
| &nbsp;&nbsp;&nbsp;*2.2.1* | *ACPO Guidelines and the Legal Mandate for Hash Integrity* |
| 2.3 | The Deep Learning Revolution in Computer Vision |
| 2.4 | The Operational and Legal Hurdles of Deep Learning in Digital Forensics |
| &nbsp;&nbsp;&nbsp;*2.4.1* | *Data Scarcity and Forensic Privacy Constraints* |
| &nbsp;&nbsp;&nbsp;*2.4.2* | *Dataset Bias, Ethics, and Algorithmic Fairness* |
| &nbsp;&nbsp;&nbsp;*2.4.3* | *Computational Overhead and Hardware Limitations* |
| &nbsp;&nbsp;&nbsp;*2.4.4* | *The "Black-Box" Interpretability Crisis and Legal Admissibility* |
| &nbsp;&nbsp;&nbsp;*2.4.5* | *Adversarial Machine Learning and the FGSM Vulnerability* |
| &nbsp;&nbsp;&nbsp;*2.4.6* | *Legal Admissibility: The Daubert and Frye Standards* |
| 2.5 | Classical Computer Vision: A Return to Determinism |
| &nbsp;&nbsp;&nbsp;*2.5.1* | *SIFT, SURF, and the Evolution of Descriptors* |
| &nbsp;&nbsp;&nbsp;*2.5.2* | *Histogram of Oriented Gradients (HOG): Capturing Structural Geometry* |
| &nbsp;&nbsp;&nbsp;*2.5.3* | *Color Space Analysis* |
| 2.6 | The Synthesis of Semantic OCR and Hybrid Pipelines |
| &nbsp;&nbsp;&nbsp;*2.6.1* | *Comparative Synthesis of Triage Paradigms* |
| 2.7 | Summary |
| | |
| **Chapter 3** | **Design** |
| 3.1 | Introduction |
| 3.2 | Dataset Acquisition, Curation, and Normalization |
| &nbsp;&nbsp;&nbsp;*3.2.1* | *Automated Data Scraping* |
| &nbsp;&nbsp;&nbsp;*3.2.2* | *Normalization and Stratification Pipeline* |
| 3.3 | Classical Feature Extraction (The OpenCV Pipeline) |
| &nbsp;&nbsp;&nbsp;*3.3.1* | *Capturing Color: The 3D HSV Histogram* |
| &nbsp;&nbsp;&nbsp;*3.3.2* | *Capturing Structural Geometry: Histogram of Oriented Gradients (HOG)* |
| &nbsp;&nbsp;&nbsp;*3.3.3* | *Feature Space Dimensionality and Evaluation of PCA* |
| | |
| **Chapter 4** | **Implementation** |
| 4.1 | Introduction |
| 4.2 | Classical Classification Algorithms |
| 4.3 | Deep Learning Baselines and Transfer Learning |
| 4.4 | Hardware and Evaluation Metrics |
| 4.5 | Out-of-Distribution Image Exclusion Filter |
| | |
| **Chapter 5** | **Evaluation** |
| 5.1 | Introduction |
| 5.2 | Statistical Performance of Classical Computer Vision |
| &nbsp;&nbsp;&nbsp;*5.2.1* | *Support Vector Machine (RBF Kernel)* |
| &nbsp;&nbsp;&nbsp;*5.2.2* | *K-Fold Cross-Validation and Statistical Stability* |
| &nbsp;&nbsp;&nbsp;*5.2.3* | *Random Forest Ensemble* |
| &nbsp;&nbsp;&nbsp;*5.2.4* | *Receiver Operating Characteristic (ROC) and AUC Analysis* |
| 5.3 | Deep Learning Baselines |
| &nbsp;&nbsp;&nbsp;*5.3.1* | *ResNet-50* |
| &nbsp;&nbsp;&nbsp;*5.3.2* | *VGG-16* |
| &nbsp;&nbsp;&nbsp;*5.3.3* | *MobileNetV3-Large* |
| 5.4 | Granular Class-by-Class Analysis |
| &nbsp;&nbsp;&nbsp;*5.4.1* | *Weaponry (Firearms and Bladed Articles)* |
| &nbsp;&nbsp;&nbsp;*5.4.2* | *Illicit Narcotics and Pills* |
| &nbsp;&nbsp;&nbsp;*5.4.3* | *Alcohol and Pharmaceutical Bottles* |
| 5.5 | The CPU Inference Latency Tradeoff |
| &nbsp;&nbsp;&nbsp;*5.5.1* | *Big O Asymptotic Computational Complexity* |
| 5.6 | The Semantic Safety Net: OCR Validation |
| &nbsp;&nbsp;&nbsp;*5.6.1* | *Granular Case Study: The "Codeine" Override* |
| 5.7 | Summary |
| | |
| **Chapter 6** | **Conclusion** |
| 6.1 | Conclusion |
| &nbsp;&nbsp;&nbsp;*6.1.1* | *The Socioeconomic Impact of Rapid Triage* |
| 6.2 | Future Work |
| &nbsp;&nbsp;&nbsp;*6.2.1* | *Edge-Device and Mobile Deployment* |
| &nbsp;&nbsp;&nbsp;*6.2.2* | *Federated Learning for Cross-Jurisdictional Intelligence* |
| &nbsp;&nbsp;&nbsp;*6.2.3* | *Advancements in Semantic Parsing* |
| &nbsp;&nbsp;&nbsp;*6.2.4* | *Ethical Liability and Automation Bias* |
| &nbsp;&nbsp;&nbsp;*6.2.5* | *The Environmental Carbon Footprint of Forensic AI* |
| &nbsp;&nbsp;&nbsp;*6.2.6* | *Integration with Blockchain for Immutable Chain of Custody* |
| &nbsp;&nbsp;&nbsp;*6.2.7* | *Policy and Legal Standardization* |
| &nbsp;&nbsp;&nbsp;*6.2.8* | *Final Concluding Remarks* |
| 6.3 | References |

---

# List of Figures

| Figure | Description | Chapter |
| :--- | :--- | :--- |
| **Figure 1.1** | Conceptual Framework and Problem Domain of the Hybrid Digital Forensic Triage System | Chapter 1 |
| **Figure 3.1** | Architectural Flowchart of the Experimental Design Methodology | Chapter 3 |
| **Figure 3.2** | Dataset Distribution by Evidence Category across Training and Validation Splits | Chapter 3 |
| **Figure 4.1** | Operational Implementation Flowchart and Real-Time Decision Logic of the Forensic Triage Engine | Chapter 4 |
| **Figure 5.1** | Confusion Matrix of Classical Support Vector Machine (SVM RBF) | Chapter 5 |
| **Figure 5.2** | Multi-class Receiver Operating Characteristic (ROC) Curves for Classical SVM | Chapter 5 |
| **Figure 5.3** | Confusion Matrix of Classical Random Forest Ensemble | Chapter 5 |
| **Figure 5.4** | Multi-class Receiver Operating Characteristic (ROC) Curves for Random Forest | Chapter 5 |
| **Figure 5.5** | Confusion Matrix of Classical K-Nearest Neighbors ($k=5$) Classifier | Chapter 5 |
| **Figure 5.6** | Multi-class Receiver Operating Characteristic (ROC) Curves for KNN Classifier | Chapter 5 |
| **Figure 5.7** | Confusion Matrix of Fine-Tuned ResNet-50 Baseline | Chapter 5 |
| **Figure 5.8** | Confusion Matrix of Fine-Tuned VGG-16 Baseline | Chapter 5 |
| **Figure 5.9** | Confusion Matrix of Fine-Tuned MobileNetV3-Large Baseline | Chapter 5 |
| **Figure 5.10** | Quantitative CPU Inference Latency Benchmark and Projected Large-Scale Triage Processing Times | Chapter 5 |
| **Figure 5.11** | Granular Forensic Case Study: The 'Codeine' Semantic OCR Override on Structurally Ambiguous Evidence | Chapter 5 |

---

# List of Tables

| Table | Description | Chapter |
| :--- | :--- | :--- |
| **Table 2.1** | Comparative Critical Synthesis of Digital Forensic Evidence Triage Paradigms | Chapter 2 |

---

# Abstract

Digital forensic investigators face an escalating data crisis, characterized by overwhelming volumes of seized digital evidence. While deep learning offers high accuracy for automated triage, its prohibitive hardware requirements and "black-box" legal opacity render it largely unusable for frontline field units equipped with standard CPU-bound hardware. This dissertation engineers and evaluates a highly pragmatic, hybrid triage pipeline that synthesizes the raw computational speed of classical computer vision with the semantic intelligence of Optical Character Recognition (OCR). By extracting deterministic 4292-dimensional structural (HOG) and color (HSV) features, the classical Support Vector Machine (SVM) achieved an accuracy of 88.4% with an inference latency of just ~96.5ms on standard CPU hardware—over 3× faster than a ResNet-50 baseline (~294.2ms). To resolve inherent classical visual biases (e.g., misclassifying medicine bottles as alcohol), the system integrates an OCR safety net, achieving legal interpretability and robust performance. This research demonstrates that hybrid classical pipelines offer unmatched raw inference speed and ethical transparency, making them the superior choice for scalable, resource-constrained forensic deployment.

---

# Declaration

No part of this project has been submitted in support of an application for any other degree or qualification at this or any other institute of learning. Apart from those parts of the project containing citations to the work of others, this project is my own unaided work. It has been undertaken in accordance with the University research ethics standards, by the terms of permit number 2026-92076-70036 (EthOS Project ID: 92076).

Signed  
____________________________  
Alston Darren Pereira  
Student ID: 24850898

---

# Acknowledgements

I would like to express my sincere gratitude to my supervisor, Dr. Alex Akinbi, for his invaluable guidance, patience, and continuous support throughout this research. His expertise was instrumental in shaping the methodology and direction of this dissertation. 

I also extend my thanks to the Department of Computing and Mathematics at Manchester Metropolitan University for providing the necessary resources to conduct this study. 

Finally, I am deeply grateful to my family and friends for their unwavering encouragement during my academic journey.

---

# Abbreviations

| Abbreviation | Meaning |
| :--- | :--- |
| ACPO | Association of Chief Police Officers |
| Adam | Adaptive Moment Estimation |
| API | Application Programming Interface |
| AUC | Area Under the Curve |
| BGR | Blue, Green, Red |
| CLIP | Contrastive Language-Image Pre-training |
| CNN | Convolutional Neural Network |
| CPU | Central Processing Unit |
| CRAFT | Character Region Awareness for Text Detection |
| CRNN | Convolutional Recurrent Neural Network |
| CUDA | Compute Unified Device Architecture |
| EXIF | Exchangeable Image File Format |
| FGSM | Fast Gradient Sign Method |
| FN | False Negative |
| FP | False Positive |
| GDPR | General Data Protection Regulation |
| GPU | Graphics Processing Unit |
| HOG | Histogram of Oriented Gradients |
| HSV | Hue, Saturation, Value |
| JSON | JavaScript Object Notation |
| KKT | Karush-Kuhn-Tucker |
| KNN | K-Nearest Neighbors |
| LSTM | Long Short-Term Memory |
| MD5 | Message Digest 5 |
| NPCC | National Police Chiefs' Council |
| NSRL | National Software Reference Library |
| OCR | Optical Character Recognition |
| OOD | Out-of-Distribution |
| PCA | Principal Component Analysis |
| RBF | Radial Basis Function |
| ReLU | Rectified Linear Unit |
| ResNet | Residual Network |
| RF | Random Forest |
| RGB | Red, Green, Blue |
| ROC | Receiver Operating Characteristic |
| SGD | Stochastic Gradient Descent |
| SHA-1 | Secure Hash Algorithm 1 |
| SIFT | Scale-Invariant Feature Transform |
| SURF | Speeded-Up Robust Features |
| SVM | Support Vector Machine |
| TN | True Negative |
| TP | True Positive |
| VGG | Visual Geometry Group |

