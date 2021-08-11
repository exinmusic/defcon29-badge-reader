import serial
from pythonosc.udp_client import SimpleUDPClient
from subprocess import call
from time import sleep
import time
import re
import struct
from enum import Enum

print("Turning OFF wlan0.")
call("sudo ifconfig wlan0 down", shell=True) # ensure no wifi

ip = "192.168.0.102"
port = 1337
client = SimpleUDPClient(ip, port)  # create client

class Role(Enum):
	HUMAN 	= 0b00000001
	GOON 	= 0b00000010
	CREATOR = 0b00000100
	SPEAKER = 0b00001000
	ARTIST 	= 0b00010000
	VENDOR 	= 0b00100000
	PRESS 	= 0b01000000
	UBER 	= 0b10000000

class Badge:
	def __init__(self, packet):
		self.packet = packet
		self.mask = packet[1]
	
	def check_role(self, role: Role):
		if role.value & self.mask:
			return role.name.lower()
		else:
			return ''

	def check_all_roles(self):
		role_stats = {}
		for role in Role:
			role_stats[role.name] = self.check_role(role)
		return role_stats

	def check_all_scores(self):
		return [struct.unpack('<H', self.packet[n-2:n])[0] for n in range(4,16,2)]

def send_to_visuals(num_badges, num_signal, solo_score, multi_score, played, most_badges, percent, human, goon, creator, speaker, artist, vendor, press, uber):
	# Number of Badges Connected
	osc_flag_command = "/composition/layers/3/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(num_badges)
	client.send_message(osc_flag_command, osc_flag_value)
	# Times the signal is shared.
	osc_flag_command = "/composition/layers/4/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(num_signal)
	client.send_message(osc_flag_command, osc_flag_value)
	# Solo Highscore
	osc_flag_command = "/composition/layers/5/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(solo_score)
	client.send_message(osc_flag_command, osc_flag_value)
	# Multi Highscore
	osc_flag_command = "/composition/layers/6/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(multi_score)
	client.send_message(osc_flag_command, osc_flag_value)
	# Games Played
	osc_flag_command = "/composition/layers/7/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(played)
	client.send_message(osc_flag_command, osc_flag_value)
	# Most Badges In A Game
	osc_flag_command = "/composition/layers/8/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(most_badges)
	client.send_message(osc_flag_command, osc_flag_value)
	# Percent Upper
	osc_flag_command = "/composition/layers/17/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(percent)
	client.send_message(osc_flag_command, osc_flag_value)
	# Percent Lower
	osc_flag_command = "/composition/layers/18/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(percent)
	client.send_message(osc_flag_command, osc_flag_value)

	# HUMAN
	osc_flag_command = "/composition/layers/9/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(human)
	client.send_message(osc_flag_command, osc_flag_value)
	# GOON
	osc_flag_command = "/composition/layers/10/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(goon)
	client.send_message(osc_flag_command, osc_flag_value)
	# CREATOR
	osc_flag_command = "/composition/layers/11/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(creator)
	client.send_message(osc_flag_command, osc_flag_value)
	# SPEAKER
	osc_flag_command = "/composition/layers/12/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(speaker)
	client.send_message(osc_flag_command, osc_flag_value)
	# ARTIST
	osc_flag_command = "/composition/layers/13/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(artist)
	client.send_message(osc_flag_command, osc_flag_value)
	# VENDOR
	osc_flag_command = "/composition/layers/14/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(vendor)
	client.send_message(osc_flag_command, osc_flag_value)
	# PRESS
	osc_flag_command = "/composition/layers/15/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(press)
	client.send_message(osc_flag_command, osc_flag_value)
	# UBER
	osc_flag_command = "/composition/layers/16/clips/2/video/source/blocktextgenerator/text/params/lines"
	osc_flag_value = str(uber)
	client.send_message(osc_flag_command, osc_flag_value)

def get_percent(types):
	type_count = 0
	for value in types.values():
		if value:
			type_count += 1
	return f"{round((type_count/7)*100)}%"

# MAIN LOOP
while True:

	while True:
		sleep(1)
		try:
			ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
			print('Badge reader connected!')
			break
		except:
			pass
		try:
			ser = serial.Serial('/dev/ttyACM1', 9600)
			print('Badge reader connected!')
			break
		except:
			print('Waiting for the badge reader to connect...')

	print('Making serial read blocking...')
	ser.timeout = None

	while True:

		try:
			s = ser.read(87) # Read serial
			print(f"SERIAL FEED:{bytes(s)}")
			print([ byt for byt in s ])
		except:
			print('Badger reader disconnected!')
			sleep(.5)
			ser.close()
			sleep(1)
			break

		split_s = s.split(b'\x1d\x1d\x1d')

		for bs in split_s:
			print(bs)
			if bs[0:1] == b'\xc9' and len(bs)==24:
				badge = Badge(bs)
				print(f"RAW BYTES:{badge.packet}")
				scores = badge.check_all_scores()
				types = badge.check_all_roles()
				print(f"BADGE TYPES:{types}")
				print(f"SCORES:{scores}")
				print("Sending OSC Packets...")

				send_to_visuals(scores[0], scores[1], scores[2], scores[3], scores[5], scores[4], get_percent(types), types['HUMAN'], types['GOON'], types['CREATOR'], types['SPEAKER'], types['ARTIST'], types['VENDOR'], types['PRESS'], types['UBER'])
