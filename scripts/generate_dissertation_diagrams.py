import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle
import numpy as np
import os

VISUALS_DIR = r"C:\Users\perei\Documents\thesis\visuals"
os.makedirs(VISUALS_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. CHAPTER 1: Figure 1.1 Conceptual Framework & Problem Domain
# -------------------------------------------------------------
def generate_fig1_1():
    print("Generating Figure 1.1: Chapter 1 Conceptual Framework...")
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    # Title Banner
    title_box = FancyBboxPatch((0.5, 8.1), 14, 0.7, boxstyle="round,pad=0.1", 
                               ec="#1E293B", fc="#1E293B")
    ax.add_patch(title_box)
    ax.text(7.5, 8.45, "Figure 1.1: Digital Forensic Evidence Crisis & Proposed Hybrid Triage Architecture", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='white')

    # Column 1: Evidence Influx & Crime Scene (Left)
    c1 = FancyBboxPatch((0.5, 1.2), 3.2, 6.5, boxstyle="round,pad=0.15", 
                        ec="#3B82F6", fc="#EFF6FF", lw=2)
    ax.add_patch(c1)
    ax.text(2.1, 7.35, "1. SEIZED DIGITAL MEDIA", ha='center', va='center', 
            fontsize=11, fontweight='bold', color="#1E3A8A")
    
    devices = [
        ("Suspect Smartphones\n& Tablets (iOS / Android)", 6.4),
        ("High-Capacity Storage\n(NVMe / SSD / HDD)", 5.2),
        ("Cloud Cache & Encrypted\nMessaging Logs", 4.0),
        ("Unstructured Visual Deluge\n(100,000s of Images)", 2.7)
    ]
    for text, y in devices:
        b = FancyBboxPatch((0.7, y-0.4), 2.8, 0.8, boxstyle="round,pad=0.08", 
                           ec="#93C5FD", fc="#FFFFFF", lw=1.2)
        ax.add_patch(b)
        ax.text(2.1, y, text, ha='center', va='center', fontsize=8.5, color="#1E293B")

    # Column 2: The Forensic Triage Dilemma (Middle-Left)
    c2 = FancyBboxPatch((4.1, 1.2), 3.3, 6.5, boxstyle="round,pad=0.15", 
                        ec="#EF4444", fc="#FEF2F2", lw=2)
    ax.add_patch(c2)
    ax.text(5.75, 7.35, "2. OPERATIONAL BOTTLENECKS", ha='center', va='center', 
            fontsize=11, fontweight='bold', color="#991B1B")

    bottlenecks = [
        ("Cryptographic Hash Fragility", 
         "MD5/SHA-1 defeated by 1-pixel\nalteration, cropping, or compression\n(Avalanche Effect & Collisions)", 6.1),
        ("Heavy Deep Learning Bottlenecks", 
         "Requires costly GPU infrastructure;\nCPU inference causes 40+ hr delays;\n'Black-Box' opacity fails Daubert test", 4.3),
        ("Investigator Cognitive Trauma", 
         "Manual inspection of terabytes leads\nto human fatigue, backlogs & errors\n(e.g., R v Allan trial collapse)", 2.4)
    ]
    for title, desc, y in bottlenecks:
        b = FancyBboxPatch((4.3, y-0.65), 2.9, 1.3, boxstyle="round,pad=0.08", 
                           ec="#FCA5A5", fc="#FFFFFF", lw=1.2)
        ax.add_patch(b)
        ax.text(5.75, y+0.35, title, ha='center', va='center', fontsize=9, fontweight='bold', color="#991B1B")
        ax.text(5.75, y-0.15, desc, ha='center', va='center', fontsize=7.5, color="#334155")

    # Column 3: Proposed Hybrid Triage Solution (Middle-Right)
    c3 = FancyBboxPatch((7.8, 1.2), 3.4, 6.5, boxstyle="round,pad=0.15", 
                        ec="#10B981", fc="#ECFDF5", lw=2)
    ax.add_patch(c3)
    ax.text(9.5, 7.35, "3. PROPOSED HYBRID ENGINE", ha='center', va='center', 
            fontsize=11, fontweight='bold', color="#065F46")

    solutions = [
        ("Deterministic OpenCV Extraction", 
         "HSV Color Bins (512D) +\nHOG Structural Edges (3780D)\n-> 4292D Linear Scaled Vector", 6.1),
        ("Standard CPU Classification", 
         "SVM (RBF Kernel) & Random Forest\nFast inference (<100ms per image)\nMathematically verifiable weights", 4.4),
        ("Semantic OCR Safety Net", 
         "CRAFT & CRNN text recognition\nextracts pharmaceutical/weapon text\nto override visual misclassifications", 2.6)
    ]
    for title, desc, y in solutions:
        b = FancyBboxPatch((8.0, y-0.6), 3.0, 1.25, boxstyle="round,pad=0.08", 
                           ec="#6EE7B7", fc="#FFFFFF", lw=1.2)
        ax.add_patch(b)
        ax.text(9.5, y+0.35, title, ha='center', va='center', fontsize=9, fontweight='bold', color="#065F46")
        ax.text(9.5, y-0.15, desc, ha='center', va='center', fontsize=7.5, color="#334155")

    # Column 4: Forensic Outcomes & Deliverables (Right)
    c4 = FancyBboxPatch((11.6, 1.2), 2.9, 6.5, boxstyle="round,pad=0.15", 
                        ec="#8B5CF6", fc="#F5F3FF", lw=2)
    ax.add_patch(c4)
    ax.text(13.05, 7.35, "4. INVESTIGATIVE IMPACT", ha='center', va='center', 
            fontsize=11, fontweight='bold', color="#5B21B6")

    impacts = [
        ("Prioritized Contraband", "Rapid isolation of Alcohol,\nIllicit Drugs, & Weapons", 6.2),
        ("Massive Speedup", "Overnight 500k-image triage\n(~13.4 hrs vs 40.8 hrs ResNet)", 4.8),
        ("OOD Image Filtering", "Drops benign pets & scenery\nvia confidence & CLIP trap", 3.4),
        ("Legal Admissibility", "Adheres to ACPO Principle 1\n& Daubert explainability", 2.0)
    ]
    for title, desc, y in impacts:
        b = FancyBboxPatch((11.8, y-0.45), 2.5, 0.95, boxstyle="round,pad=0.08", 
                           ec="#C4B5FD", fc="#FFFFFF", lw=1.2)
        ax.add_patch(b)
        ax.text(13.05, y+0.18, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color="#5B21B6")
        ax.text(13.05, y-0.18, desc, ha='center', va='center', fontsize=7.2, color="#334155")

    # Connecting Flow Arrows
    arrow_kw = dict(arrowstyle="simple,head_width=0.8,head_length=0.8", color="#64748B", lw=1.5)
    ax.annotate("", xy=(4.1, 4.45), xytext=(3.7, 4.45), arrowprops=arrow_kw)
    ax.annotate("", xy=(7.8, 4.45), xytext=(7.4, 4.45), arrowprops=arrow_kw)
    ax.annotate("", xy=(11.6, 4.45), xytext=(11.2, 4.45), arrowprops=arrow_kw)

    # Subtitle note at bottom
    ax.text(7.5, 0.55, "Conceptual overview of the research dilemma addressed in Chapter 1: Overcoming hash fragility and deep learning latency through a deterministic hybrid forensic framework.",
            ha='center', va='center', fontsize=8.5, style='italic', color="#475569")

    plt.tight_layout()
    save_path = os.path.join(VISUALS_DIR, "fig1_1_forensic_problem_framework.png")
    plt.savefig(save_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Saved {save_path}")

# -------------------------------------------------------------
# 2. CHAPTER 2: Figure 2.1 Literature Review Summary Table (Image)
# -------------------------------------------------------------
def generate_fig2_1_table():
    print("Generating Figure 2.1: Chapter 2 Literature Review Summary Table (Image)...")
    fig, ax = plt.subplots(figsize=(16, 8.5), dpi=300)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Table Header and Row Data
    columns = [
        "Triage Paradigm", 
        "Underlying Feature Space", 
        "CPU Inference\nLatency", 
        "Hardware\nRequirements", 
        "Resistance to\nMinor Edits", 
        "FGSM Adversarial\nRobustness", 
        "Daubert Legal\nExplainability", 
        "Semantic Text\nReasoning", 
        "Primary Operational\nLimitation"
    ]

    rows = [
        [
            "Cryptographic Hashing\n(MD5 / SHA-1)", 
            "Deterministic bitwise\nalphanumeric digest", 
            "< 1 ms\n(Instantaneous)", 
            "Ultra-Low\n(Standard CPU)", 
            "Extremely Fragile\n(Avalanche Effect)", 
            "N/A\n(Bit-exact match)", 
            "High for integrity;\nFails for search", 
            "None\n(Zero semantic awareness)", 
            "1-pixel modification completely\ninvalidates database match"
        ],
        [
            "Perceptual Hashing\n(pHash / dHash)", 
            "Low-frequency DCT\ncoefficient gradients", 
            "~ 5 - 15 ms", 
            "Low\n(Standard CPU)", 
            "Moderate\n(Tolerates compression)", 
            "Moderate\n(Susceptible to noise)", 
            "Moderate\n(Heuristic thresholds)", 
            "None\n(No textual semantics)", 
            "High false-positive rate on\nsimilar background textures"
        ],
        [
            "Deep CNNs\n(ResNet-50 / VGG-16)", 
            "Deep hierarchical non-linear\nlatent representations", 
            "294 - 512 ms\n(CPU bottleneck)", 
            "Prohibitive\n(Requires CUDA GPU)", 
            "High\n(Pixel-invariant)", 
            "Vulnerable\n(Susceptible to FGSM)", 
            "Very Low\n('Black-Box' opacity)", 
            "Implicit / Weak\n(Visual features only)", 
            "Skyrocketing CPU latency\n(~40-71 hrs per 500k files); opaque"
        ],
        [
            "Lightweight Mobile DL\n(MobileNetV3-Large)", 
            "Depthwise separable\nconvolutions", 
            "~ 130.8 ms", 
            "Moderate\n(Optimized for CPU)", 
            "High\n(Pixel-invariant)", 
            "Vulnerable\n(Gradient-based noise)", 
            "Low\n(Latent parameter opacity)", 
            "Implicit / Weak\n(Visual features only)", 
            "Still lacks explicit semantic\ncontext for medicine vs alcohol"
        ],
        [
            "Classical Computer Vision\n(OpenCV HOG + HSV)", 
            "3D HSV Color Bins (512D) +\nHOG Gradients (3780D) = 4292D", 
            "~ 94 - 96 ms\n(Fast CPU triage)", 
            "Low\n(Standard Field Laptop)", 
            "High for rigid shapes;\nModerate for color", 
            "High\n(Rigid structural edges)", 
            "High\n(Deterministic equations)", 
            "None\n(Purely visual)", 
            "Visual ambiguity between structurally\nidentical objects (e.g., bottles)"
        ],
        [
            "Proposed Hybrid System\n(HOG/HSV + EasyOCR + OOD)", 
            "4292D Structural/Color Vector\n+ CRAFT/CRNN Semantic Tokens", 
            "~ 96 ms (Vision) +\n~ 110 ms (Selective OCR)", 
            "Optimized for Standard\nForensic Workstation", 
            "High\n(Dual visual-semantic)", 
            "High\n(Edge + Lexicon filters)", 
            "High\n(Auditable decision rules)", 
            "Explicit & Deterministic\n(Prescription / Weapon text)", 
            "Requires visible legible typography\nfor semantic override execution"
        ]
    ]

    # Render Table
    table = ax.table(
        cellText=rows, 
        colLabels=columns, 
        cellLoc='center', 
        loc='center',
        colWidths=[0.14, 0.14, 0.10, 0.11, 0.11, 0.10, 0.10, 0.10, 0.14]
    )

    table.auto_set_font_size(False)
    table.set_fontsize(7.8)
    table.scale(1.0, 2.2)

    # Style header
    for (row_idx, col_idx), cell in table.get_celld().items():
        cell.set_edgecolor('#CBD5E1')
        cell.set_linewidth(0.8)
        if row_idx == 0:
            cell.set_facecolor('#1E293B')
            cell.set_text_props(color='white', fontweight='bold', fontsize=8.2)
            cell.set_height(0.08)
        elif row_idx % 2 == 1:
            cell.set_facecolor('#F8FAFC')
        else:
            cell.set_facecolor('#FFFFFF')
            
        # Highlight proposed hybrid row
        if row_idx == 6:
            cell.set_facecolor('#ECFDF5')
            cell.set_text_props(fontweight='bold', color='#065F46')
            cell.set_edgecolor('#10B981')
            cell.set_linewidth(1.2)

    # Add Table Title & Caption
    plt.suptitle("Table 2.1: Comparative Critical Synthesis of Digital Forensic Evidence Triage Paradigms", 
                 fontsize=13, fontweight='bold', y=0.96, color='#1E293B')
    plt.figtext(0.5, 0.03, "Synthesis of modern digital evidence triage paradigms evaluated in Chapter 2, contrasting operational latency, legal admissibility, and semantic capabilities.", 
                 ha='center', fontsize=8.5, style='italic', color='#475569')

    plt.subplots_adjust(top=0.90, bottom=0.08, left=0.02, right=0.98)
    save_path = os.path.join(VISUALS_DIR, "fig2_1_literature_review_table.png")
    plt.savefig(save_path, dpi=300, facecolor='#FFFFFF', edgecolor='none')
    plt.close()
    print(f"Saved {save_path}")

# -------------------------------------------------------------
# 3. CHAPTER 3: Figure 3.1 Design Process Flowchart
# -------------------------------------------------------------
def generate_fig3_1_flowchart():
    print("Generating Figure 3.1: Chapter 3 Experimental Design Flowchart...")
    fig, ax = plt.subplots(figsize=(15, 10), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    # Title
    title_box = FancyBboxPatch((0.5, 9.1), 14, 0.65, boxstyle="round,pad=0.1", ec="#1E293B", fc="#1E293B")
    ax.add_patch(title_box)
    ax.text(7.5, 9.42, "Figure 3.1: Architectural Flowchart of the Experimental Design Methodology", 
            ha='center', va='center', fontsize=13.5, fontweight='bold', color='white')

    # Phase 1: Data Acquisition & Normalization
    p1 = FancyBboxPatch((0.6, 6.7), 4.2, 2.0, boxstyle="round,pad=0.12", ec="#3B82F6", fc="#EFF6FF", lw=1.8)
    ax.add_patch(p1)
    ax.text(2.7, 8.4, "PHASE 1: DATASET CURATION", ha='center', fontsize=10.5, fontweight='bold', color="#1E3A8A")
    ax.text(2.7, 7.8, "- Multi-Source Web Scraping (BeautifulSoup/APIs)\n- 3 Forensic Classes: Alcohol, Drugs, Weapons\n- Total Raw Corpus: 4,951 Authentic Images", 
            ha='center', fontsize=8.2, color="#1E293B")
    ax.text(2.7, 7.05, "Corrupt File Purge + cv2 Interpolation Resizing", 
            ha='center', fontsize=8, style='italic', color="#2563EB")

    # Phase 2: Stratified Partitioning
    p2 = FancyBboxPatch((5.4, 6.7), 4.2, 2.0, boxstyle="round,pad=0.12", ec="#0284C7", fc="#F0F9FF", lw=1.8)
    ax.add_patch(p2)
    ax.text(7.5, 8.4, "PHASE 2: STRATIFIED SPLIT", ha='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    ax.text(7.5, 7.7, "- 80% Training Split: 3,959 Images\n- 20% Validation Split: 992 Images\n- Stratified across all 3 classes", 
            ha='center', fontsize=8.2, color="#1E293B")
    ax.text(7.5, 7.05, "Preserves authentic forensic class imbalance", 
            ha='center', fontsize=8, style='italic', color="#0284C7")

    # Phase 3: Classical Feature Extraction Pipeline
    p3 = FancyBboxPatch((10.2, 6.7), 4.2, 2.0, boxstyle="round,pad=0.12", ec="#10B981", fc="#ECFDF5", lw=1.8)
    ax.add_patch(p3)
    ax.text(12.3, 8.4, "PHASE 3: FEATURE EXTRACTION", ha='center', fontsize=10.5, fontweight='bold', color="#065F46")
    ax.text(12.3, 7.7, "Dual-Stream OpenCV Feature Engineering:\n1. 3D HSV Color Histogram (512D)\n2. HOG Structural Gradients (3780D)", 
            ha='center', fontsize=8.2, color="#1E293B")
    ax.text(12.3, 7.05, "Result: 4,292-Dimensional Hybrid Vector", 
            ha='center', fontsize=8, fontweight='bold', color="#059669")

    # Arrows for Top Row
    arrow_kw = dict(arrowstyle="simple,head_width=0.7,head_length=0.7", color="#475569", lw=1.2)
    ax.annotate("", xy=(5.4, 7.7), xytext=(4.8, 7.7), arrowprops=arrow_kw)
    ax.annotate("", xy=(10.2, 7.7), xytext=(9.6, 7.7), arrowprops=arrow_kw)

    # Arrow Down to Middle Phase
    ax.annotate("", xy=(7.5, 5.8), xytext=(7.5, 6.4), arrowprops=arrow_kw)

    # Phase 4: Feature Normalization & Dimensionality Benchmark (Center)
    p4 = FancyBboxPatch((3.5, 4.3), 8.0, 1.5, boxstyle="round,pad=0.12", ec="#F59E0B", fc="#FFFBEB", lw=1.8)
    ax.add_patch(p4)
    ax.text(7.5, 5.4, "PHASE 4: NORMALIZATION & DIMENSIONALITY REDUCTION EVALUATION", 
            ha='center', fontsize=10, fontweight='bold', color="#B45309")
    ax.text(7.5, 4.75, "StandardScaler Z-Score Normalization | PCA Compression Benchmark (95% Variance Retention)\nFinding: PCA linear compression dilutes critical fine blade edges & pill color peaks -> Retain full 4,292D vector", 
            ha='center', fontsize=8.2, color="#334155")

    # Split Arrows Down to Models
    ax.annotate("", xy=(4.0, 3.5), xytext=(6.0, 4.3), arrowprops=arrow_kw)
    ax.annotate("", xy=(11.0, 3.5), xytext=(9.0, 4.3), arrowprops=arrow_kw)

    # Phase 5A: Classical Machine Learning Stream (Bottom-Left)
    p5a = FancyBboxPatch((0.6, 0.8), 6.5, 2.7, boxstyle="round,pad=0.12", ec="#8B5CF6", fc="#F5F3FF", lw=1.8)
    ax.add_patch(p5a)
    ax.text(3.85, 3.15, "STREAM A: DETERMINISTIC CLASSICAL CLASSIFIERS", 
            ha='center', fontsize=10, fontweight='bold', color="#6D28D9")
    
    classical_models = [
        ("Support Vector Machine (SVM)", "RBF Kernel, Dual Quadratic Programming (KKT)", 2.5),
        ("Random Forest (RF)", "100 Decision Trees, Gini Impurity / Shannon Entropy", 1.8),
        ("K-Nearest Neighbors (KNN)", "Instance-Based Spatial Classifier (k=5)", 1.1)
    ]
    for name, detail, y in classical_models:
        box = FancyBboxPatch((0.8, y-0.25), 6.1, 0.55, boxstyle="round,pad=0.06", ec="#DDD6FE", fc="#FFFFFF")
        ax.add_patch(box)
        ax.text(1.0, y, name + ":", fontsize=8, fontweight='bold', color="#5B21B6")
        ax.text(3.5, y, detail, fontsize=7.8, color="#334155")

    # Phase 5B: Deep Learning Baselines (Bottom-Right)
    p5b = FancyBboxPatch((7.9, 0.8), 6.5, 2.7, boxstyle="round,pad=0.12", ec="#EC4899", fc="#FDF2F8", lw=1.8)
    ax.add_patch(p5b)
    ax.text(11.15, 3.15, "STREAM B: DEEP LEARNING TRANSFER LEARNING BASELINES", 
            ha='center', fontsize=10, fontweight='bold', color="#BE185D")

    deep_models = [
        ("ResNet-50", "50-layer deep residual network with skip connections", 2.5),
        ("VGG-16", "138M parameter architecture (Max CPU hardware ceiling)", 1.8),
        ("MobileNetV3-Large", "Depthwise separable convolutions for edge efficiency", 1.1)
    ]
    for name, detail, y in deep_models:
        box = FancyBboxPatch((8.1, y-0.25), 6.1, 0.55, boxstyle="round,pad=0.06", ec="#FBCFE8", fc="#FFFFFF")
        ax.add_patch(box)
        ax.text(8.3, y, name + ":", fontsize=8, fontweight='bold', color="#9D174D")
        ax.text(10.5, y, detail, fontsize=7.8, color="#334155")

    # Footer
    ax.text(7.5, 0.35, "Methodological workflow in Chapter 3: End-to-end experimental architecture from raw evidence scraping to dual-stream comparative benchmarking.", 
            ha='center', fontsize=8.2, style='italic', color='#64748B')

    plt.tight_layout()
    save_path = os.path.join(VISUALS_DIR, "fig3_1_design_flowchart.png")
    plt.savefig(save_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Saved {save_path}")

# -------------------------------------------------------------
# 4. CHAPTER 4: Figure 4.1 Operational Implementation Flowchart
# -------------------------------------------------------------
def generate_fig4_1_implementation_flowchart():
    print("Generating Figure 4.1: Chapter 4 Implementation Runtime Flowchart...")
    fig, ax = plt.subplots(figsize=(15, 10.5), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10.5)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    # Title
    title_box = FancyBboxPatch((0.5, 9.6), 14, 0.65, boxstyle="round,pad=0.1", ec="#1E293B", fc="#1E293B")
    ax.add_patch(title_box)
    ax.text(7.5, 9.92, "Figure 4.1: Operational Implementation Flowchart and Real-Time Decision Logic", 
            ha='center', va='center', fontsize=13.5, fontweight='bold', color='white')

    # Step 1: Ingestion
    s1 = FancyBboxPatch((5.5, 8.5), 4.0, 0.8, boxstyle="round,pad=0.1", ec="#3B82F6", fc="#EFF6FF", lw=1.5)
    ax.add_patch(s1)
    ax.text(7.5, 8.9, "1. INGEST SEIZED IMAGE", ha='center', fontsize=9.5, fontweight='bold', color="#1E3A8A")
    ax.text(7.5, 8.65, "Standard digital forensic clone image stream", ha='center', fontsize=7.8, color="#334155")

    # Step 2: Dual Preprocessing
    s2 = FancyBboxPatch((5.0, 7.1), 5.0, 0.9, boxstyle="round,pad=0.1", ec="#0284C7", fc="#F0F9FF", lw=1.5)
    ax.add_patch(s2)
    ax.text(7.5, 7.6, "2. PROGRAMMATIC PREPROCESSING", ha='center', fontsize=9.5, fontweight='bold', color="#0369A1")
    ax.text(7.5, 7.3, "Parallel Resizing: 224x224 (Color/CNN) & 64x128 Grayscale (HOG)", ha='center', fontsize=7.8, color="#334155")

    # Step 3: Feature Extraction & Scaling
    s3 = FancyBboxPatch((4.5, 5.7), 6.0, 0.9, boxstyle="round,pad=0.1", ec="#10B981", fc="#ECFDF5", lw=1.5)
    ax.add_patch(s3)
    ax.text(7.5, 6.2, "3. OPENCV FEATURE EXTRACTION & SCALING", ha='center', fontsize=9.5, fontweight='bold', color="#065F46")
    ax.text(7.5, 5.9, "HSV Color (512D) + HOG Gradients (3780D) -> 4292D Vector -> StandardScaler", ha='center', fontsize=7.8, color="#334155")

    # Step 4: Primary ML Inference
    s4 = FancyBboxPatch((4.8, 4.4), 5.4, 0.8, boxstyle="round,pad=0.1", ec="#8B5CF6", fc="#F5F3FF", lw=1.5)
    ax.add_patch(s4)
    ax.text(7.5, 4.85, "4. PRIMARY CLASSIFICATION INFERENCE", ha='center', fontsize=9.5, fontweight='bold', color="#5B21B6")
    ax.text(7.5, 4.6, "SVM RBF Kernel -> Softmax Probabilities: P(Alcohol), P(Drugs), P(Weapons)", ha='center', fontsize=7.8, color="#334155")

    # Arrows for linear top flow
    arrow_kw = dict(arrowstyle="simple,head_width=0.6,head_length=0.6", color="#475569", lw=1.2)
    ax.annotate("", xy=(7.5, 8.0), xytext=(7.5, 8.5), arrowprops=arrow_kw)
    ax.annotate("", xy=(7.5, 6.6), xytext=(7.5, 7.1), arrowprops=arrow_kw)
    ax.annotate("", xy=(7.5, 5.2), xytext=(7.5, 5.7), arrowprops=arrow_kw)
    ax.annotate("", xy=(7.5, 3.9), xytext=(7.5, 4.4), arrowprops=arrow_kw)

    # Decision Diamond 1: Low Confidence OOD Check
    d1 = patches.Polygon([[7.5, 3.9], [9.3, 3.2], [7.5, 2.5], [5.7, 3.2]], 
                         closed=True, ec="#F59E0B", fc="#FFFBEB", lw=1.5)
    ax.add_patch(d1)
    ax.text(7.5, 3.3, "Max Confidence\n< 0.50 ?", ha='center', va='center', fontsize=8, fontweight='bold', color="#B45309")

    # Exclude Box (Left of D1)
    ex1 = FancyBboxPatch((0.8, 2.7), 3.4, 1.0, boxstyle="round,pad=0.1", ec="#EF4444", fc="#FEF2F2", lw=1.5)
    ax.add_patch(ex1)
    ax.text(2.5, 3.3, "EXCLUDED FROM TRIAGE", ha='center', fontsize=8.5, fontweight='bold', color="#DC2626")
    ax.text(2.5, 2.95, "Flagged: Out of Distribution (OOD)\nUncertain low-confidence artifact", ha='center', fontsize=7.2, color="#7F1D1D")

    # D1 YES arrow
    ax.annotate("YES", xy=(4.2, 3.2), xytext=(5.7, 3.2), arrowprops=arrow_kw, fontsize=8, fontweight='bold', color="#DC2626")

    # Decision Diamond 2 / Semantic OCR Safety Net (Below D1)
    ax.annotate("NO", xy=(7.5, 1.9), xytext=(7.5, 2.5), arrowprops=arrow_kw, fontsize=8, fontweight='bold', color="#059669")

    # Step 5: Hybrid Semantic OCR Safety Net
    s5 = FancyBboxPatch((4.0, 0.6), 7.0, 1.3, boxstyle="round,pad=0.1", ec="#0D9488", fc="#F0FDFA", lw=1.8)
    ax.add_patch(s5)
    ax.text(7.5, 1.6, "5. HYBRID SEMANTIC OCR SAFETY NET (EasyOCR)", ha='center', fontsize=9.5, fontweight='bold', color="#0F766E")
    ax.text(7.5, 1.25, "CRAFT Text Detector isolates label bounding boxes -> CRNN recognizes characters\nLexicon Check: Does image contain 'Rx', 'Codeine', 'Phosphate' on bottle classified as Alcohol?", ha='center', fontsize=7.8, color="#134E4A")
    ax.text(7.5, 0.85, "-> If Detected: Deterministic Hard Rule OVERRIDES visual class to 'Drugs' with 100% confidence", 
            ha='center', fontsize=8, fontweight='bold', color="#0D9488")

    # Step 6: Final Triage Evidence Dashboard (Right)
    s6 = FancyBboxPatch((11.5, 2.2), 3.0, 2.8, boxstyle="round,pad=0.1", ec="#10B981", fc="#ECFDF5", lw=1.8)
    ax.add_patch(s6)
    ax.text(13.0, 4.6, "6. FORENSIC AUDIT", ha='center', fontsize=9.5, fontweight='bold', color="#065F46")
    ax.text(13.0, 4.0, "Verified Contraband:\n- Alcohol / Drugs / Weapons\n- JSON Audit Manifest\n- Daubert-Compliant Trace\n- Latency: ~96.5ms CPU\n- ACPO Chain of Custody", 
            ha='center', fontsize=7.8, color="#064E3B")

    # Arrow from OCR to Final Audit
    ax.annotate("", xy=(12.0, 2.2), xytext=(11.0, 1.3), arrowprops=arrow_kw)

    # Secondary Arrow from CLIP / OOD trap
    clip_box = FancyBboxPatch((11.5, 6.0), 3.0, 1.5, boxstyle="round,pad=0.1", ec="#6366F1", fc="#EEF2FF", lw=1.5)
    ax.add_patch(clip_box)
    ax.text(13.0, 7.1, "CLIP Benign Trap", ha='center', fontsize=8.5, fontweight='bold', color="#4338CA")
    ax.text(13.0, 6.5, "Cosine similarity match\nto 'benign scenery/pets'\n-> Drops false alarms", ha='center', fontsize=7.2, color="#312E81")
    ax.annotate("", xy=(10.5, 6.7), xytext=(11.5, 6.7), arrowprops=dict(arrowstyle="simple,head_width=0.5,head_length=0.5", color="#6366F1", lw=1))

    # Caption
    ax.text(7.5, 0.15, "Operational triage pipeline documented in Chapter 4, showcasing feature scaling, inference, confidence gating, and the OCR semantic safety net.", 
            ha='center', fontsize=8, style='italic', color='#64748B')

    plt.tight_layout()
    save_path = os.path.join(VISUALS_DIR, "fig4_1_implementation_flowchart.png")
    plt.savefig(save_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Saved {save_path}")

# -------------------------------------------------------------
# 5. CHAPTER 5: Figure 5.10 CPU Latency & Projected Triage Benchmark
# -------------------------------------------------------------
def generate_fig5_10_latency_benchmark():
    print("Generating Figure 5.10: Chapter 5 Latency & Triage Time Benchmark...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    models = ['Random Forest\n(Classical)', 'SVM RBF\n(Classical)', 'MobileNetV3\n(Lightweight DL)', 'ResNet-50\n(Heavy DL)', 'VGG-16\n(Heavy DL)']
    latencies = [94.48, 96.52, 130.75, 294.22, 512.40]
    colors = ['#10B981', '#059669', '#3B82F6', '#EF4444', '#DC2626']

    # Panel 1: Milliseconds per Single Image
    bars1 = ax1.bar(models, latencies, color=colors, width=0.55, edgecolor='#1E293B', lw=1.2)
    ax1.set_ylabel('Inference Latency on CPU (Milliseconds)', fontsize=10, fontweight='bold')
    ax1.set_title('CPU Inference Latency per Single Image\n(Simulating Frontline Workstation)', fontsize=11, fontweight='bold', pad=12)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    ax1.set_ylim(0, 580)

    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 10, f"{yval:.1f} ms", 
                 ha='center', va='bottom', fontsize=8.5, fontweight='bold')

    # Panel 2: Total Time to Triage 500,000 Seized Images (in Hours)
    triage_hours = [(lat * 500000) / (1000 * 3600) for lat in latencies]
    bars2 = ax2.bar(models, triage_hours, color=colors, width=0.55, edgecolor='#1E293B', lw=1.2)
    ax2.set_ylabel('Projected Triage Duration (Hours)', fontsize=10, fontweight='bold')
    ax2.set_title('Projected Triage Duration for 500,000 Seized Images\n(Real-World Forensic Storage Drive)', fontsize=11, fontweight='bold', pad=12)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    ax2.set_ylim(0, 80)

    # Reference threshold lines (Overnight vs Multi-day)
    ax2.axhline(y=24, color='#F59E0B', linestyle=':', lw=1.5, label='24-Hour Threshold (1 Day)')
    ax2.legend(loc='upper left', fontsize=8.5)

    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f"{yval:.1f} hrs\n({yval/24:.1f} days)", 
                 ha='center', va='bottom', fontsize=8.2, fontweight='bold')

    plt.suptitle("Figure 5.10: Quantitative CPU Inference Latency Benchmark and Projected Large-Scale Triage Processing Times", 
                 fontsize=12.5, fontweight='bold', y=0.98, color='#1E293B')
    plt.tight_layout()
    plt.subplots_adjust(top=0.88, bottom=0.15)
    
    save_path = os.path.join(VISUALS_DIR, "fig5_10_cpu_latency_benchmark.png")
    plt.savefig(save_path, dpi=300, facecolor='#FFFFFF', edgecolor='none')
    plt.close()
    print(f"Saved {save_path}")

# -------------------------------------------------------------
# 6. CHAPTER 5: Figure 5.11 Codeine Semantic OCR Case Study Infographic
# -------------------------------------------------------------
def generate_fig5_11_case_study():
    print("Generating Figure 5.11: Chapter 5 Codeine Semantic OCR Case Study...")
    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    # Title Banner
    title_box = FancyBboxPatch((0.5, 6.1), 13, 0.65, boxstyle="round,pad=0.1", ec="#1E293B", fc="#1E293B")
    ax.add_patch(title_box)
    ax.text(7.0, 6.42, "Figure 5.11: Granular Forensic Case Study: The 'Codeine' Semantic OCR Override", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='white')

    # Panel 1: Input Evidence Image Simulation (Amber Prescription Bottle)
    p1 = FancyBboxPatch((0.6, 1.2), 3.6, 4.5, boxstyle="round,pad=0.15", ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(p1)
    ax.text(2.4, 5.35, "1. SEIZED EVIDENCE IMAGE", ha='center', fontsize=10, fontweight='bold', color="#92400E")
    
    # Graphic illustration of medicine bottle
    bottle_body = FancyBboxPatch((1.6, 2.3), 1.6, 2.2, boxstyle="round,pad=0.05", ec="#78350F", fc="#B45309")
    bottle_cap = FancyBboxPatch((2.0, 4.5), 0.8, 0.5, boxstyle="round,pad=0.03", ec="#1E293B", fc="#FFFFFF")
    label = FancyBboxPatch((1.75, 2.7), 1.3, 1.4, boxstyle="round,pad=0.03", ec="#DC2626", fc="#FFFFFF", lw=1.2)
    ax.add_patch(bottle_body)
    ax.add_patch(bottle_cap)
    ax.add_patch(label)
    ax.text(2.4, 3.7, "RX ONLY", ha='center', fontsize=6.5, fontweight='bold', color="#DC2626")
    ax.text(2.4, 3.3, "CODEINE", ha='center', fontsize=7, fontweight='bold', color="#1E293B")
    ax.text(2.4, 2.9, "PHOSPHATE", ha='center', fontsize=5.5, color="#1E293B")
    ax.text(2.4, 1.7, "Amber Glass Cylinder\nAmbiguous Foreground Object", ha='center', fontsize=7.5, color="#78350F")

    # Panel 2: Classical Visual Model Failure
    p2 = FancyBboxPatch((4.7, 1.2), 4.0, 4.5, boxstyle="round,pad=0.15", ec="#EF4444", fc="#FEF2F2", lw=1.8)
    ax.add_patch(p2)
    ax.text(6.7, 5.35, "2. OPENCV VISUAL STREAM", ha='center', fontsize=10, fontweight='bold', color="#991B1B")
    
    vis_details = [
        ("HSV Color Analysis", "High amber/brown pigment spike in Hue bins"),
        ("HOG Structural Edge", "Vertical cylindrical gradient contour"),
        ("SVM Classification", "P(Alcohol) = 92.4%\nP(Drugs) = 6.1%\nP(Weapons) = 1.5%"),
        ("CLASSIFIER RESULT", "FLAGGED AS 'ALCOHOL' (False Negative)")
    ]
    y_pos = 4.4
    for title, desc in vis_details:
        b = FancyBboxPatch((4.9, y_pos-0.28), 3.6, 0.65, boxstyle="round,pad=0.05", ec="#FCA5A5", fc="#FFFFFF")
        ax.add_patch(b)
        ax.text(5.1, y_pos+0.08, title, fontsize=7.8, fontweight='bold', color="#991B1B")
        ax.text(5.1, y_pos-0.15, desc, fontsize=7, color="#334155")
        y_pos -= 0.85

    # Panel 3: Semantic OCR Safety Net Override
    p3 = FancyBboxPatch((9.2, 1.2), 4.2, 4.5, boxstyle="round,pad=0.15", ec="#10B981", fc="#ECFDF5", lw=2.0)
    ax.add_patch(p3)
    ax.text(11.3, 5.35, "3. SEMANTIC SAFETY NET", ha='center', fontsize=10, fontweight='bold', color="#065F46")

    ocr_details = [
        ("CRAFT Text Detector", "Detects rectangular text region on bottle label"),
        ("CRNN Text Recognition", "Extracted text tokens:\n'RX ONLY: CODEINE PHOSPHATE'"),
        ("Forensic Lexicon Rule", "Matched Keyword: ['RX', 'CODEINE']\nMandates Class: 'DRUGS'"),
        ("PROGRAMMATIC OVERRIDE", "FINAL TRIAGE: 'DRUGS' (100% Correct)")
    ]
    y_pos = 4.4
    for title, desc in ocr_details:
        b = FancyBboxPatch((9.4, y_pos-0.28), 3.8, 0.65, boxstyle="round,pad=0.05", ec="#6EE7B7", fc="#FFFFFF")
        ax.add_patch(b)
        ax.text(9.6, y_pos+0.08, title, fontsize=7.8, fontweight='bold', color="#065F46")
        ax.text(9.6, y_pos-0.15, desc, fontsize=7, color="#134E4A")
        y_pos -= 0.85

    # Connecting Arrows
    arrow_kw = dict(arrowstyle="simple,head_width=0.7,head_length=0.7", color="#64748B", lw=1.5)
    ax.annotate("", xy=(4.7, 3.4), xytext=(4.2, 3.4), arrowprops=arrow_kw)
    ax.annotate("", xy=(9.2, 3.4), xytext=(8.7, 3.4), arrowprops=arrow_kw)

    # Subtitle note
    ax.text(7.0, 0.6, "Demonstration of hybrid semantic safety net resolving classical visual ambiguity: When structural vision fails to distinguish brown medicine bottles from beer bottles, OCR reads the label to execute a deterministic override.", 
            ha='center', fontsize=8, style='italic', color='#475569')

    plt.tight_layout()
    save_path = os.path.join(VISUALS_DIR, "fig5_11_codeine_ocr_case_study.png")
    plt.savefig(save_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Saved {save_path}")

if __name__ == "__main__":
    print("Generating all dissertation thesis visual figures...")
    generate_fig1_1()
    generate_fig2_1_table()
    generate_fig3_1_flowchart()
    generate_fig4_1_implementation_flowchart()
    generate_fig5_10_latency_benchmark()
    generate_fig5_11_case_study()
    print("All figures successfully created in visuals/!")
