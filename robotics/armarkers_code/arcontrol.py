import cv2
import cv2.aruco as aruco
from picamera2 import Picamera2
import picar_4wd as fc
import time

speed = 50

camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'BGR888', 'size': (640,480)}, buffer_count=1))
camera.start()

def findArucoMarkers(img, markerSize=6, totalMarkers=250, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, 'DICT_' + str(markerSize) + 'X' + str(markerSize) + '_' + str(totalMarkers))
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters=arucoParam)
    if draw:
        aruco.drawDetectedMarkers(img, bboxs)
    return [bboxs, ids]

def execute_robot_action(id):
    if id == 0:  # Stop
        fc.stop()
    elif id == 1:  # Turn left 
        fc.turn_left(speed)
        time.sleep(0.5)
        fc.stop()
    elif id == 2:
        fc.turn_right(speed)
        time.sleep(0.5)
        fc.stop()
    elif id == 3:  # Straight
        fc.forward(speed)
        time.sleep(0.5)
        fc.stop()
    elif id == 4: 
        fc.forward(speed)
    elif id == 5:
        fc.turn_left(speed)
        time.sleep(0.5)
        fc.stop()
        time.sleep(0.5)
        fc.turn_left(speed)
        time.sleep(0.5)
        fc.stop()
        time.sleep(0.5)
        fc.turn_left(speed)
        time.sleep(0.5)
        fc.stop()
        time.sleep(0.5)
        fc.turn_left(speed)
        time.sleep(0.5)
        fc.stop()

last_seen_id = None 
try:
    while True:
        img = camera.capture_array(wait=True)
        bboxs, ids = findArucoMarkers(img)

        if ids is not None:
            ids = ids.flatten()
            current_id = ids[0]  
            execute_robot_action(current_id)    

        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    camera.close()
    fc.stop()
    cv2.destroyAllWindows()
