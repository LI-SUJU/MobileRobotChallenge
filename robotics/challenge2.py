import time
import sys
import tty
import termios
import picar_4wd as fc
import  find_and_touch_red_v2 as ft
power_val = 5

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)

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
    print("停止")

movement_log = []

def manual_drive():
    print("开始手动驱动，使用WASD控制机器人，按Q结束。")
    running = True
    while running:
        key = readkey()
        if key == 'q':
            navigate_home()
            running = False
        elif key in ['w', 's', 'a', 'd']:
            action = {'w': 'forward', 's': 'backward', 'a': 'turn_left', 'd': 'turn_right'}[key]
            start_time = time.time()
            move(action, power_val)
            while readkey(readchar) == key:
                time.sleep(0.1)
            duration = time.time() - start_time
            movement_log.append((action, duration))
            stop()
        if key == 't':
            logs = ft.rotate_move_rotate_touch()
            # move_touch(logs)
            navigate_home(logs)
            print("navigate")
            # navigate_home()
            navigate_home(movement_log)

def move_touch(logs):
    # logs = ft.rotate_move_rotate_touch()
    movement_log.extend(logs)
    print("touch logs", logs)



def navigate_home(logs):
    print("导航回原点...")
    reverse_commands = {
        'forward': 'backward',
        'backward': 'forward',
        'turn_left': 'turn_right',
        'turn_right': 'turn_left'
    }
    while logs:
        action, duration = logs.pop()
        move(reverse_commands[action], power_val)
        time.sleep(duration)
    stop()


# def navigate_home(logs):
#     print("导航回原点...")
#     reverse_commands = {
#         'forward': 'backward',
#         'backward': 'forward',
#         'turn_left': 'turn_right',
#         'turn_right': 'turn_left'
#     }
#     while movement_log:
#         action1, duration1 = movement_log.pop()
#         move(reverse_commands[action1], power_val)
#         time.sleep(duration1)
#     stop()

# 主逻辑
manual_drive()


