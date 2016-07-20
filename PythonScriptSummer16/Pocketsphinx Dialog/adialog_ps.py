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
    #tts = ALProxy("ALTextToSpeech", robotIP, 9559)
    
    def __init__(self):	
	G = nx.read_graphml("write_graphml.graphml", unicode)
	
	root = 'n1'
	current = root
	
	# Clear words.log
	f = open("words.log","r+")
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
		    	#print 'IMPORTANT %s' %str(e[2].values()[0])
		        # If what was spoken matches the 'spoken' attribute of the edge
			if str(speech).upper() == str(e[2].values()[0]):
						
		        # Switch the current node to be the node the edge goes to
				current = e[1]
		        	
		        # Get the dialogue stored in the new node and save it in 'output'
				output = G.node[current]['robot']
				print 'OUTPUT: %s' %output
			
	    		#tts.say(str(output))
		        
		        # Add 'output' to the top of clean.log
				with open("clean.log","r+") as g:
		            		# Read everything from clean.log into 'content'
					content = g.read()
		            		# Go to the top of the file
					g.seek(0,0)
		            		# Write 'output' with 'content' appended to the end back to clean.log
		            		g.write(output.rstrip('\r\n')+'\n'+content)
		            		g.close()
		                
		        # If there are no outgoing edges from the current node, go back to the root
				if G.out_degree(current) == 0:
					current = root
			
		    

    def shutdown(self):
	f.close()
        sys.exit(0)

if __name__ == '__main__':
    try: 
	ttsconvert()

    except:
	print ("Terminated"); 	    
	

