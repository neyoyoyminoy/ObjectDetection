from threading import Thread
import cv2
import time

class vStream: #this class will have a thread constantly grabbing frames
  def __init__(self,src) #always pass itself:
    self.capture=cv2.VideoCapture(src) #launching first camera
    self.thread=Thread(target=self.update,args=()) #continuously read a frame from cam1
    self.thread.daemon=True #when program ends the threads will end as well
    self.thread.start()
  def update(self):
    while True:
      _,self.frame=self.capture.read() #seperating two cameras frames
  def getFrame(self):
    return self.Frame+

#stopped at camSet
camSet=camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam1=vStream(1) #webcam
cam2=vStream(camSet) #PiCam
