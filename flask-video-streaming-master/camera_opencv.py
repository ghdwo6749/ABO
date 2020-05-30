import os
import cv2
import jetson.utils
import jetson.inference
import numpy as np
from base_camera import BaseCamera

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
width = 320	
height = 240

class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH,width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, frame = camera.read()
            frame = cv2.flip(frame, 1)
            frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA).astype(np.float32)
            img = jetson.utils.cudaFromNumpy(frame_rgba)
            detections = net.Detect(img, width, height)
            
            conv1 = jetson.utils.cudaToNumpy(img, width, height, 4)
            conv2 = cv2.cvtColor(conv1, cv2.COLOR_RGBA2RGB).astype(np.uint8)
            conv3 = cv2.cvtColor(conv2, cv2.COLOR_RGB2BGR)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', conv3)[1].tobytes()
