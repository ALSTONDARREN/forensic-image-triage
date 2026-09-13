import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc_path = 'MSc_Dissertation_Draft.docx'
doc = docx.Document(doc_path)

# P0: Title
doc.paragraphs[0].text = "IMAGE CLASSIFICATION USING MACHINE LEARNING FOR DIGITAL FORENSIC INVESTIGATIONS"
doc.paragraphs[0].runs[0].font.bold = True
doc.paragraphs[0].runs[0].font.size = Pt(16)
doc.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

# P5: Year
doc.paragraphs[5].text = "2026"
doc.paragraphs[5].alignment = WD_ALIGN_PARAGRAPH.CENTER

# P7: Author & Student Details
doc.paragraphs[7].text = "Alston Darren Pereira (Student ID: 24850898)\nSupervisor: Dr. Alex Akinbi"
doc.paragraphs[7].alignment = WD_ALIGN_PARAGRAPH.CENTER

# P11-13: List of Tables & List of Figures
doc.paragraphs[11].text = "List of Tables"
doc.paragraphs[11].runs[0].font.bold = True

doc.paragraphs[12].text = "\tTable 2.1\tComparative Critical Synthesis of Digital Forensic Evidence Triage Paradigms"

# Replace P13 with List of Figures heading and list
doc.paragraphs[13].text = "List of Figures"
doc.paragraphs[13].runs[0].font.bold = True

figures_list = [
    ("\tFigure 1.1", "Conceptual Framework and Problem Domain of the Hybrid Digital Forensic Triage System"),
    ("\tFigure 3.1", "Architectural Flowchart of the Experimental Design Methodology"),
    ("\tFigure 3.2", "Dataset Distribution by Evidence Category across Training and Validation Splits"),
    ("\tFigure 4.1", "Operational Implementation Flowchart and Real-Time Decision Logic of the Forensic Triage Engine"),
    ("\tFigure 5.1", "Confusion Matrix of Classical Support Vector Machine (SVM RBF)"),
    ("\tFigure 5.2", "Multi-class Receiver Operating Characteristic (ROC) Curves for Classical SVM"),
    ("\tFigure 5.3", "Confusion Matrix of Classical Random Forest Ensemble"),
    ("\tFigure 5.4", "Multi-class Receiver Operating Characteristic (ROC) Curves for Random Forest"),
    ("\tFigure 5.5", "Confusion Matrix of Classical K-Nearest Neighbors (k=5) Classifier"),
    ("\tFigure 5.6", "Multi-class Receiver Operating Characteristic (ROC) Curves for KNN Classifier"),
    ("\tFigure 5.7", "Confusion Matrix of Fine-Tuned ResNet-50 Baseline"),
    ("\tFigure 5.8", "Confusion Matrix of Fine-Tuned VGG-16 Baseline"),
    ("\tFigure 5.9", "Confusion Matrix of Fine-Tuned MobileNetV3-Large Baseline"),
    ("\tFigure 5.10", "Quantitative CPU Inference Latency Benchmark and Projected Large-Scale Triage Processing Times"),
    ("\tFigure 5.11", "Granular Forensic Case Study: The 'Codeine' Semantic OCR Override on Structurally Ambiguous Evidence")
]

# Insert figures after P13
ref_p = doc.paragraphs[13]
for fig_id, fig_title in reversed(figures_list):
    new_p = ref_p.insert_paragraph_before(f"{fig_id}\t{fig_title}")

# Find updated indices of subsequent sections
for idx, p in enumerate(doc.paragraphs[:40]):
    if p.text.strip() == "Abstract":
        abstract_idx = idx
    elif p.text.strip() == "Declaration":
        declaration_idx = idx
    elif p.text.strip() == "Acknowledgements":
        ack_idx = idx
    elif p.text.strip() == "Abbreviations":
        abbrev_idx = idx

print(f"Indices: Abstract={abstract_idx}, Declaration={declaration_idx}, Ack={ack_idx}, Abbrev={abbrev_idx}")

# Update Abstract
abstract_text = (
    "Digital forensic investigators face an escalating data crisis, characterized by overwhelming volumes of seized digital evidence. "
    "While deep learning offers high accuracy for automated triage, its prohibitive hardware requirements and 'black-box' legal opacity "
    "render it largely unusable for frontline field units equipped with standard CPU-bound hardware. This dissertation engineers and evaluates "
    "a highly pragmatic, hybrid triage pipeline that synthesizes the raw computational speed of classical computer vision with the semantic "
    "intelligence of Optical Character Recognition (OCR). By extracting deterministic 4292-dimensional structural (HOG) and color (HSV) "
    "features, the classical Support Vector Machine (SVM) achieved an accuracy of 88.4% with an inference latency of just ~96.5ms on standard CPU "
    "hardware—over 3× faster than a ResNet-50 baseline (~294.2ms). To resolve inherent classical visual biases (e.g., misclassifying medicine bottles "
    "as alcohol), the system integrates an OCR safety net, achieving legal interpretability and robust performance. This research demonstrates that "
    "hybrid classical pipelines offer unmatched raw inference speed and ethical transparency, making them the superior choice for scalable, resource-constrained forensic deployment."
)
doc.paragraphs[abstract_idx + 1].text = abstract_text

# Update Declaration
decl_text = (
    "No part of this project has been submitted in support of an application for any other degree or qualification at this or any other institute of learning. "
    "Apart from those parts of the project containing citations to the work of others, this project is my own unaided work. "
    "It has been undertaken in accordance with the University research ethics standards, by the terms of permit number 2026-92076-70036 (EthOS Project ID: 92076).\n\n"
    "Signed: Alston Darren Pereira\nStudent ID: 24850898\nDate: September 2026"
)
doc.paragraphs[declaration_idx + 1].text = decl_text

# Update Acknowledgements
ack_text = (
    "I would like to express my sincere gratitude to my supervisor, Dr. Alex Akinbi, for his invaluable guidance, patience, and continuous support "
    "throughout this research. His expertise was instrumental in shaping the methodology and direction of this dissertation.\n\n"
    "I also extend my thanks to the Department of Computing and Mathematics at Manchester Metropolitan University for providing the necessary resources to conduct this study.\n\n"
    "Finally, I am deeply grateful to my family and friends for their unwavering encouragement during my academic journey."
)
doc.paragraphs[ack_idx + 1].text = ack_text

# Update Abbreviations
abbrevs = [
    ("ACPO", "Association of Chief Police Officers"),
    ("AUC", "Area Under the Curve"),
    ("CLIP", "Contrastive Language-Image Pre-training"),
    ("CNN", "Convolutional Neural Network"),
    ("CPU", "Central Processing Unit"),
    ("FGSM", "Fast Gradient Sign Method"),
    ("GPU", "Graphics Processing Unit"),
    ("HOG", "Histogram of Oriented Gradients"),
    ("HSV", "Hue, Saturation, Value"),
    ("KNN", "K-Nearest Neighbors"),
    ("MD5", "Message Digest 5"),
    ("NSRL", "National Software Reference Library"),
    ("OCR", "Optical Character Recognition"),
    ("PCA", "Principal Component Analysis"),
    ("ReLU", "Rectified Linear Unit"),
    ("RF", "Random Forest"),
    ("ROC", "Receiver Operating Characteristic"),
    ("SHA-1", "Secure Hash Algorithm 1"),
    ("SIFT", "Scale-Invariant Feature Transform"),
    ("SURF", "Speeded-Up Robust Features"),
    ("SVM", "Support Vector Machine")
]

# Clear existing sample abbreviations (PCA, LTA)
doc.paragraphs[abbrev_idx + 1].text = f"\t{abbrevs[0][0]}\t{abbrevs[0][1]}"
if len(doc.paragraphs) > abbrev_idx + 2 and "LTA" in doc.paragraphs[abbrev_idx + 2].text:
    doc.paragraphs[abbrev_idx + 2].text = f"\t{abbrevs[1][0]}\t{abbrevs[1][1]}"
    start_abbrev = 2
else:
    start_abbrev = 1

ref_abbrev = doc.paragraphs[abbrev_idx + 1 + (start_abbrev - 1)]
for abbr, desc in reversed(abbrevs[start_abbrev:]):
    ref_abbrev.insert_paragraph_before(f"\t{abbr}\t{desc}")

doc.save(doc_path)
print("Preamble successfully updated in MSc_Dissertation_Draft.docx!")
