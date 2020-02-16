import os
import pygame
import serial
import math
import signal

# prevents quiting on pi when run through systemd
def handler(signum, frame):
    print("GOT singal", signum)
signal.signal(signal.SIGHUP, handler)

# those two lines allow for running headless (hopefully)
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.putenv('DISPLAY', ':0.0')

pygame.display.init()
pygame.joystick.init()

# wait until joystick is connected
while 1:
    try:
        pygame.joystick.Joystick(0).init()
        print("Connected to joystick")
        break
    except pygame.error:
        pygame.time.wait(500)

# Prints the joystick's name
JoyName = pygame.joystick.Joystick(0).get_name()
print("Name of the joystick:")
print(JoyName)
# Gets the number of axes
JoyAx = pygame.joystick.Joystick(0).get_numaxes()
print("Number of axis:")
print(JoyAx)

doggo = serial.Serial('/dev/ttyACM0', 115200)

def deadband(x, deadband):
    if math.fabs(x) < deadband:
        return 0
    else:
        return x

def doggo_send(x):
    doggo.write(bytes(x+'\n',"utf-8"))

while True:
    pygame.event.pump()
    pygame.event.pump()

    r_x = (pygame.joystick.Joystick(0).get_axis(2)) # right side-to-side
    r_y = -(pygame.joystick.Joystick(0).get_axis(5)) # right up-down
    
    l_x = (pygame.joystick.Joystick(0).get_axis(0)) # left side-to-side
    l_y  = -(pygame.joystick.Joystick(0).get_axis(1)) # left up-down

    L2 = pygame.joystick.Joystick(0).get_axis(3)
    R2 = pygame.joystick.Joystick(0).get_axis(4)

    on_right = (pygame.joystick.Joystick(0).get_button(5))
    on_left = (pygame.joystick.Joystick(0).get_button(4))
    l_trigger = (pygame.joystick.Joystick(0).get_axis(3))
    r_trigger = (pygame.joystick.Joystick(0).get_axis(4))

    square = pygame.joystick.Joystick(0).get_button(0)
    x = pygame.joystick.Joystick(0).get_button(1)
    circle = pygame.joystick.Joystick(0).get_button(2)
    triangle = pygame.joystick.Joystick(0).get_button(3)

    (d_pad_x, d_pad_y) = (pygame.joystick.Joystick(0).get_hat(0))
    
    # Apply deadband to the forward commands and the turning commands
    forward_back = deadband(l_y, 0.1)
    left_right = deadband(l_x, 0.1)

    if forward_back == 0 and left_right == 0 and x == 0 and circle == 0:
        print('S')
        doggo_send('S')
    elif forward_back != 0 or left_right != 0:
        print('Y;l%.3f;s%.3f' % ((forward_back * 0.15), (left_right * 0.08)))
        doggo_send('Y;l%.3f;s%.3f' % ((forward_back * 0.15), (left_right * 0.08)))
    elif x == 1:
        print('H')
        doggo_send('H')
    elif circle == 1:
        print('E')
        doggo_send('E')
    else:
        print('S')
        doggo_send('S')

    pygame.time.wait(100)
