import os
import pygame
import serial
import math

os.environ["SDL_VIDEODRIVER"] = "dummy"

pygame.display.init()
pygame.joystick.init()

# wait untill joystick is connected
while 1:
    try:
        pygame.joystick.Joystick(0).init()
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

doggo = serial.Serial('/dev/tty.usbserial-DN042CH3', 115200)

def deadband(x, deadband):
    if math.fabs(x) < deadband:
        return 0
    else:
        return x

def doggo_send(x):
	doggo.write(bytes(x+'\n',"utf-8"))

while True:
    pygame.event.pump()

    forward = -pygame.joystick.Joystick(0).get_axis(1)
    right   = pygame.joystick.Joystick(0).get_axis(0)
    
    forward = deadband(forward, 0.1)
    right   = deadband(right, 0.1)

    b_button    = pygame.joystick.Joystick(0).get_button(2)
    a_button    = pygame.joystick.Joystick(0).get_button(1)

    x_button    = pygame.joystick.Joystick(0).get_button(0)
    y_button    = pygame.joystick.Joystick(0).get_button(3)

    # code to figure out what axis is which
    # for i in range(4):
    #     print(i, pygame.joystick.Joystick(0).get_axis(i))
    # for i in range(12):
    #     print(i, pygame.joystick.Joystick(0).get_button(i))

    # print("fwd", forward, "turn", right, 
    #             "x",x_button, "y",y_button, 
    #             "a",a_button, "b",b_button)

    if forward == 0 and right == 0 and a_button == 0:
        print('S')
        doggo_send('S')
    elif forward != 0:
        print('T;l%.3f' % (forward*0.15))
        doggo_send('T;l%.3f' % (forward*0.15))
    elif a_button == 1:
        print('H')
        doggo_send('H')
    else:
        print('S')
        doggo_send('S')

    pygame.time.wait(100)
