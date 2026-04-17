import pyautogui
import pygetwindow as gw
from pynput import keyboard 
run = True
x= 635
y = 297
""" 
key_pressed = False
key_2 = False

def on_press(key):
    global key_pressed
    global key_2
    try:
        if key.char == 'q':
            key_pressed = True
        if key.char == 's':
            key_2 == True
    except AttributeError:
        pass

def on_release(key):
    global key_pressed
    try: 
        if key.char == 'q':
            key_pressed = False
        if key.char == 's':
            key_2 == False
    except AttributeError:
        pass
listener = keyboard.Lis tener(on_press=on_press, on_release=on_release)
listener.start()"""
while run:
    r,g,b = pyautogui.pixel(x*2, y*2)
    print(r,g,b)
    if r == 83 and b == 83 and g == 83:
        pyautogui.press("space")
    #if key_pressed:
        #run = False
