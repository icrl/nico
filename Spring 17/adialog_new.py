# -*- encoding: utf-8 -*-

# imports
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
Move = None
memory = None
asr = None

# other global objects
writer = None # writer of the csv file
f = None # file to write to
#inputTime = 0 # holds the time of the speech

robotIP = "nico.d.mtholyoke.edu"

# dictionary from text to digits
nums = {
    "one" : 1,
    "two" : 2,
    "to" : 2,
    "three" : 3,
    "four" : 4,
    "five" : 5
}

digits = [1, 2, 3, 4, 5]

# Module for Speech
class TestModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)

        global memory
        memory = ALProxy("ALMemory")
        
        # when these events change, the methods are called
        '''memory.subscribeToEvent("forward", "Move", "onForward")
        memory.subscribeToEvent("back", "Move", "onBack")
        memory.subscribeToEvent("left", "Move", "onLeft")
        memory.subscribeToEvent("right", "Move", "onRight")
        memory.subscribeToEvent("turn", "Move", "onTurn")
        memory.subscribeToEvent("other", "Move", "onOther")'''
        memory.subscribeToEvent("Dialog/LastInput", "Move", "onInput")
        memory.subscribeToEvent("ALTextToSpeech/CurrentSentence", "Move", "onCurrentSentence")
        memory.subscribeToEvent("SpeechDetected", "Move", "onSpeechDetected")

        global inputTime
        inputTime = time.time()
        global isDone
        isDone = True

    # when speech is detected, set inputTime's value to the current time
    def onSpeechDetected(self, name, value):
        global inputTime
        global isDone
        # if human is just starting to speak, set input time, otherwise don't
        if isDone:
            inputTime = time.time()
            isDone = False

    # when a word/phrase is recognized, write the recognized phrase to file
    def onInput(self, name, value):
        memory.unsubscribeToEvent("Dialog/LastInput", "Move")
        global inputTime
        global isDone
        # once the phrase is recognized, isDone can be set to true
        isDone = True
        # put the timestamp into a readable format
        st = datetime.datetime.fromtimestamp(inputTime).strftime('%a %h %d %H:%M:%S %Y')
        # write the timestamp and the utterance into the csv file (if not empty)
        if value != "":
            writer.writerow({' Time': st, 'human': value}) 
        memory.subscribeToEvent("Dialog/LastInput", "Move", "onInput")

    # when the robot says something, write the phrase to file
    def onCurrentSentence(self, name, value):
        memory.unsubscribeToEvent("ALTextToSpeech/CurrentSentence", "Move")
        # if the value is not empty, write to file
        if value != "":
            # get timestamp and convert to readable format
            ts = time.time() 
            st = datetime.datetime.fromtimestamp(ts).strftime('%a %h %d %H:%M:%S %Y')
            # write the timestamp and text into the csv file
            writer.writerow({' Time': st, 'robot': value}) 
        memory.subscribeToEvent("ALTextToSpeech/CurrentSentence", "Move", "onCurrentSentence")
  

# creates speech recognition proxy to add vocabulary to the robot
def createSpeechRecogProxy(robot_ip, robot_port):
    # creates the speech recognition proxy
    global asr
    asr = ALProxy("ALSpeechRecognition", robot_ip, robot_port)
    asr.setLanguage("English")
    asr.pause(True)
    # adds vocabulary, sets it, and enables word spotting
    vocabulary = ["what is the slope of the line from"]
    asr.setVocabulary(vocabulary, True)
    asr.pause(False)
    asr.subscribe("Test_ASR")

# creates csv file and its writer, takes in fName as input
def createFile(fName):
    global f
    # opens the file and creates a writer
    f = open(fName, 'w')
	
    global writer
    # sets the fieldnames and writes the header
    writer = csv.DictWriter(f, fieldnames=[' Time', 'human', 'robot'])
    writer.writeheader()

# main method
def main(robot_ip, robot_port, topf_path, csvf):
    # creates the speech recognition proxy and a csv file
    createSpeechRecogProxy(robot_ip, robot_port)
    createFile(csvf)
    
    # creates dialog and posture proxies
    dialog_p = ALProxy('ALDialog', robot_ip, robot_port)
    postureProxy = ALProxy("ALRobotPosture", robot_ip, robot_port)
    dialog_p.setLanguage("English")
    tts = ALProxy('ALTextToSpeech', robot_ip, robot_port)
    tts.say("starting")
    postureProxy.goToPosture("StandInit", 0.5) # brings robot to standing pos.
    
    # Load topic - absolute path is required
    # TOPIC MUST BE ON ROBOT 
    topic = dialog_p.loadTopic(topf_path)

    # Start dialog
    dialog_p.subscribe('myModule')
    
    # Activate dialog
    dialog_p.activateTopic(topic)

    # create broker
    myBroker = ALBroker("myBroker", "0.0.0.0",
                        0, robot_ip, robot_port)
    
    '''# creates a module called "Move"
    global Move
    Move = TestModule("Move")'''

    # pressing key will unsubscribe from the topic
    raw_input(u"Press 'Enter to exit.")
    #speech recognition unsubscribing from test_asr wtf?: 
    asr.unsubscribe("Test_ASR")

    # until interrupted, keep broker running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down" 
        myBroker.shutdown()

    # Deactivate topic
    dialog_p.deactivateTopic(topic)

    # Unload topic
    dialog_p.unloadTopic(topic)

    # Stop dialog
    dialog_p.unsubscribe('myModule')

    # close file
    f.close()

    # exit
    sys.exit(0)

if __name__ == '__main__': 
    global csvf 
    #csvf = 'test{}.csv'.format(time.time())
    csvf = 'testApril20.csv'
    filepath = "/home/nao/programs/move.top"
    main(robotIP, 9559, filepath, csvf)

'''
TODO:

additional speaking feature
yay hip shake
http://doc.aldebaran.com/2-1/nao/nao_freeze.html#nao-freeze
repeat thing
'''
