#!/usr/bin/python3
import requests
from argparse import ArgumentParser
import sqlite3
from datetime import datetime
import configparser
import os

last_number = 0
last_number_filename = "/home/pi/Spesa/last_number.txt"

connection = sqlite3.connect('/home/pi/Spesa/database.db')
num_take = connection.execute('SELECT COUNT(*) FROM spesa WHERE toTake=1').fetchone()[0]
connection.close()

with open(last_number_filename,"r") as f:
	last_number = f.read()
	f.close()

if (int(num_take) == int(last_number)):
	exit()

if (int(num_take) == 0):
	config = configparser.ConfigParser()
	config.read('/home/pi/Spesa/config.ini')

	TOKEN = config['DEFAULT']['TELEGRAM_TOKEN']
	CHAT_ID = config['DEFAULT']['TELEGRAM_CHAT_ID']
	#CHAT_ID = config['DEFAULT']['PRIVATE_CHAT_ID']

	message = "Spesa finita..."

	if (TOKEN == None):
		print("ELEGRAM_TOKEN None")
		exit()
	if (CHAT_ID == None):
		print("TELEGRAM_CHAT_ID None")
		exit()
	if (message == None):
		print("message None")
		exit()
		
	url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN,CHAT_ID,message)
	response = requests.get(url).json()
	print(response) # this sends the message

with open(last_number_filename,"w") as f:
	f.write("{}".format(num_take))
	f.close()
