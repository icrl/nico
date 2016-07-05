# -*- encoding: UTF-8 -*-
import sys
import time


from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

NAO_IP = "138.110.234.37"

Test = None
memory = None

class TestModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        
        self.tts = ALProxy("ALTextToSpeech", "138.110.234.37", 9559)
        asr = ALProxy("ALSpeechRecognition", "138.110.234.37", 9559)
        
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("WordRecognized", "Test", "onWordRecognized")

        asr.pause(True)
        asr.setVocabulary(["cabbage", "hello", "punch"], True)
        asr.setAudioExpression(True)
        asr.setVisualExpression(True)
        asr.pause(False)
        
    def onWordRecognized(self, *_args):
        memory.unsubscribeToEvent("WordRecognized", "Test")
        self.tts.post.say("Cabbage")
        memory.subscribeToEvent("WordRecognized", "Test", "onWordRecognized")
        time.sleep(1)
