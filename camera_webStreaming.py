#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
import sys
import numpy
import threading
import jetson.inference
import jetson.utils

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.gstCamera(320,240,"/dev/video0")  # using V4L2

app = Flask(__name__)

@app.route('/')
def index():
return render_template('index.html')

def get_frame():
    #camera_port=0
    #camera=cv2.VideoCapture(camera_port) #this makes a web cam object
    #camera.set(3,320) #CV_CAP_PROP_FRAME_WIDTH
    #camera.set(4,240) #CV_CAP_PROP_FRAME_HEIGHT
    #camera.set(1,1) #CV_CAP_PROP_FPS
global camera,net
while True:
img, width, height = camera.CaptureRGBA(zeroCopy=1)
detections = net.Detect(img, width, height)
img_numpy = jetson.utils.cudaToNumpy(img,width,height,4)
jetson.utils.cudaDeviceSynchronize()
imgencode=cv2.imencode('.jpg',img_numpy)[1]
stringData=imgencode.tostring()
yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

del(camera)

@app.route('/calc')
def calc():
     return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':

    app.run(host='192.168.43.29',port='8002', debug=True)
