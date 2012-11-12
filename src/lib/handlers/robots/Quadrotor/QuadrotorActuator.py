#!/usr/bin/env python
"""
===================================================
QuadrotorActuator.py - Quadrotor's Actuator Handler
===================================================
The actions for the Quadrotor.
"""

import math
import time
import thread

class actuatorHandler:

    # Change height settings
    stepSize = .05
    timeInt = .5
    
    OVERRIDE = 9.87654321

    def __init__(self, proj, shared_data):
        self.loco = None
        self.pose = None
        self.MAINTAIN = None

#        # Get reference to other handlers
#        try:
#            self.loco = proj.h_instance['locomotionCommand']
#            self.MAINTAIN = self.loco.MAINTAIN
#        except:
#            print "(DRIVE) ERROR: Locomotion Command Handler not found."
#        try:
#            self.pose = proj.h_instance['pose']
#        except:
#            print "(DRIVE) ERROR: Pose Handler not found."
#            
#            
#            
#    def changeHeight(self, desZ, actuatorVal, initial=False):
#        """
#        Changes the height that the quadrotor is flying height
#        
#        desZ (float): The height to change to (default=.5) 
#        """
#        
#        if initial or int(actuatorVal) == 0:
#            return
#        
#        if desZ < self.loco.MIN_Z or desZ > self.loco.MAX_Z:
#            return
#        
#        if self.loco.state == "FLYING" or actuatorVal == self.OVERRIDE:
#            self.loco.state = "ACTUATION"
#            (cX, cY, cYaw, cZ) = self.pose.getPose()            
#            disp = desZ - cZ
#            stepDir = disp / math.fabs(disp) * self.stepSize 
#            numSteps = int(math.fabs(disp) / self.stepSize)
#                        
#            for step in range(numSteps):
#                if self.loco.state != "ACTUATION":
#                    return
#                
#                self.loco.setRefPos(cX, cY, cZ + stepDir * (step + 1),  cYaw)
#                time.sleep(self.timeInt)
#            
#            if self.loco.state != "ACTUATION":
#                return
#            self.loco.setRefPos(cX, cY, desZ,  cYaw)
#            time.sleep(self.timeInt) 
#            
#            self.loco.flyHeight = desZ
#            self.loco.state = "FLYING"
#                
#                
#    
#    def changeYaw(self, yaw, angS, actuatorVal, initial=False):
#        """
#        Changes the direction the quadorotr is facing
#        
#        yaw (float): The direction to face towards (default=0)
#        angS (float): The angular speed to turn at (default=.785)
#        """
#        if initial or int(actuatorVal) == 0:
#            return
#        
#        if self.loco.state == "FLYING" or actuatorVal == self.OVERRIDE:
#            self.loco.state = "ACTUATION"
#            self.loco.setRefPos(self.MAINTAIN, self.MAINTAIN, 
#                                self.MAINTAIN, yaw)
#            time.sleep(3)
#            self.loco.state = "FLYING"
#    
#    def lookLeftAndRight(self, actuatorVal, initial=False):
#        """
#        Tells the robot to look left 90 degrees and right 90 degrees 
#        """
#        pass
#    
#    def spin(self, actuatorVal, initial=False):
#        """
#        Make the robot spin in a complete circle 
#        """
#        pass
#    
#    def bobUpAndDown(self, actuatorVal, initial=False):
#        """
#        Tell the robot to move up and down
#        """
#        repetitions = 5
#        distance = .2
#        pass
#    
    
    
