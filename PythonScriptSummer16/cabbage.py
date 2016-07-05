# -*- encoding: UTF-8 -*-

import sys
import time


from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

NAO_IP = "nico.d.mtholyoke.edu"

Test = None
memory = None

class TestModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        
        self.tts = ALProxy("ALTextToSpeech")
        asr = ALProxy("ALSpeechRecognition")
        
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
        #punch.main(NAO_IP, 9559)
        #memory.subscribeToEvent("WordRecognized", "Test", "onWordRecognized")
        #time.sleep(1)
        
def main():
    """ Main entry point

    """
    parser = OptionParser()
    parser.add_option("--pip",
        help="Parent broker port. The IP address or your robot",
        dest="pip")
    parser.add_option("--pport",
        help="Parent broker port. The port NAOqi is listening to",
        dest="pport",
        type="int")
    parser.set_defaults(
        pip=NAO_IP,
        pport=9559)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port
    # Warning: HumanGreeter must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global Test
    Test = TestModule("Test")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()
