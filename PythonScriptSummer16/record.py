# Records sound onto the robot for 10 seconds

# imports
import time

from naoqi import ALProxy

def main(robotIP, PORT = 9559):
    recorderProxy = ALProxy("ALAudioRecorder", robotIP, PORT)
    recorderProxy.stopMicrophonesRecording()
    
    print("recorded")
    # configure channels
    # left, right, front rear (mics?)
    channels = (0, 0, 1, 0); # python tuple, C++ code uses AL:ALValue
    recorderProxy.startMicrophonesRecording("~/ICRL/nao-setup/test.wav", "wav", 16000, channels)
    
    # continue recording for 10 seconds
    time.sleep(10)

    # stop recording
    recorderProxy.stopMicrophonesRecording()

if __name__ == "__main__":
    main("nico.d.mtholyoke.edu", 9559)
