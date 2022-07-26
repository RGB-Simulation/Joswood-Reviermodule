#!/usr/bin/env python

"""main.py: Controls WS2812 LEDs to simulate a daycycle."""

#from time import sleep
from utime import sleep
from machine import Pin
from neopixel import NeoPixel

__author__    = "Christian v. Schoenebeck (Develeon64)"
__copyright__ = "Copyright © (2022) Christian v. Schoenebeck"
__credits__   = ["Michael v. Schoenebeck", "Christian v. Schoenebeck"]
__contact__   = ["michael@v-schoenebeck.de", "software@develeon.de"]

__license__    = "UNLICENSED"
__version__    = "1.0.0"
__maintainer__ = "Christian v. Schoenebeck"
__email__      = "software@develeon.de"
__status__     = "Development"
__requires__   = ["MicroPython", "Raspberry Pi Pico"]
__since__      = "06.2022"
__date__       = "23.07.2022"

debug = 0
pin = 0
stangen = [
	298, # Zeche
	298, # Kokerei
	146, # Weiße Seite
	297, # Gasstraße
	228, # Hochofen
	297, # Überführung Links
	148, # Überführung Rechts
	298, # Hafen Links
	298, # Hafen Rechts
	147, # Kurve
	148, # Heiko Links
	297, # Heiko Rechts
#	2900 # Insgesamt
]
leds = 0
for i in range(len(stangen)):
	leds += stangen[i]

def start ():
	strip = NeoPixel(Pin(pin, Pin.OUT), leds)
	write_all_pixels(strip, 0, 0, 0)
	sleep(5)
	#for i in range(leds):
	#	band[i] = (63, 127, 191)
	#	band.write()
	#	sleep(0.1)
	return strip

def show_debug (strip):
	while True:
		write_all_pixels(strip, 0, 0, 0)
		sleep(1)
		write_all_pixels(strip, 0, 0, 255)
		sleep(1)
		write_all_pixels(strip, 0, 255, 0)
		sleep(1)
		write_all_pixels(strip, 0, 255, 255)
		sleep(1)
		write_all_pixels(strip, 255, 0, 0)
		sleep(1)
		write_all_pixels(strip, 255, 0, 255)
		sleep(1)
		write_all_pixels(strip, 255, 255, 0)
		sleep(1)
		write_all_pixels(strip, 255, 255, 255)
		sleep(1)

def stop (strip):
	set_all_pixels(strip, 63, 127, 191)
	for i in range(leds - 1, -1, -1):
		strip[i] = (0, 0, 0)
		strip.write()
		sleep(0.1)

def calc_subcolors (start, goal, count, phase):
	if start > goal:
		return int(start - (((start - goal) / count) * phase))
	elif start < goal:
		return int(start + (((goal - start) / count) * phase))
	else:
		return int(start)

def set_all_pixels (strip, red, green, blue):
	for i in range(leds):
		strip[i] = (red, green, blue)

def write_all_pixels (strip, red, green, blue):
	set_all_pixels(strip, red, green, blue)
	strip.write()

if __name__ == "__main__":
	band = start()

	if debug >= 2: show_debug(band)

	#scenes = [(255, 255, 127), (255, 255, 127), (255, 255, 127), (255, 255, 127)]
	#scenes = [(127, 0, 255), (63, 0, 255), (255, 255, 127), (255, 127, 63)]
	scenes = [(31, 0, 31), (15, 0, 63), (63, 63, 31), (255, 255, 127), (255, 255, 127), (255, 127, 63)]
	colors = [tuple()] * 864
	length = int(len(colors) / len(scenes))
	while True:
		for scene in range(len(scenes)):
			for i in range(length):
				r = calc_subcolors(scenes[scene][0], scenes[scene + 1 if scene < len(scenes) - 1 else 0][0], length, i)
				g = calc_subcolors(scenes[scene][1], scenes[scene + 1 if scene < len(scenes) - 1 else 0][1], length, i)
				b = calc_subcolors(scenes[scene][2], scenes[scene + 1 if scene < len(scenes) - 1 else 0][2], length, i)
				colors[(scene * length) + i] = (r, g, b)

		for i in range(len(colors)):
			write_all_pixels(band, colors[i][0], colors[i][1], colors[i][2])
			#sleep(1)

		if debug >= 1:
			write_all_pixels(band, 255, 0, 0)
			sleep(10)

	stop(band)
