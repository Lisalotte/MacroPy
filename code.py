# A simple script to set the keys on a Pico RGB Keypad
# Optimized for use with Photoshop
# Runs on: Raspberry Pi Pico

# Required libraries:
# PMK - Pimoroni Mechanical/Mushy Keypad - CircuitPython
# Adafruit_hid - CircuitPython

from pmk import PMK
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware 

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Set up Keybow
keybow = PMK(Hardware())
keys = keybow.keys

# Set up keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# Set up consumer control
consumer_control = ConsumerControl(usb_hid.devices)

# Keymap
keymap = [
Keycode.B, #0
Keycode.M, #1
Keycode.CONTROL,  #2
Keycode.A, #3
Keycode.E, #4
Keycode.H, #5
Keycode.ALT, #6
Keycode.A, #7
Keycode.I, #8
Keycode.FIVE, #9 
Keycode.A, #10
Keycode.A, #11
Keycode.Z, #12
Keycode.LEFT_ALT, #13
Keycode.A, #14
Keycode.A, #15
]

# Key colours
rgb = [(70, 16, 0), (70, 0, 0), (70, 40, 0)]
i=0

for key in keys:
    key.set_led(*rgb[i])
    i = i + 1
    if i == 3: i = 0

    @keybow.on_press(key)
    def press_handler(key):
        keycode = keymap[key.number]
        if keycode == Keycode.CONTROL or keycode == Keycode.ALT:
            keyboard.press(keycode)
        elif key.number == 3:
            keyboard.press(Keycode.ALT)
            keyboard.press(Keycode.CONTROL)
            keyboard.send(Keycode.Z)
        elif key.number == 7:
            keyboard.press(Keycode.SHIFT)
            keyboard.press(Keycode.CONTROL)
            keyboard.send(Keycode.Z)
        else:
            keyboard.send(keycode)

    @keybow.on_release(key)
    def release_handler(key):        
        keycode = keymap[key.number]
        keyboard.release(keycode)
        if key.number == 3:
            keyboard.release(Keycode.ALT)
            keyboard.release(Keycode.CONTROL)            
        elif key.number == 7:
            keyboard.release(Keycode.SHIFT)
            keyboard.release(Keycode.CONTROL)            

while True:
    keybow.update()
