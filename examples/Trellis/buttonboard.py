#!/bin/env python

# Trellis - Scanner 

from __future__ import print_function
import time

from HT16K33 import Trellis

trellis=Trellis(bus=1).setUp()


numKeys=16

MOMENTARY = 0
LATCHING = 1
# Set the mode here:
MODE = LATCHING
# MODE =  MOMENTARY

for i in range(numKeys):
	trellis.setLED(i)
	trellis.writeDisplay()
	time.sleep(0.05)
# then turn them off
for i in range(numKeys):
	trellis.clrLED(i)
	trellis.writeDisplay()
	time.sleep(0.05)

# Loop
print('Press Ctrl-C to quit.')
while True:
	time.sleep(0.03)

	if MODE == MOMENTARY:
		# If a button was just pressed or released...
		if trellis.readSwitches():
			# go through every button
			for i in range(numKeys):
				# if it was pressed, turn it on
				if trellis.justPressed(i):
					print('v{0}'.format(i))
					trellis.setLED(i)
				# if it was released, turn it off
				if trellis.justReleased(i):
					print('^{0}'.format(i))
					trellis.clrLED(i)
			# tell the trellis to set the LEDs we requested
			trellis.writeDisplay()

	if MODE == LATCHING:
		# If a button was just pressed or released...
		if trellis.readSwitches():
			# go through every button
			for i in range(numKeys):
				# if it was pressed...
				if trellis.justPressed(i):
					print('v{0}'.format(i))
					# Alternate the LED
					if trellis.isLED(i):
						trellis.clrLED(i)
					else:
						trellis.setLED(i)
			# tell the trellis to set the LEDs we requested
			trellis.writeDisplay()


