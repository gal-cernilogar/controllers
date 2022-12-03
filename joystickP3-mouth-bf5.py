import serial
import pydirectinput

arduino = serial.Serial('COM11', 115200, timeout=.1)     #serial input from arduino. change COM port to wherever your arduino is connected

pydirectinput.FAILSAFE = False
pydirectinput.PAUSE = 0

zoom = False
checkedForZoom = False

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

def toggleZoom():
    global zoom
    global checkedForZoom
    zoom = not zoom
    checkedForZoom = True


def handleJoyStickAsArrowKeys(x, y, z):      #note that the x and y directions are swapped due to the way I orient my thumbstick
    global zoom
    global checkedForZoom
    if x == 0:
        keyDown('c')
    elif x == 2 & checkedForZoom == False:
        if zoom == False:
            keyDown('v')
            toggleZoom()
            print(zoom)
        else:
            keyUp('v')
            toggleZoom()
            print(zoom)
        keyUp('c')
    else:
        keyUp('c')
        checkedForZoom = False

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
    rawdata = arduino.readline()            #read serial data from arduino one line at a time
    data = str(rawdata.decode('utf-8'))     #decode the raw byte data into UTF-8
    if data.startswith("S"):                #make sure the read starts in the correct place
        dx = int(data[1])                   #X direction is second digit in data (data[0] is 'S')
        dy = int(data[3])                   #Y direction is fourth digit in data
        JSButton = int(data[5])             #JSButton is sixth digit in 
        #print(dx, dy, JSButton)            #remove '#' from print to test data stream
        handleJoyStickAsArrowKeys(dx, dy, JSButton)     #run body of code using dx, dy and JSButton as inputs
