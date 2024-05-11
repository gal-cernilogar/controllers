import serial
import pydirectinput

arduino1 = serial.Serial('COM11', 115200, timeout=.1)     #serial input from arduino. change COM port to wherever your arduino is connected
arduino2 = serial.Serial('COM12', 115200, timeout=.1)     #serial input from arduino. change COM port to wherever your arduino is connected

pydirectinput.FAILSAFE = False
pydirectinput.PAUSE = 0

keysDown = {}   #list of currently pressed keys


def keyDown(key):               #what to do if key pressed. takes value from handleJoyStickAsArrowKeys
    keysDown[key] = True        #adds key to KeysDown list
    pydirectinput.keyDown(key)  #runs pydirectinput using key from (argument)
    #print('Down: ', key)       #remove '#' from print to test data stream


def keyUp(key):                     #what to do if key released. takes value from handleJoyStickAsArrowKeys
    if key in keysDown:
        del (keysDown[key])         #remove key from KeysDown
        pydirectinput.keyUp(key)    #runs pydirectinput using key from (argument)
        #print('Up: ', key)         #remove '#' from print to test data stream


def handleJoyStickAsArrowKeys(x, y, z):      #note that the x and y directions are swapped due to the way I orient my thumbstick
    if x == 0:          #0 is up on joystick
        keyDown('up')   #add up key to keyDown (argument)
        keyUp('down')   #add down key to keyUp (argument), as you can't press up and down together
    elif x == 2:        #2 is down on joystick
        keyDown('down')
        keyUp('up')
    else:               #1 is neutral on joystick
        keyUp('up')
        keyUp('down')

    if y == 2:          #2 is right on joystick
        keyDown('right')
        keyUp('left')
    elif y == 0:        #0 is left on joystick
        keyDown('left')
        keyUp('right')
    else:               #1 is neutral on joystick
        keyUp('left')
        keyUp('right')

    if z == 1:          #z argument is JSButton in this case. 1 is button pressed
        keyDown('')    #key to be pressed with Joystick button. Change to any key
    else:
        keyUp('')      #0 is button not pressed


def handleJoyStickAsAlternativeKeys(x, y, z):      #note that the x and y directions are swapped due to the way I orient my thumbstick
    if x == 0:          #0 is up on joystick
        keyDown('c')   #add up key to keyDown (argument)
        keyUp('v')   #add down key to keyUp (argument), as you can't press up and down together
    elif x == 2:        #2 is down on joystick
        keyDown('v')
        keyUp('c')
    else:               #1 is neutral on joystick
        keyUp('c')
        keyUp('v')

    if y == 2:          #2 is right on joystick
        keyDown('pageup')
        keyUp('pagedown')
    elif y == 0:        #0 is left on joystick
        keyDown('pagedown')
        keyUp('pageup')
    else:               #1 is neutral on joystick
        keyUp('pageup')
        keyUp('pagedown')

    if z == 1:          #z argument is JSButton in this case. 1 is button pressed
        keyDown('')    #key to be pressed with Joystick button. Change to any key
    else:
        keyUp('')      #0 is button not pressed


while True:
    rawdata1 = arduino1.readline()            #read serial data from arduino one line at a time
    data1 = str(rawdata1.decode('utf-8'))     #decode the raw byte data into UTF-8
    if data1.startswith("S"):                #make sure the read starts in the correct place
        dx = int(data1[1])                   #X direction is second digit in data (data[0] is 'S')
        dy = int(data1[3])                   #Y direction is fourth digit in data
        JSButton = int(data1[5])             #JSButton is sixth digit in data
        #print(dx, dy, JSButton)            #remove '#' from print to test data stream
        handleJoyStickAsAlternativeKeys(dx, dy, JSButton)     #run body of code using dx, dy and JSButton as inputs


    rawdata2 = arduino2.readline()            #read serial data from arduino one line at a time
    data2 = str(rawdata2.decode('utf-8'))     #decode the raw byte data into UTF-8
    if data2.startswith("S"):                #make sure the read starts in the correct place
        dx = int(data2[1])                   #X direction is second digit in data (data[0] is 'S')
        dy = int(data2[3])                   #Y direction is fourth digit in data
        JSButton = int(data2[5])             #JSButton is sixth digit in data
        #print(dx, dy, JSButton)            #remove '#' from print to test data stream
        handleJoyStickAsArrowKeys(dx, dy, JSButton)     #run body of code using dx, dy and JSButton as inputs
