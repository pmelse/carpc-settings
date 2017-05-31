#  License: GPL v3
#  Copyright: Peter Melse, 2017
# Requirements:
#  $ sudo apt-get install xautomation
#  raspbian(os), or equivlent with the rpi gpio modules for python
#  rpi model (b)2 or later (for the 40 gpio pinout)
# Purpose: to provide hardware keys to nvlc (or rather the os globally)
#  with thanks to the raspberrypi.org/learning guide for GPIO pins, 
#  www.larsen-b.com/Article/184.html for general structure, and 
#  http://stackoverflow.com/questions/5714072/simulate-keystroke-in-linux-with-python for the xkb side of things.
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
from subprocess import Popen, PIPE

buttons = [18,         23,         24,         25,        8,     7 ]
opcodes = ['next', 'enter', 'alt tab', 'previous', 'spacebar', 'shift' ]
opcodes2 = ['key Left ', 'key Up ', 'key Down ', 'key Right ', 'key Return ', 'key Shift_L ']
# note the spaces after the commands above. they are necessary.

# set the gpio pins to UP 
for button in buttons:
    GPIO.setup(button, GPIO.IN, GPIO.PUD_UP )

def keypress(sequence):
    p = Popen(['xte', '-x:0'], stdin=PIPE)
    p.communicate(input=sequence)
	
def main():
    while True:
        #get the values for all push buttons
        button_state = []
        for button in buttons:
            button_state.append(GPIO.input(button))
        # conditional multibutton function:
        # power_off (if the first two buttons on the left the of the device are pressed)
        if button_state[0] == 0 and button_state[1] == 0:
            print ("shutting down! (in 2 sec)")
            time.sleep(2)
            Popen(['sudo', 'poweroff'])
            return
        # else we evaluate the rest of the button states, and press the relevant key(s)
        for item in range(len(button_state)):
            if button_state[item] == 0:
                # print (opcodes2[item] ) #debugging, useful for tweaking the main loop delay
                # send X key for keystroke in (for the given iteration of the loop) opcodes[button.output(index)]
                keypress(str(opcodes2[item]).encode('ascii'))
        print (repr(button_state)) #for debugging
        time.sleep(0.35)
        del button_state

if __name__ == '__main__':
    main()
