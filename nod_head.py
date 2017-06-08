import argparse
import time
import random
from naoqi import ALProxy

robotIP = 'nico.d.mtholyoke.edu'
PORT = 9559
count = 0
motionProxy  = ALProxy("ALMotion", robotIP, PORT)
postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

r_shoulder = ['RShoulderPitch', 'RShoulderRoll']
l_shoulder = ['LShoulderPitch', 'LShoulderRoll']
l_elbow = ['LElbowYaw', 'LElbowRoll']
r_elbow = ['RElbowYaw', 'RElbowRoll']
#names = ['HeadYaw', 'HeadPitch']

times = [[0.5], [0.5]]

for i in range(2):
#motionProxy.angleInterpolation(names, [0.0, 0.0], times, True)
	motionProxy.angleInterpolation(r_shoulder, [-1.0, 0.0], times, True)
	motionProxy.angleInterpolation(r_shoulder, [-0.5, -0.5], times, True)
	

#motionProxy.angleInterpolation(l_shoulder, [0.0, -0.3], times, True)
#motionProxy.angleInterpolation(l_elbow, [-1, -0.02], times, False)
#motionProxy.angleInterpolation(r_elbow, [1,  0.02], times, False)


'''
for i in range(2):
	#nodding head; positive - downward
    motionProxy.angleInterpolation(right_names, [0.0, -1.0], times, True)
    motionProxy.angleInterpolation(left_names, [0.0, 1.0], times, True)

#motionProxy.angleInterpolation(names, [0.5, -0.5], times, True)

'''
'''
while count < 2:
	
	motionProxy.setAngles("HeadPitch", 0.2, 0.6)

	#motionProxy.setAngles("HeadYaw", 0.4, 0.6)
	motionProxy.setAngles("HeadPitch", -0.2, 0.6)
	time.sleep(2)
	count+=1'''
