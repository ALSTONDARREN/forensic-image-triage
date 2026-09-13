from fpdf import FPDF
import datetime

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 15)
        self.cell(0, 10, "MSc Thesis - Progress Report", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def main():
    pdf = PDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "Supervisor Update Report", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # 1. Task Done Till Now
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "1. Task Progress Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    progress_text = (
        "The project has successfully completed the development of a comprehensive multi-model training pipeline for forensic triage categorization. "
        "The following key milestones have been achieved:\n"
        "- Automated massive dataset downloading and combining across several categories.\n"
        "- Implementation of an optimized PyTorch dataset preparation pipeline (80/20 train/val split, in-memory caching).\n"
        "- Development of a robust training loop with Early Stopping, Learning Rate Scheduling, and Metric Logging.\n"
        "- Execution of comparative experiments across three distinct CNN architectures using a larger, complex dataset."
    )
    pdf.multi_cell(0, 5, progress_text)
    pdf.ln(5)

    # 2. Dataset Information
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "2. Dataset Information", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    dataset_text = (
        "The current combined dataset consists of 4,951 real-world images representing digital forensic evidence. "
        "The dataset is divided into three primary categories:\n"
        "- Alcohol: 2,557 images\n"
        "- Drugs: 1,823 images\n"
        "- Weapons: 571 images\n\n"
        "Data augmentation techniques (Random Horizontal Flip, Random Rotation up to 15 degrees, and standard ImageNet Normalization) "
        "were actively applied during training to improve generalizability. The data is strictly split into 3,959 training images and 992 validation images."
    )
    pdf.multi_cell(0, 5, dataset_text)
    pdf.ln(5)

    # 3. Model Information
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "3. Model Architecture Details", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    model_text = (
        "The experiments evaluated three distinct pre-trained architectures modified for the multi-class forensic task:\n"
        "- ResNet-50: A 25M-parameter deep residual network serving as the industry standard benchmark.\n"
        "- VGG-16: A massive 138M-parameter older architecture for baseline and performance comparison.\n"
        "- MobileNetV3-Large: A highly efficient 5.4M-parameter architecture optimized for resource-constrained edge devices.\n\n"
        "All models used the Adam optimizer, Cross-Entropy Loss, and processed inputs at a standard 224x224 resolution."
    )
    pdf.multi_cell(0, 5, model_text)
    pdf.ln(5)

    # 4. Comparative Report
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "4. Multi-Model Evaluation & Comparative Findings", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    comparative_text = (
        "Based on the combined large dataset (4,951 images), all models were trained sequentially on CPU, yielding the following findings:\n\n"
        "A. ResNet-50\n"
        "- MCC: 0.9948 | Validation Accuracy: 99.50%\n"
        "- Inference Speed (CPU): ~294.22ms per image\n"
        "- Summary: Extremely accurate with almost zero false negatives. Serves as a perfect standard for forensic baseline evidence classification, but slower for real-time triage.\n\n"
        "B. MobileNetV3\n"
        "- MCC: 0.9931 | Validation Accuracy: 99.60%\n"
        "- Inference Speed (CPU): ~130.75ms per image\n"
        "- Summary: The absolute standout performer among deep learning models. Despite having ~80% fewer parameters than ResNet, it achieved the highest raw accuracy.\n\n"
        "C. VGG-16\n"
        "- MCC: 0.9914 | Validation Accuracy: 99.50%\n"
        "- Summary: While it achieved identical accuracy to ResNet-50, its massive parameter count made it exceptionally slow and inefficient for CPU-based training, proving older architectures are ill-suited for this rapid triage pipeline.\n\n"
        "D. Classical OpenCV (Random Forest & SVM)\n"
        "- Inference Speed (CPU): ~94.48ms per image (RF), ~96.52ms (SVM)\n"
        "- Summary: The classical pipelines successfully processed images significantly faster than the neural networks. The Random Forest pipeline proved to be roughly 1.3x faster than MobileNetV3 and 3.1x faster than ResNet-50.\n\n"
        "Conclusion: The hypothesis is strongly proven. Modern, efficient deep learning architectures like MobileNetV3 achieve >99% "
        "accuracy, but the classical OpenCV pipelines offer unmatched raw inference speed (under 100ms per image) on standard CPU hardware, making them a pragmatic choice for resource-constrained field laptops."
    )
    pdf.multi_cell(0, 5, comparative_text)
    
    pdf.output("Supervisor_Progress_Report.pdf")

if __name__ == "__main__":
    main()
