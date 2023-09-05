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
def live():
    detector = FaceMeshDetector(maxFaces=1)

    idList =[22,23,24,26,110,157,158,159,160,161,130,243,252,253,254,255,385,384,386,382,388,359]
    
    fname=str(vidn)+".txt"                       
    file=open(fname,"x")
    
    logtime(file)
    file.write("Sl.no"+'\t'+"Timestamp"+'\n')
    bcounter=0
    counter=0
    
    while True:
            _, img = cap.read()
            
            img, faces = detector.findFaceMesh(img,draw=False)
            pixcm=aruco(img)
                                
            if faces:
                file=open(fname,"a")
                
                now = datetime.now()

                current_time = now.strftime("%H:%M:%S")
                
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
                        file.write(str(bcounter)+'\t'+str(current_time)+'\n')
                            
                    if counter !=0:
                        counter+=1
                        if counter>12:
                            counter = 0
                
                cvzone.putTextRect(img,f'Blink Count: {bcounter}',(50,100))  
                # if cap==cv2.VideoCapture(0):
                out.write(img)
                
                
            cv2.imshow("Image",img)
            key=cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    
    cap.release()
    out.release() 
    
    file=open(fname,"a")
    logtime(file)
    
    return(file)
    
    
    
    
    file.close(fname)

def recorded():
    detector = FaceMeshDetector(maxFaces=1)

    idList =[22,23,24,26,110,157,158,159,160,161,130,243,252,253,254,255,385,384,386,382,388,359]
    
    bcounter=0
    counter=0
    
    fname=str(vid)+".txt"                       
    file=open(fname,"x")
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
  
# calculate duration of the video
    seconds = round(frames / fps)
    file.write("Duration:"+str(seconds)+" "+"seconds"+'\n')
    file.write("Sl.no"+'\t'+"Timestamp"+'\n')
    print(seconds)
    try:
        while True:
            _, img = cap.read()
            
            img, faces = detector.findFaceMesh(img,draw=False)
            pixcm=aruco(img)
                                    
            if faces:
                    file=open(fname,"a")
                    
                    now = datetime.now()

                    current_time = now.strftime("%H:%M:%S")
                    
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
                        eyethres=float(0.29)
                
                        if round(ratioLeft,2)<0.29 and round(ratioRight,2)<0.29 and counter==0:
                            print(ratioLeft)
                            bcounter+=1
                            counter = 1
                            print(bcounter)
                            file.write(str(bcounter)+'\t'+str(current_time)+'\n')
                                
                        if counter !=0:
                            counter+=1
                            if counter>12:
                                counter = 0
                    
                    cvzone.putTextRect(img,f'Blink Count: {bcounter}',(50,100))  
                    # if cap==cv2.VideoCapture(0):
            cv2.imshow("Image",img)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                    
                    break
            
        cap.release()
        cv2.destroyAllWindows()  
    except:
        rcblinks()  
    
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

#Updating the output file for recorded video
def rcblinks():
    filename=str(vid)+".txt"
    file=open(filename,"a")
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
  
# calculate duration of the video
    seconds = round(frames / fps)
    lines=count_lines(filename)
    blink=lines-2
    
    file.write("Blink:"+str(blink)+'\n')
    blinkrate=round(((60*blink)/seconds),2)
    file.write("BlinkRate:"+str(blinkrate)+" "+"blinks per minute")

#Choose between live detection and recorded video
option=int(input("1.For Live Detection\n2.To pass a video\nEnter your Choice:"))
if option==1:
    vidn=input("Enter the name of file:")
    vidname=str(vidn)+".avi"
    
    if vidname!=None:
        
        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(vidname, fourcc, 20.0, (640, 480))
        live()
        filename=str(vidn)+".txt"
        file=open(filename,"a")
        first_line, last_line = get_first_and_last_lines(filename)
        print("First Line:", first_line)
        print("Last Line:", last_line)
        start=first_line.partition("-")
        end=last_line.partition("-")
        t1=datetime.strptime(start[2],"%H:%M:%S")
        t2=datetime.strptime(end[2],"%H:%M:%S")
        diff=t2-t1
        dt=diff.total_seconds()
        file.write("Duration:"+str(dt)+" "+"seconds"+'\n')
        nol=count_lines(filename)
        print(nol)
        blinks=nol-3
        file.write("Blinks:"+str(blinks)+'\n')
        blinkrate=round((blinks*60)/dt,2)
        file.write("BlinkRate:"+str(blinkrate)+" "+"blinks per minute")

else:
    vid=input("Enter the video file name:")
    video=str(vid)+".mp4"
    cap = cv2.VideoCapture(video)
    recorded()
    cap.release()
    
  
 
    
    
#cap = cv2.VideoCapture('eyeb.mp4')



    






    