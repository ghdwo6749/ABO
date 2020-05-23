#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
import sys
import numpy
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def get_frame():
    camera_port=0
    camera=cv2.VideoCapture(camera_port) #this makes a web cam object
    camera.set(3,320) #CV_CAP_PROP_FRAME_WIDTH
    camera.set(4,240) #CV_CAP_PROP_FRAME_HEIGHT
    #camera.set(1,1) #CV_CAP_PROP_FPS


    while True:
        retval, im = camera.read()
        imgencode=cv2.imencode('.jpg',im)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

    del(camera)

@app.route('/calc')
def calc():
     return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':

    app.run(host='192.168.43.89',port='8002', debug=True)
    
    
