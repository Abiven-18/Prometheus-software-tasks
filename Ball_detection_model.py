from roboflow import Roboflow
import yaml
from ultralytics import YOLO
import requests
from PIL import Image
from io import BytesIO

#load dataset
rf = Roboflow(api_key="qlCoMkv7Ttq6Fhmpe1gn")
project = rf.workspace().project("soccer-ball-detection-hddyk")
dataset = project.version("2").download("yolov8")

with open("/content/soccer-ball-detection-2/data.yaml", "r") as f:
    data = yaml.safe_load(f)
print(data)

#train the model
model = YOLO("yolov8s.pt")
model.train(data="/content/soccer-ball-detection-2/data.yaml", epochs=50, imgsz=640, batch=8, verbose=True)

model.val()

#test it on an image
url = "https://icdn.football-espana.net/wp-content/uploads/2021/08/1002614356.jpg"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
model.predict(img, save=True, conf=0.5)

#test it an image with no ball
url = "https://i.nextmedia.com.au/News/GettyImages-1325105287.jpg"  
response = requests.get(url)
img = Image.open(BytesIO(response.content))

results = model.predict(img, save=True, conf=0.5)
results[0].show()

#with a ball now
url = "https://th.bing.com/th/id/OIP.1x8jsok-Zlbl35x08F5P0AHaEH?w=1080&h=600&rs=1&pid=ImgDetMain"  
response = requests.get(url)
img = Image.open(BytesIO(response.content))

results = model.predict(img, save=True, conf=0.5)
results[0].show()




