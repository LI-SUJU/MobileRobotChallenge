import time
import sys
import tty
import termios
import picar_4wd as fc
import find_and_touch_red as ft
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
    # Move the robot in the specified direction with the given power
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

# List to log movements and their durations
movement_log = []

def manual_drive():
    # Function to manually drive the robot using WASD keys
    print("Begin manual driving, use WASD to control the robot, press Q to end.")
    running = True
    while running:
        key = readkey()
        if key == 'q':
            # If 'q' is pressed, navigate home and stop running
            navigate_home()
            running = False
        elif key in ['w', 's', 'a', 'd']:
            # Map WASD keys to actions
            action = {'w': 'forward', 's': 'backward', 'a': 'turn_left', 'd': 'turn_right'}[key]
            start_time = time.time()
            move(action, power_val)
            while readkey(readchar) == key:
                time.sleep(0.1)
            duration = time.time() - start_time
            movement_log.append((action, duration))
            stop()
        if key == 't':
            # If 't' is pressed, initiate the find and touch red object routine
            logs = ft.rotate_move_rotate_touch()
            navigate_home(logs) # navigate to the place where start to touch the object
            print("navigate")
            navigate_home(movement_log) # navigate back to the origin

def move_touch(logs):
    movement_log.extend(logs)
    print("touch logs", logs)


def navigate_home(logs):
    # Extend the movement log with new logs
    print("Navigating back to the origin...")
    reverse_commands = {
        'forward': 'backward',
        'backward': 'forward',
        'turn_left': 'turn_right',
        'turn_right': 'turn_left'
    }
    while logs:
        # Function to navigate back to the origin by reversing logged movements
        action, duration = logs.pop()
        move(reverse_commands[action], power_val)
        time.sleep(duration)
    stop()
    
# Start manual driving mode
manual_drive()


