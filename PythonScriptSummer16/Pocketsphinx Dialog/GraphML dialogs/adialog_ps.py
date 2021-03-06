# -*- encoding: utf-8 -*-
# Adapted from Caitlin and Raeesa's GraphML reader 
import rospy
import networkx as nx
import argparse
import sys
import time
import datetime
import csv
import turn
import move_forward
import move_left
import move_right
import turn

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

	G = nx.read_graphml("pleasework2.graphml", unicode)
	
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
	
	# Constantly read from words.log for new lines
	while True:
		
		line = f.readline() 
		# If the user said something
		if line:
			# The lines with dialogue all begin with a numerical value
			if line[0][:1] in '0123456789':
				# remove 9 numbers, colon, and space from the beginning, and any whitespace from the end of the line
				speech = line[11:].rstrip()
				print speech
				
				# Search through all edges connected to the current node
				for e in G.edges(current, data=True):
					
					if current == 'n4' or current == 'n5' or current == 'n6' or current == 'n7' or str(speech) == str(e[2].values()[0]):

						if (current == 'n4' or current == 'n5'):
							if str(speech) == 'COMPUTER SCIENCE':
								temp = 'n7'
							else:
								temp = 'n6'
	
						elif current == 'n6' or current == 'n7':
							temp = 'n8'
							

						#print 'key %s' %str(e[2].values()[0])
						# If what was spoken matches the 'spoken' attribute of the edge
						elif str(speech) == str(e[2].values()[0]):
							#print speech
								
							# Switch the current node to be the node the edge goes to
							temp = e[1]

						if speech == 'MOVE':
							action = 'move'
						if speech == 'TURN':
							action = 'turn'
						if speech == 'RIGHT':
							if action == 'move':
								move_right.main("nico.d.mtholyoke.edu", 9559, 1)
							if action == 'turn':
								turn.main("nico.d.mtholyoke.edu", 9559, "right")
							time.sleep(2)
						if speech == 'LEFT':
							if action == 'move':
								move_left.main("nico.d.mtholyoke.edu", 9559, 1)
							if action == 'turn':
								turn.main("nico.d.mtholyoke.edu", 9559, "left")	
							time.sleep(2)					
						if speech == 'FORWARD':
							move_forward.main("nico.d.mtholyoke.edu", 9559, 1)
							time.sleep(2)

						current = temp	
						# Get the dialogue stored in the new node and save it in 'output'
						output = G.node[current]['robot']
						print 'OUTPUT: %s' %output
						tts.say(str(output))

						break
							# Add 'output' to the top of clean.log
							# with open("clean.log","r+") as g:
							# Read everything from clean.log into 'content'
							# content = g.read()
							# Go to the top of the file
							# g.seek(0,0)
							# Write 'output' with 'content' appended to the end back to clean.log
							# g.write(output.rstrip('\r\n')+'\n'+content)
							# g.close()
									
							# If there are no outgoing edges from the current node, go back to the root
							# if G.out_degree(current) == 0:
							# current = root


	def shutdown(self):
		f.close()
		sys.exit(0)

if __name__ == '__main__':
	try: 
		ttsconvert()

	except:
		print ("Terminated"); 		
		

