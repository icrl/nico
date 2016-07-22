# -*- encoding: utf-8 -*-
import networkx as nx
import argparse
import sys
import time
import datetime
import csv
import move_forward
import move_left
import move_right
import turn

from naoqi import (
    ALProxy,
    ALBroker,
    ALModule )


robotIP = "nico.d.mtholyoke.edu"
robot_port = 9959
nums = {'ZERO': 0, 'ONE': 1, 'TWO': 2, 'THREE': 3, 'FOUR': 4, 'FIVE': 5}

class ttsconvert():
    #myBroker = ALBroker("myBroker", "0.0.0.0",
                        #0, robotIP, robot_port)
    global tts
    tts = ALProxy("ALTextToSpeech", robotIP, 9559)
    
    def __init__(self):
      
	# Clear words.log
	f = open("words.log","r+")
	f.seek(0)
	f.truncate()
	
	dialog = dict()
	d = open("dialog.txt", "r"); 
	turns = d.readlines()
	global human 
	for turn in turns:
		if 'HUMAN: ' in str(turn): 
			human = turn[7:].rstrip()
			dialog[human] = []
		elif 'ROBOT: ' in str(turn):
			turn = turn[7:].rstrip()
			dialog[human].append(turn)
		else: 
			turn = str(turn[9:].rstrip())
			dialog[human].append(turn)
	
	#print dialog	
	
	# Clear clean.log
	with open("clean.log", "w"):
	    pass
	#Intro 	
	tts.say("Hello I'm Neeko")
	# Constantly read from words.log for new lines
	while True:
	    
 	    line = f.readline() 
	    # If the user said something
	    if line:
		# The lines with dialogue all begin with a numerical value
		if line[0][:1] in '0123456789':
		# remove 9 numbers, colon, and space from the beginning, and any whitespace from the end of the line
			speech = line[11:].rstrip()
			for key in dialog.keys(): 	
		    		# If what was spoken matches the 'spoken' attribute of the edge
				if speech in key:
					print 'INPUT %s' %key
					output = dialog[key][0]
					print 'OUTPUT: %s' %output
		    			tts.say(output)
					
					if 'MOVE' in speech: 
						if 'LEFT' in speech:
							tts.say("How many steps?")
							num = f.readline() 
							print 'NUM %s' %num
							time.sleep(2)
							if num in nums:
								move_left.main("nico.d.mtholyoke.edu", 9559, nums[num])
							else:
								tts.say("Missed")
							break
	
						if 'RIGHT' in speech:
							tts.say("How many steps?")
							num = f.readline() 
							time.sleep(3)
							move_right.main("nico.d.mtholyoke.edu", 9559, 1)
							break

						if 'FORWARD' in speech:  
							tts.say("How many steps?")
							num = f.readline() 
							time.sleep(3)
							move_forward.main("nico.d.mtholyoke.edu", 9559, 1)
							break
		
				else:
					tts.say("I didn't understand that")
					break
    def shutdown(self):
	f.close()
        sys.exit(0)

if __name__ == '__main__':
    try: 
	ttsconvert()

    except:
	print ("Terminated"); 	    
	

