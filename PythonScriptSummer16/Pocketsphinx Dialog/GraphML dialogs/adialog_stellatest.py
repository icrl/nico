# -*- encoding: utf-8 -*-
# Adapted from Caitlin and Raeesa's GraphML reader 
import rospy
import networkx as nx
import argparse
import sys
import time
import datetime
import csv

from naoqi import (
	ALProxy,
	ALBroker,
	ALModule )

# proxies
#memory = None
#asr = None

# other global objects
writer = None # writer of the csv file
f = None # file to write to
#inputTime = 0 # holds the time of the speech

robotIP = "nico.d.mtholyoke.edu"
robot_port = 9959

class ttsconvert():
	
	global tts
	tts = ALProxy("ALTextToSpeech", robotIP, 9559)
	global G
	#def __init__(self):	

	G = nx.read_graphml("stella.graphml", unicode)
	
	root = 'n1'
	current = root
	recordData = sys.argv[1]
	# Clear words.log
	f = open(recordData,"r+")
	f.seek(0)
	f.truncate()

	# Clear clean.log
	with open("clean.log", "w"):
		pass
	
	while True:
	    line = f.readline()
	    
	    # If the user said something
	    if line:
		# The lines with dialogue all begin with a numerical value
			if line[0][:1] in '0123456789':
				# remove 9 numbers, colon, and space from the beginning, and any whitespace from the end of the line
				speech = line[11:].rstrip()
				#print speech
		
				# Search through all edges connected to the current node
				for e in G.edges(current, data=True):
				
			    # If what was spoken matches the 'spoken' attribute of the edge
					if str(speech) == str(e[2].values()[0]):
						# Switch the current node to be the node the edge goes to
						current = e[1]
				    
				    	# Get the dialogue stored in the new node and save it in 'output'
						output = G.node[current]['robot']
						print 'OUTPUT: %s' %output
						tts.say(str(output))
				


	def shutdown(self):
		f.close()
		sys.exit(0)

if __name__ == '__main__':
	try: 
		ttsconvert()

	except:
		print ("Terminated"); 		
		

