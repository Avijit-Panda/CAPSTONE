#Import necessary libraries
from flask import Flask, render_template, Response
import cv2
import cvzone 
import argparse
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np
from PIL import Image
from datetime import datetime
import uuid
import random
import string
import time

timeout = time.time() + 10  # 10 s
para = cv2.aruco.DetectorParameters_create()
aru_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_100)

def aruco(img):
    image_greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                             #Finding the contours and processing the image
    image_blur = cv2.GaussianBlur(img,(5,7),0)
    imagecanny = cv2.Canny(image_blur,100,200)
    kernel = np.ones((2,2)) 
    imgDial = cv2.dilate(imagecanny,kernel,iterations=3)
    iThre = cv2.erode(imgDial,kernel,iterations=2)
    thresh, image_black = cv2.threshold(image_greyscale, 100,100,cv2.THRESH_BINARY)
    corners, _, _ = cv2.aruco.detectMarkers(img, aru_dict, parameters=para)
    if corners:
                        int_corners = np.int0(corners)
                        cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
                        contours, _ = cv2.findContours(iThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                        aru_peri = cv2.arcLength(corners[0], True)
                        
                        pix_cm_rat = aru_peri / 20
                        
                        return(pix_cm_rat)
def logtime(file):
    n=datetime.now()
    start=n.strftime("%H:%M:%S")
    file.write("Time-"+str(start)+'\n')

def get_first_and_last_lines(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        first_line = lines[0].strip() if lines else None
        last_line = lines[-1].strip() if lines else None
    return first_line, last_line     
      
def count_lines(filename):
    with open(filename, "r") as file:
        line_count = sum(1 for line in file)
    return line_count

vidn=str("de")
vidname=str(vidn)+".avi"
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(vidname, fourcc, 20.0, (640, 480))
fname=str(vidn)+".txt"                       
file=open(fname,"a")
    

file.write("Sl.no"+'\t'+"Timestamp"+'\n')

detector = FaceMeshDetector(maxFaces=1)
idList =[22,23,24,26,110,157,158,159,160,161,130,243,252,253,254,255,385,384,386,382,388,359]

#Initialize the Flask app
app = Flask(__name__)

cap = cv2.VideoCapture(0)
def gen_frames():
    bcounter=0 
    counter=0 
    while True:
        # success, frame = camera.read()  # read the camera frame
        # if not success:
        #     break
        # else:
        #     ret, buffer = cv2.imencode('.jpg', frame)
        #     frame = buffer.tobytes()
        #     yield (b'--frame\r\n'
        #            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            _, img = cap.read()
            
            img, faces = detector.findFaceMesh(img,draw=False)
            pixcm=aruco(img)
                                
            if faces:
                file=open(fname,"a")
                
                now = datetime.now()

                current_time = now.strftime("%H:%M:%S")
                logtime(file)
                
                face = faces[0]
                for id in idList:
                    cv2.circle(img,face[id],2,(255,0,255),cv2.FILLED)

                leftUp=face[159]
                leftDown=face[23]
                leftLeft=face[130]
                leftRight=face[243]
                rightUp=face[386]
                rightDown=face[253]
                rightLeft=face[382]
                rightRight=face[359]
                lengthLeftV,_ = detector.findDistance(leftUp,leftDown) 
                lengthLeftH,_ = detector.findDistance(leftLeft,leftRight)
                lengthRightV,_ = detector.findDistance(rightUp,rightDown) 
                lengthRightH,_ = detector.findDistance(rightLeft,rightRight)
                
                cv2.line(img,leftUp,leftDown,(0,200,0),2)
                cv2.line(img,rightUp,rightDown,(0,200,0),2)
                cv2.line(img,leftLeft,leftRight,(0,200,0),2)
                cv2.line(img,rightLeft,rightRight,(0,200,0),2)
                if pixcm!=None:
                    ratioLeft = (lengthLeftV/pixcm)/(lengthLeftH/pixcm)
                    ratioRight=(lengthRightV/pixcm)/(lengthRightH/pixcm)
                    
            
                    if round(ratioLeft,2)<0.29 and round(ratioRight,2)<0.29 and counter==0:
                        print(ratioLeft)
                        bcounter+=1
                        counter = 1
                        print(bcounter)
                        file=open(fname,"a")
                        file.write("Blink:"+ str(bcounter)+'\n')
                        
                            
                    if counter !=0:
                        counter+=1
                        if counter>12:
                            counter = 0
                
                cvzone.putTextRect(img,f'Blink Count: {bcounter}',(50,100))
            
            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
            
            
            # file.write("Blinks:"+str(blinks)+'\n')
            # blinkrate=round((blinks*60)/t,2)
     
           # file.write("BlinkRate:"+str(blinkrate)+" "+"blinks per minute")
          
            
            