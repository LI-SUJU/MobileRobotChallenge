import time
import picar_4wd as fc
from color_detect_new import analysis_image, color_detect, check_center_state
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

def turn_left():
    global movement_log
    start_time = time.time()
    move("turn_left", 5)
    duration = time.time() - start_time
    movement_log.append(("turn_left", duration))
    stop()

def go_forward():
    global movement_log
    start_time = time.time()
    move("forward", 5)
    duration = time.time() - start_time
    movement_log.append(("forward", duration))
    stop()
    
def trun_right():
    global movement_log
    start_time = time.time()
    move("turn_right", 5)
    duration = time.time() - start_time
    movement_log.append(("turn_right", duration))
    stop()
    
def move_to_touch_red():
    global movement_log
    start_time = time.time()
    move("forward", 5)
    time.sleep(0.2)
    duration = time.time() - start_time
    movement_log.append(("forward", duration))
    stop()
    
def adjust_rotate(center_state):
  if center_state == 1:
    trun_right()
  elif center_state == 3:
    turn_left()
  else:
    go_forward()

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
        diff_tolerance = 50
        img,img_2,img_3, contours =  color_detect(img,'red')
        cv2.imshow("video", img)    # OpenCV image show
        cv2.imshow("mask", img_2)    # OpenCV image show
        cv2.imshow("morphologyEx_img", img_3)    # OpenCV image show

        is_item_present, center_state, width_percentage = analysis_image(img, contours, diff_tolerance)
        print("image state", is_item_present, center_state, width_percentage)
        
        if is_item_present:
          if width_percentage < 0.5:
            current_state = check_center_state(img, contours, 60)
            adjust_rotate(current_state)
          else:
            current_state = check_center_state(img, contours, 20)
            adjust_rotate(current_state)

          k = cv2.waitKey(1) & 0xFF
          # 27 is the ESC key, which means that if you press the ESC key to exit
          if k == 27:
              break

      print('quit ...') 
      cv2.destroyAllWindows()
      camera.close()  