import argparse
import motion
import time

from naoqi import ALProxy

def main(robotIP, PORT = 9559, turn="left"):
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    motionProxy.setMoveArmsEnabled(True, True)
    motionProxy.setExternalCollisionProtectionEnabled("All", False)
    
    if turn == "left":
        theta = .5
    else:
        theta = -.5

    # X, Y, Theta, Freq
    motionProxy.setWalkTargetVelocity(0, 0, theta, 1)
    time.sleep(3.65)
    motionProxy.setWalkTargetVelocity(0, 0, 0, 0) # stop motion

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type = str, default = "left",
                        help = "direction to turn")
    args = parser.parse_args()
    main("nico.d.mtholyoke.edu", 9559, args.dir)
