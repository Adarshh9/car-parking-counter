import cv2
import pickle
import cvzone
import numpy as np 
from ultralytics import YOLO
from IPython.display import display, Image

yolo_model = YOLO('best.pt')
def checkParkingSpace(yolo_model ,image_path):
    spaceCounter = 0
    totalSpaces = len(posList)
    
    results = yolo_model.predict(source=image_path, conf=0.25)

    detected_boxes = results[0].boxes.xyxy
    detected_classes = results[0].boxes.cls

    for i in range(len(detected_boxes)):
        if yolo_model.names[int(detected_classes[i].numpy().item())] == 'empty':
            
            color = (0,0,255)
            thickness = 2
        else:
            color = (0,255,0)
            thickness = 5
            spaceCounter += 1
        for pos in posList:
            cv2.rectangle(img ,pos ,(pos[0]+width,pos[1]+height) ,color ,thickness)
        
    cvzone.putTextRect(img ,f'Free: {spaceCounter}/{totalSpaces}' ,(100,50) ,scale=3 ,thickness=5 ,offset=20 ,colorR=(0,255,0))

        

with open('carParkPos','rb') as file:
    posList = pickle.load(file)

width ,height = 107 ,48

cap = cv2.VideoCapture('carPark.mp4')

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES ,0)
    
    success ,img = cap.read()
    
    checkParkingSpace(yolo_model ,img )
        
    cv2.imshow('Image',img)
    cv2.waitKey(1)