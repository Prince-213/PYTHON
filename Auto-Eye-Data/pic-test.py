from ultralytics import YOLO
from PIL import Image

model = YOLO('myset/best.pt')


source = 'new27.jpg'

results = model([source], save=True, conf=0.55, iou=0.4)



for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    print(result.path) # display to screen
    im = Image.open(f"runs/detect/predict/{result.path}") 

    im.show()