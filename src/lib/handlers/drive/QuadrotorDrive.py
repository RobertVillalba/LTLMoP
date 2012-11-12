#!/usr/bin/env python
"""
==================================================
QuadrotorDrive.py - DriveHandler for the Quadrotor
==================================================
Converts a desired global velocity vector into a desired location and
applies a state machine.
"""

from numpy import array, sqrt, vdot
import time

class driveHandler:

#    distScale = .03     # Weight for calculated displacement 
#    timeInt = .25       # Time alloted per change in position
    
    distScale = .02     # Weight for calculated displacement 
    timeInt = .3       # Time alloted per change in position

    def __init__(self, proj, shared_data):

        self.loco = None        # Reference to locomotion handler
        self.pose = None        # Reference to pose handler
        self.timeElap = time.clock()

        # Get reference to other handlers
        try:
            self.loco = proj.h_instance['locomotionCommand']
        except:
            print "(DRIVE) ERROR: Locomotion Command Handler not found."
        try:
            self.pose = proj.h_instance['pose']
        except:
            print "(DRIVE) ERROR: Pose Handler not found."
            
        self.newPose = self.getPosition()
        self.newDir = array([0, 0])
        


    def setVelocity(self, x, y, theta=0):
        """
        This method will take the velocity only for its direction. It will
        then tell the robot to step by the desired interval in that
        direction
        """    
        
        oldPose = self.newPose
        oldDir = self.newDir
        self.newPose = self.getPosition()
        self.newDir = self.normalise(array([x, y]))
                
        if (self.getMagnitude(self.newDir) == 0 or 
                    not(self.loco.state == "FLYING") or
                    (time.clock() - self.timeElap) < self.timeInt):
            time.sleep(.01)
            return
                
        disp = self.normalise(self.newPose - oldPose)
        desPos = ((oldDir - disp + self.newDir) * self.distScale + 
                    self.newPose)
        self.loco.setRefPos(desPos[0], desPos[1], self.loco.flyHeight,
                                self.loco.MAINTAIN)
        self.timeElap = time.clock()
   
        """
#        OLD CODE
        
        vicPose = self.pose.getPose()
        currPos = array([vicPose[0], vicPose[1]])

        dispVec = array([x,y])
        dispMag = sqrt(vdot(dispVec,dispVec))
        
        if dispMag == 0 or (time.clock() - self.timeElap) < self.timeInt:
            return

        desPos = currPos + (dispVec / dispMag * self.distScale)

        if self.loco.state == "FLYING":
            self.loco.setRefPos(desPos[0], desPos[1], self.loco.MAINTAIN_POS,
                                self.loco.MAINTAIN_POS)
            self.timeElap = time.clock()
        """

    def getPosition(self):
        """
        Give the position of the robot as a vector with x, y
        """
        vicPose = self.pose.getPose()
        return array([vicPose[0], vicPose[1]])

    def normalise(self, vec):
        """
        Turn a vector into a unit vector. If it is the 0 vector
        just returns it
        """
        if self.getMagnitude(vec) == 0:
            return vec
        return vec/self.getMagnitude(vec)
    
    def getMagnitude(self, vec):
        """
        Returns the magnitude of a vector 
        """
        return sqrt(vdot(vec,vec))







