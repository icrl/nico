import argparse
import motion
import time

from naoqi import ALProxy

def main(robotIP, PORT = 9559, steps=1):
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    motionProxy.setMoveArmsEnabled(True, True)
    motionProxy.setExternalCollisionProtectionEnabled("All", False)
    motionProxy.moveTo(steps / 4.0, 0, 0) # X, Y, Theta

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=1, 
                        help="Number of steps")
    args = parser.parse_args()
    main("nico.d.mtholyoke.edu", 9559, args.steps)
