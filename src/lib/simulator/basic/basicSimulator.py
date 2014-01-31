#!/usr/bin/env python
"""
================================================================
basicSimulator.py -- A simple robot simulator provides pose by integrating given locomotion cmd
================================================================
"""

import numpy as np
from threading import Lock, _start_new_thread
import time, sys

class basicSimulator:
    def __init__(self, init_pose, type):
        """
        Initialization handler for a holonomic or differential drive robot.

        :param init_pose: a 1-by-3 vector [x,y,orintation]
        :param type: 0 - holonomic, 1 - differential drive        
        """
        # SETTINGS
        self.updateInterval = .1    # The max time to wait between intervals
        self.inertia = 1 # scale from 0 to 1, the bigger the scale the smaller the "inertia" is

        print "(Basic Simulator) Initializing Basic Simulator..."
        self.type = type    # Holonomic or differential drive
        self.pose = np.array(init_pose) # current pose
        self.curVel = np.array([0.0,0.0]) # current velocity
        self.updateTime = None  # The time of the last update

        # Choose a timer func with maximum accuracy for given platform
        if sys.platform in ['win32', 'cygwin']:
            self.timer_func = time.clock
        else:
            self.timer_func = time.time

        print "(Basic Simulator) Start Basic Simulator..."
        self.simMutex = Lock()
        self.updateTime = self.timer_func()
        _start_new_thread(self.runSimulation, () )

    def getPose(self):
        """ Returns the current pose of the robot """
        return self.pose

    def setVel(self,cmd):
        """
        Set the velocity of the robot, update the pose by integrating the velocity

        :param cmd: can be a numpy array with [xVelocity, yVelocity] or 
                    [linearVelocity, angularVelocity] depending on robot type.
        """
        self.updatePose()
        
        # assume the velocity takes times to change (avoids local minimum)
        self.curVel = self.inertia*np.array(cmd)+(1-self.inertia)*self.curVel

    def runSimulation(self):
        """ Updates the simulator at the desired time interval """
        while True:
            self.updatePose()
            time.sleep(self.updateInterval)
            
    def updatePose(self):
        """ Updates pose depending on robot type """
        with self.simMutex:
            timeSpan = self.timer_func() - self.updateTime
            
            # Holonomic
            if self.type == 0:
                self.pose[:2] += self.curVel[:2] * timeSpan
            
            # Differential drive
            elif self.type == 1:
                self.pose[:3] = self.integrateForwardsDifferential(self.pose[:3], 
                                self.curVel[0], self.curVel[1], timeSpan)
            
            # Error
            else:
                print "Error: BasicSim - Incorrect robot type."
            
            self.updateTime = self.timer_func()
            
    def integrateForwardsDifferential(self, posePrev, u, w, delT):
        """ Calculate the robots new pose based on the previous position,
        controls, and time elapsed. Assumes differential drive.
        
        :param posePrev: numpy 3D array. The previous pose
        :param u: linear velocity
        :param w: angular velocity
        :param delT: time elapsed
        :return: poseN: the new pose of the robot
        """
        poseN = np.array(posePrev)
        
        delAng = w*delT
        dist = u*delT
        
        if np.abs(delAng) < .0000001:
            poseN[0] += dist*np.cos(posePrev[2])   
            poseN[1] += dist*np.sin(posePrev[2])
        else:
            # Radius of circle and length of displacement vector
            rad = dist/delAng;
            vecL = np.sqrt( (rad*np.sin(delAng))**2 + (rad - rad*np.cos(delAng))**2) * np.sign(dist)
            
            poseN[0] += vecL*np.cos(delAng/2 + poseN[2])
            poseN[1] += vecL*np.sin(delAng/2 + poseN[2])
            poseN[2] = (poseN[2] + delAng)%(2*np.pi)
            
        return poseN


