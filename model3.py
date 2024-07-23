import torch
import torchvision
from PIL import Image

print("Running Model 3: Image Classification")
model = torchvision.models.resnet18(pretrained=True)
model.eval()

# Example: classify a random image
random_image = torch.rand(1, 3, 224, 224)
with torch.no_grad():
    output = model(random_image)

print(f"Model output shape: {output.shape}")
print("Model ready for image classification")