import cv2
import cv2.aruco as aruco
import numpy as np
from picamera2 import Picamera2
import time

def findArucoMarkers(img, markerSize=6, totalMarkers=250, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, 'DICT_6X6_250')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters=arucoParam)
    if draw:
        aruco.drawDetectedMarkers(img, bboxs)
    return [bboxs, ids]

def arucoAug(bbox, id, img, imgAug):
    tl = bbox[0][0][0], bbox[0][0][1]
    tr = bbox[0][1][0], bbox[0][1][1]
    br = bbox[0][2][0], bbox[0][2][1]
    bl = bbox[0][3][0], bbox[0][3][1]
    h, w, c = imgAug.shape
    pts1 = np.array([tl, tr, br, bl])
    pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    matrix, _ = cv2.findHomography(pts2, pts1)
    imgout = cv2.warpPerspective(imgAug, matrix, (img.shape[1], img.shape[0]))
    cv2.fillConvexPoly(img, pts1.astype(int), (0, 0, 0))
    imgout = img + imgout
    return imgout
    
# 加载替换的图像
imgSign = [
    cv2.imread("stop.jpg"),
    cv2.imread("left.jpg"),
    cv2.imread("right.jpg"),
    cv2.imread("return.jpg"),
    cv2.imread("noreturn.jpg"),
    cv2.imread("pedestrian.jpg")
]



camera = Picamera2()
camera.configure(camera.create_preview_configuration(
                            main={"format": 'BGR888', 'size': (640,480)}, 
                            buffer_count=1))
camera.start()

while True:
    img = camera.capture_array(wait=True)
    arucofound = findArucoMarkers(img)

    if len(arucofound[0]) != 0:
        for bbox, id in zip(arucofound[0], arucofound[1]):
            if id[0] < len(imgSign):
                img = arucoAug(bbox, id, img, imgSign[id[0]])

    cv2.imshow('img', img)

    if cv2.waitKey(30) & 0xff == 27:
        break

print('quit ...')
cv2.destroyAllWindows()
camera.close()
