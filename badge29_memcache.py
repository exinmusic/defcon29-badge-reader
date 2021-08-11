from pythonosc.udp_client import SimpleUDPClient
from subprocess import call
from time import sleep
import time
from pymemcache.client import base
from pprint import pprint
import json

print("Lemme see dat cache...")
print("Turning OFF wlan0.")
call("sudo ifconfig wlan0 down", shell=True) # ensure no wifi

ip = "192.168.0.102"
port = 1337
client = SimpleUDPClient(ip, port)  # create client

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

	if str(uber) == "begins?":
		osc_flag_command = "/composition/layers/19/clips/3/connect"
		osc_flag_value = 1
		client.send_message(osc_flag_command, osc_flag_value)
	elif str(uber) == "aliens!":
		osc_flag_command = "/composition/layers/19/clips/2/connect"
		osc_flag_value = 1
		client.send_message(osc_flag_command, osc_flag_value)
	elif str(uber) == "new signal!":
		osc_flag_command = "/composition/layers/19/clips/4/connect"
		osc_flag_value = 1
		client.send_message(osc_flag_command, osc_flag_value)
	elif not uber:
		print("CLEAR!")
		osc_flag_command = "/composition/layers/19/clips/5/connect"
		osc_flag_value = 1
		client.send_message(osc_flag_command, osc_flag_value)



def get_percent(types):
	type_count = 0
	for value in types.values():
		if value:
			type_count += 1
	return f"{round((type_count/8)*100)}"

# MAIN LOOP
while True:

	mem_client = base.Client(('localhost',11211))
	stats =  json.loads(mem_client.get('badgedata').decode('UTF-8'))
	pprint(stats)
	sleep(1)

	types = {'Human':'','Goon':'','Creator':'','Speaker':'', 'Artist':'', 'Vendor':'','Press':''}
	for key in stats['badgetypes'].split(','):
		types[key] = key.lower()
	pprint(types)

	secret_mode = ''
	percentnow = get_percent(types)
	if stats['ctf']['redpill']:
		secret_mode = "begins?"
		percentnow = int(get_percent(types)) + 10
	if stats['ctf']['newsignal']:
		secret_mode = "new signal!"
		percentnow = int(get_percent(types)) + 11
	if stats['ctf']['aliens']:
		secret_mode = "aliens!"
		percentnow = 1337

	send_to_visuals(stats['connected'], stats['signal'], stats['gamestats']['highscore'], stats['gamestats']['m-highscore'], stats['gamestats']['m-played'], stats['gamestats']['m-longest'], f"{percentnow}%", types['Human'], types['Goon'], types['Creator'], types['Speaker'], types['Artist'], types['Vendor'], types['Press'], secret_mode)
