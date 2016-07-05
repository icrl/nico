# -*- encoding: utf-8 -*-

# imports
import argparse
import sys
import time
import move_forward
import move_back
import move_left
import move_right
import turn
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
        memory.subscribeToEvent("forward", "Move", "onForward")
        memory.subscribeToEvent("back", "Move", "onBack")
        memory.subscribeToEvent("left", "Move", "onLeft")
        memory.subscribeToEvent("right", "Move", "onRight")
        memory.subscribeToEvent("turn", "Move", "onTurn")
        memory.subscribeToEvent("other", "Move", "onOther")
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
    
    # when a phrase not in the dialog is heard, print what robot thinks it heard
    def onOther(self, name, value):
        memory.unsubscribeToEvent("other", "Move")
        print value
        memory.subscribeToEvent("other", "Move", "onOther")

    # when the robot is told to move forward, move.
    # If not a valid number, robot says "I can't move that way!"
    def onForward(self, name, value):
        memory.unsubscribeToEvent("forward", "Move")
        # sets the number of steps to num as an integer, otherwise error text
        num = nums.get(value) or "I can't move that way!"
        # robot can't move if value is not a valid number
        if num == "I can't move that way!":
            ALProxy("ALTextToSpeech", robotIP, 9559).say(num)
        # otherwise move forward
        else:
            move_forward.main("nico.d.mtholyoke.edu", 9559, num)
        # make the number of squares to move forward zero
        memory.insertData("forward", "zero")
        memory.subscribeToEvent("forward", "Move", "onForward")
    
    # when the robot is told to move backward, move. If a valid number
    # is not given, robot says "I can't move that way!"
    def onBack(self, name, value):
        memory.unsubscribeToEvent("back", "Move")
        # sets the number of steps to num as an integer, otherwise error text
        num = nums.get(value) or "I can't move that way!"
        # robot can't move if value is not a valid number
        if num == "I can't move that way!":
            ALProxy("ALTextToSpeech", robotIP, 9559).say(num)
        # otherwise move backward
        else:
            move_back.main("nico.d.mtholyoke.edu", 9559, num)
        # set number of steps to move to zero
        memory.insertData("back", "zero")
        memory.subscribeToEvent("back", "Move", "onBack")

    # when the robot is told to move left, move. If a valid number
    # is not given, robot says "I can't move that way!"
    def onLeft(self, name, value):
        memory.unsubscribeToEvent("left", "Move")
        # sets the number of steps to num as an integer, otherwise error text
        num = nums.get(value) or "I can't move that way!"
        # robot can't move if value is not a valid number
        if num == "I can't move that way!":
            ALProxy("ALTextToSpeech", robotIP, 9559).say(num)
        # otherwise move left
        else:
            move_left.main("nico.d.mtholyoke.edu", 9559, num)
        # set number of steps to move to zero
        memory.insertData("left", "zero")
        memory.subscribeToEvent("left", "Move", "onLeft")

    # when the robot is told to move right, move. If a valid number
    # is not given, robot says "I can't move that way!"
    def onRight(self, name, value):
        memory.unsubscribeToEvent("right", "Move")
        # sets the number of steps to num as an integer, otherwise error text
        num = nums.get(value) or "I can't move that way!"
        # robot can't move if value is not a valid number
        if num == "I can't move that way!":
            ALProxy("ALTextToSpeech", robotIP, 9559).say(num)
        # otherwise move right
        else:
            move_right.main("nico.d.mtholyoke.edu", 9559, num)
        # set number of steps to move to zero
        memory.insertData("right", "zero")
        memory.subscribeToEvent("right", "Move", "onRight")

    # when the robot is told to turn, turn. If a valid direction is not given,
    # the robot says "I can't move that way!"
    def onTurn(self, name, value):
        memory.unsubscribeToEvent("turn", "Move")
        # checking for valid directions ('left' is often misheard as 'last')
        if value in ("left", "last", "right"):
            turn.main("nico.d.mtholyoke.edu", 9559, value)
        # otherwise give error message
        else:
            ALProxy("ALTextToSpeech", robotIP, 9559).say("I can't turn that way!")

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
def main(robot_ip, robot_port, topf_path):
    # creates the speech recognition proxy and a csv file
    createSpeechRecogProxy(robot_ip, robot_port)
    createFile(csvf)
    
    # creates dialog and posture proxies
    dialog_p = ALProxy('ALDialog', robot_ip, robot_port)
    postureProxy = ALProxy("ALRobotPosture", robot_ip, robot_port)
    dialog_p.setLanguage("English")
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
    
    # creates a module called "Move"
    global Move
    Move = TestModule("Move")

    # pressing key will unsubscribe from the topic
    raw_input(u"Press 'Enter to exit.")
        
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
    topf = sys.argv[1] 
    global csvf
    csvf = str(sys.argv [2])
    filepath = "/home/nao/programs/" + str(topf)
    main(robotIP, 9559, filepath)
