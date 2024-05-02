import cv2
import cv2.aruco as aruco
import picar_4wd as fc
from picamera2 import Picamera2
import time

# 初始化摄像头
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'BGR888', 'size': (640,480)}, buffer_count=1))
camera.start()

# AR 标记检测函数
def findArucoMarkers(img, markerSize=6, totalMarkers=250, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, 'DICT_6X6_250')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters=arucoParam)
    return ids

def main():
    while True:
        img = camera.capture_array(wait=True)
        ids = findArucoMarkers(img)
        
        if ids is not None:
            for id in ids:
                if id == 0:  # 停止
                    fc.stop()
                elif id == 1:  # 直行
                    fc.forward(50)
                elif id == 2:  # 左转
                    fc.turn_left(50)
                elif id == 3:  # 右转
                    fc.turn_right(50)
                elif id == 4:  # 执行特别动作，例如原地转圈
                    # 这里可以添加您选择的特别动作
                    fc.turn_right(50)
                    time.sleep(1)
                    fc.stop()
        else:
            fc.stop()

        k = cv2.waitKey(30) & 0xff
        if k == 27:  # 按 ESC 退出
            break

    cv2.destroyAllWindows()
    camera.close()

if __name__ == '__main__':
    main()
