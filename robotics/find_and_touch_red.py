import time
import picar_4wd as fc
from color_detect_v3 import analysis_image, color_detect, check_center_state
from picamera2 import Picamera2
import cv2
movement_log = []

   

def move(action, power_val):
    if action == "forward":
        fc.forward(power_val)
    elif action == "backward":
        fc.backward(power_val)
    elif action == "turn_left":
        fc.turn_left(power_val)
    elif action == "turn_right":
        fc.turn_right(power_val)
    else:
        fc.stop()

def stop():
    fc.stop()
    print("stop")

def rotate_to_find_red():
  
    global movement_log
    start_time = time.time()
    move("turn_left", 5)
    duration = time.time() - start_time
    movement_log.append(("turn_left", duration))
    stop()
    print("rotate_to_find_red")
    isRedFound = False

def move_close_to_red():
    global movement_log
    start_time = time.time()
    move("forward", 5)
    duration = time.time() - start_time
    movement_log.append(("forward", duration))
    stop()
    print("move_close_to_red")
def rotate_to_middle_red():
    global movement_log
    start_time = time.time()
    move("turn_right", 5)
    duration = time.time() - start_time
    movement_log.append(("turn_right", duration))
    stop()
    print("rotate_to_middle_red")
def move_to_touch_red():
    global movement_log
    start_time = time.time()
    move("forward", 5)
    time.sleep(0.2)
    duration = time.time() - start_time
    movement_log.append(("forward", duration))
    stop()
    print("move_to_touch_red")

def rotate_move_rotate_touch():

  with Picamera2() as camera:
      print("start color detect")

      camera.preview_configuration.main.size = (640,480)
      camera.preview_configuration.main.format = "RGB888"
      camera.preview_configuration.align()
      camera.configure("preview")
      camera.start()

      while True:
          img = camera.capture_array() #frame.array
          img,img_2,img_3, contours =  color_detect(img,'red')
          cv2.imshow("video", img)    # OpenCV image show
          cv2.imshow("mask", img_2)    # OpenCV image show
          cv2.imshow("morphologyEx_img", img_3)    # OpenCV image show

          is_item_present, is_center, width_percentage = analysis_image(img, contours)
          print(is_item_present, is_center, width_percentage)

          while not is_item_present:
              img = camera.capture_array()  # frame.array
              img, img_2, img_3, contours = color_detect(img, 'red')
              rotate_to_find_red()
              is_item_present, is_center, width_percentage = analysis_image(img, contours)
              print(is_item_present, is_center, width_percentage)
              cv2.imshow("video", img)  # OpenCV image show
              cv2.imshow("mask", img_2)  # OpenCV image show
              cv2.imshow("morphologyEx_img", img_3)  # OpenCV image show
          print("found red")

          # while width_percentage < 0.5:
          #     move_close_to_red()
          #     is_item_present, is_center, width_percentage = analysis_image(img, contours)
          # print("close to red")

          while not is_center:
              img = camera.capture_array()  # frame.array
              img, img_2, img_3, contours = color_detect(img, 'red')
              rotate_to_middle_red()
              is_item_present, is_center, width_percentage = analysis_image(img, contours)
              cv2.imshow("video", img)  # OpenCV image show
              cv2.imshow("mask", img_2)  # OpenCV image show
              cv2.imshow("morphologyEx_img", img_3)  # OpenCV image show
              print("red in middle")

          while width_percentage < 0.7:
              img = camera.capture_array()  # frame.array
              img, img_2, img_3, contours = color_detect(img, 'red')
              move_to_touch_red()
              is_item_present, is_center, width_percentage = analysis_image(img, contours)
              cv2.imshow("video", img)  # OpenCV image show
              cv2.imshow("mask", img_2)  # OpenCV image show
              cv2.imshow("morphologyEx_img", img_3)  # OpenCV image show
          print("touch red")


          k = cv2.waitKey(1) & 0xFF
          # 27 is the ESC key, which means that if you press the ESC key to exit
          if k == 27:
              break

      print('quit ...') 
      cv2.destroyAllWindows()
      camera.close()  