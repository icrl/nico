import threading
import argparse
from threading import Thread
import adialog_new as ad
from naoqi import ALProxy
import shlex, subprocess
from sys import executable
from subprocess import *
import nicoGestures as gesture

dialog = {
          ########## casual response ##############
          '1': "Hi" , \
          '16': "Yes I'm very excited.", \
          '18': "Okay!", \
          ######## prompting the user to go on ############
          '20': "I want to learn how to solve this problem!", \
          '2': "How do you solve this problem?", \
          '5': "What do we do next?", \
          '8': "How do we do that?", \
          '13': "Nevermind. Please go on.", \
          ######## response to specific solutions #########
          '3': "Okay now we multiply?",\
          '4': "Okay now we add?", \
          '17': "Green paint?", \
          '19': "Okay so we divide?", \
          '21': "How did we get that number?", \
          ######## confused ##################
          '7': "That was a lot of information. Could you break it down into parts?", \
          '11': "Hmmm. That part seems complicated to me. Can you explain that again?", \
          '12': "Sorry, I was daydreaming. Could you explain that again?", \
          '15': "I don't know. Could you give me some hints?", \

          ####### end #############
          '6': "I think I understand now", \
          '9': "Yay we solved the problem!", \
          '10': "Thank you! You're awesome. You made me feel smarter.", \
          '14': "I'm getting tired now, but I think I understand the problem better. Maybe we can continue this another time." }




#Hello
def hello(command_dialog):
    tts = ALProxy("ALTextToSpeech", "nico.d.mtholyoke.edu", 9559)
    gesture.wave_hand()
    tts.say("Hello")

def yay(command_dialog):
    tts = ALProxy("ALTextToSpeech", "nico.d.mtholyoke.edu", 9559)
    gesture.yay()
    tts.say(dialog[command_dialog])

def peace(command_dialog):
    tts = ALProxy("ALTextToSpeech", "nico.d.mtholyoke.edu", 9559)
    gesture.peace()
    tts.say(dialog[command_dialog])
    
#I M LOST
def shrugAndShakeHead(command_dialog):
    tts = ALProxy("ALTextToSpeech", "nico.d.mtholyoke.edu", 9559)
    #tts.say(dialog[command_dialog])
    gesture.shrug_and_shakehead()
    tts.say(dialog[command_dialog])

def oneHandUp(command_dialog):
    tts = ALProxy("ALTextToSpeech", "nico.d.mtholyoke.edu", 9559)
    gesture.one_hand_up()
    tts.say(dialog[command_dialog])

#nodding
def nod(command_dialog):
    tts = ALProxy("ALTextToSpeech", "nico.d.mtholyoke.edu", 9559)
    gesture.head_yaw()
    tts.say(dialog[command_dialog])

def fistYay(command_dialog):
    tts = ALProxy("ALTextToSpeech", "nico.d.mtholyoke.edu", 9559)
    gesture.fistYay()
    tts.say(dialog[command_dialog])

#nodding
def shakeHead(command_dialog):
    tts = ALProxy("ALTextToSpeech", "nico.d.mtholyoke.edu", 9559)
    gesture.head_pitch()
    tts.say(dialog[command_dialog])

def other(command_dialog):
    tts = ALProxy("ALTextToSpeech", "nico.d.mtholyoke.edu", 9559)
    tts.say(command_dialog)

def shrug(command_dialog):
    tts = ALProxy("ALTextToSpeech", "nico.d.mtholyoke.edu", 9559)
    gesture.shrug()
    tts.say(dialog[command_dialog])


if __name__ == '__main__':
    filepath = "/home/nao/programs/move.top"
    #ad.main()
    args = shlex.split('python adialog_new.py')
    #subprocess.Popen(["python", "adialog_new.py"])
    p = subprocess.call(['gnome-terminal', '-x', 'bash', '-c','python adialog.py'])
    while (True): 
        print 'Input choice' 
        inp = raw_input(u"enter choice: ")
        if inp == 'Stop': 
            break
        elif inp == '9' or inp == '16':
            fistYay(inp)
        elif inp == '0':
            gesture.faceForward()
        elif inp == '1':
            hello(inp)
        elif inp == '2' or inp == '8' or inp == '5' or inp == '17' or inp == '20' or inp == '21':
            oneHandUp(inp)
        elif inp == '3' or inp == '4' or inp == '6' or inp == '18' or inp == '19':
            nod(inp)
        elif inp == '12' or inp == '14':
            shrug(inp)
        elif inp == '11' or inp == '15':
            shrugAndShakeHead(inp)
        elif inp == '7' or inp == '13':
            shakeHead(inp)
        elif inp == '10':
            peace(inp)
        else:
            other(inp)
        '''if inp is not None:
            speak(inp)'''
    #Thread(target = func2).start()
    subprocess.kill()
