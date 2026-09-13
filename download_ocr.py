import easyocr
import torch
print("Downloading EasyOCR models...")
reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())
print("Download complete!")
