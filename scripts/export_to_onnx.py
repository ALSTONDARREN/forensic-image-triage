import torch
import torch.nn as nn
from torchvision import models
import os

def export_model_to_onnx():
    CLASSES = ['alcohol', 'drugs', 'weapons']
    NUM_CLASSES = len(CLASSES)
    
    # 1. Initialize Model Architecture
    print("Initializing MobileNetV3 architecture...")
    model = models.mobilenet_v3_large(weights=None)
    num_ftrs = model.classifier[3].in_features
    model.classifier[3] = nn.Sequential(
        nn.Linear(num_ftrs, 512),
        nn.ReLU(),
        nn.Dropout(0.5),
        nn.Linear(512, NUM_CLASSES)
    )
    
    # 2. Load Weights
    weights_path = "../models_output/mobilenetv3/mobilenetv3_forensic_model.pth"
    if not os.path.exists(weights_path):
        # Try relative to root if run from workspace root
        weights_path = "models_output/mobilenetv3/mobilenetv3_forensic_model.pth"
        
    if not os.path.exists(weights_path):
        print(f"[Error] Weights file not found at {weights_path}")
        return
        
    print(f"Loading weights from {weights_path}...")
    model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
    model.eval()
    
    # 3. Create dummy input tensor
    # The pipeline resizes to 224x224 and standardizes to 3 channels
    dummy_input = torch.randn(1, 3, 224, 224)
    
    # 4. Export to ONNX
    output_path = weights_path.replace(".pth", ".onnx")
    print(f"Exporting model to {output_path}...")
    
    torch.onnx.export(
        model, 
        dummy_input, 
        output_path,
        export_params=True,
        opset_version=12,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
    )
    
    print("[Success] Model exported to ONNX format successfully!")

if __name__ == "__main__":
    export_model_to_onnx()
