import cv2
import cv2.aruco as aruco
import numpy as np
import os

from picamera2 import Picamera2
import time

def findArucoMarkers(img, markerSize = 6, totalMarkers=250, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, 'DICT_6X6_250')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
    # print(ids)
    if draw:
        aruco.drawDetectedMarkers(img, bboxs) 
    return [bboxs, ids]

#with PiCamera() as camera:
#    camera.resolution = (640, 480)
#    camera.framerate = 24
#    rawCapture = PiRGBArray(camera, size=camera.resolution)
#    time.sleep(2)

camera = Picamera2()
camera.configure(camera.create_preview_configuration(
                            main={"format": 'BGR888', 'size': (640,480)},
                            buffer_count=1))
camera.start()

while True:
    img = camera.capture_array(wait=True) #frame.array
    arucofound = findArucoMarkers(img)
    # loop through all the markers and augment each one
    if  len(arucofound[0])!=0:
        for bbox, id in zip(arucofound[0], arucofound[1]):
            print(bbox)
    cv2.imshow('img',img)
    #rawCapture.truncate(0)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

print('quit ...')
cv2.destroyAllWindows()
camera.close()

