# -*- encoding: UTF-8 -*-

import motion
import almath
import time
from naoqi import ALProxy

def main(robotIP, PORT = 9559):
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    
    motionProxy.setExternalCollisionProtectionEnabled("All", False)
    
    motionProxy.rest()
    motionProxy.wakeUp()
    
    postureProxy.goToPosture("StandInit", 0.5)
    motionProxy.setStiffnesses("LArm", 1.0)
    motionProxy.setStiffnesses("RArm", 1.0)
    
#    motionProxy.setFootStepsWithSpeed(["LLeg"], [[0.06, 0.1, 0.0]], [0.8], False)
#    time.sleep(0.3)
    
    name = "LShoulderRoll"
    angle = 0
    fractionMaxSpeed = 0.25
    motionProxy.setAngles(name, -9 * almath.TO_RAD, fractionMaxSpeed)
    motionProxy.setAngles("LElbowRoll", -70.5 * almath.TO_RAD, fractionMaxSpeed)
    motionProxy.setAngles("LShoulderPitch", 30 * almath.TO_RAD, fractionMaxSpeed)
    motionProxy.setAngles("LElbowYaw", -70 * almath.TO_RAD, fractionMaxSpeed)
    motionProxy.closeHand("LHand")
    
    time.sleep(0.1)
    
    name = "RShoulderRoll"
    motionProxy.setAngles(name, 18 * almath.TO_RAD, fractionMaxSpeed)
    motionProxy.setAngles("RElbowRoll", 89.5 * almath.TO_RAD, fractionMaxSpeed)
    motionProxy.setAngles("RShoulderPitch", 30 * almath.TO_RAD, fractionMaxSpeed)
    motionProxy.setAngles("RElbowYaw", 70 * almath.TO_RAD, fractionMaxSpeed)
    motionProxy.closeHand("RHand")
    
    time.sleep(.3)
    
    #motionProxy.setAngles("RShoulderRoll", 0, 1)
    motionProxy.setAngles("RElbowRoll", 2 * almath.TO_RAD, 1)
    motionProxy.setAngles("RShoulderPitch", 0, 1)
    time.sleep(0.4)
    name = "RShoulderRoll"
    motionProxy.setAngles(name, 18 * almath.TO_RAD, 1)
    motionProxy.setAngles("RElbowRoll", 89.5 * almath.TO_RAD, 1)
    motionProxy.setAngles("RShoulderPitch", 30 * almath.TO_RAD, 1)
    motionProxy.setAngles("RElbowYaw", 70 * almath.TO_RAD, 1)
    #motionProxy.setAngles("LHipPitch", -30 * almath.TO_RAD, fractionMaxSpeed)
        
#    effector = "LArm"
#    frame = motion.FRAME_ROBOT
#    axisMask = almath.AXIS_MASK_VEL
#    useSensorValues = False
#    
#    path = []
#    currentTf = motionProxy.getTransform(effector, frame, useSensorValues)
#    targetTf = almath.Transform(currentTf)
#    #targetTf.r1_c4 += 1 #x
#    #targetTf.r2_c4 += 1 #y
#    
#    path.append(list(targetTf.toVector()))
#    #path.append(currentTf)
#    
#    # times to go to the target and back
#    times = [2.0, 4.0]
#    
#    motionProxy.transformInterpolations(effector, frame, path, axisMask, times)
    
    #motionProxy.rest()
    
if __name__ == "__main__":
    main("138.110.234.37", 9559)
