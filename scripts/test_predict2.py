import torch
from torchvision import models, transforms
import cv2
import numpy as np
import torch.nn as nn
import os

CLASSES = ['alcohol', 'drugs', 'weapons']
DEVICE = torch.device('cpu')

model = models.mobilenet_v3_large(weights=None)
num_ftrs = model.classifier[3].in_features
model.classifier[3] = nn.Sequential(
    nn.Linear(num_ftrs, 512),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(512, len(CLASSES))
)
model.load_state_dict(torch.load('models_output/mobilenetv3/mobilenetv3_forensic_model.pth', map_location=DEVICE))
model.eval()

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def test_img(cls_name):
    img_dir = f'data/dataset_split/val/{cls_name}'
    img_name = os.listdir(img_dir)[0]
    img_path = os.path.join(img_dir, img_name)
    image = cv2.imread(img_path)
    if image is None:
        print(f"Failed to read image: {img_path}")
        return
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(input_tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)[0] * 100
    print(f'Testing {cls_name} image: {img_name}')
    for i, c in enumerate(CLASSES):
        print(f'{c}: {probs[i].item():.2f}%')

test_img('alcohol')
test_img('weapons')
