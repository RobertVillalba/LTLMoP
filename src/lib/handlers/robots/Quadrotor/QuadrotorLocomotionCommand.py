#!/usr/bin/env python
# -*- coding: cp1252 -*-
"""
================================================================================
QuadrotorLocomotionCommand.py - The Quadrotor's Locomotion Command Handler
================================================================================
Handles communications to QuadrotorControl.exe and stores the current state of
the robot.
"""
import math
import thread
import time
import struct
import wx

class locomotionCommandHandler:
    """
    List of possible states:
        OFF         - Motors are toggled off
        TURNING_OFF - Motors are turning off (wait until finished)
        LANDED      - Motors are toggled on but not flying
        TAKING_OFF  - Bird is taking off (don't send position commands)
        LANDING     - Bird is landing (don't send position commands)
        FLYING      - Bird is currently flying (ready for position commands)
        ACTUATION   - Actuator Handler is currently in control
        LOCKED      - Emergency toggle was called. Do nothing until called again
    """

    takeOffTime = 10        # The number of seconds it takes to safely take off
    landTime = 10           # The number of seconds it takes to safely land

    MAX_POS = 100           # Any position greater than this will be ignored
                            # in the QuadrotorControl software

    MAINTAIN = 120
    
    MAX_Z = .95
    MIN_Z = .15

    def __init__(self, proj, shared_data):

        self.pose = None         # Reference to pose handler
        self.state = "OFF"       # The current state or action being performed
        self.headers = None
        self.quadController = None
        self.flyHeight = .5

        # Get needed shared data
        try:
            self.headers = shared_data["Headers"]
            self.quadController = shared_data["QuadController"]
        except:
            print "(LOCO) ERROR: No shared data"

        # Get reference to other handlers
        try:
            self.pose = proj.h_instance['pose']
        except:
            print "(LOCO) ERROR: Pose Handler not found."

        # Start Control GUI
        thread.start_new_thread(self.openGui, ())
        
  
  
    def openGui(self):
        app = wx.PySimpleApp()
        window = _PythonQuadControl(self)
        app.MainLoop()


    def turnOff(self):
        """
        Land the bird and turn off the motors safely. Non blocking.
        """
        thread.start_new_thread(self.turnOffTFun, ())


    def turnOffTFun(self):
        """
        Takes the necessary steps to turn off the bird regardless of its state.
        To be called by a separate thread.
        """
        if self.state == "LOCKED" or self.state == "OFF":
            return

        oldState = self.state
        self.state = "TURNING_OFF"

        # Run through the necessary steps
        if oldState == "TAKING_OFF":
            time.sleep(self.takeOffTime)
            oldState = "FLYING"

        if oldState == "FLYING":
            self.quadController.send(self.headers["LAND"])
            oldState = "LANDING"

        if oldState == "LANDING":
            time.sleep(self.landTime)
            oldState = "LANDED"

        if oldState == "LANDED":
            self.quadController.send(self.headers["TOGGLE"])
            time.sleep(.1)

        self.state = "OFF"


    def toggleMotors(self):
        """
        Will turn the motors off if they are on or on if they are off. Only
        if bird is not flying.
        """
        if self.state == "OFF":
            self.quadController.send(self.headers["TOGGLE"])
            time.sleep(.1)
            self.state = "LANDED"
        elif self.state == "LANDED":
            self.quadController.send(self.headers["TOGGLE"])
            time.sleep(.1)
            self.state = "OFF"


    def eToggle(self):
        """
        Will turn off the motors if they are on and enter a locked state
        where only a call o this function again will change.
        """
        print self.state
        
        if self.state == "OFF":
            print "did nothing"
            return
        elif self.state == "LOCKED":
            print "just removed the lock"
            self.state = "OFF"
        else:
            self.quadController.send(self.headers["TOGGLE"])
            self.state = "LOCKED"
            time.sleep(.1)
            print "toggled motors and went into locked mode"


    def takeOff(self):
        """
        Tells the bird to take off and waits for a given amount of time
        before changing the state to FLYING
        """
        # C# must take off from the off mode
        if self.state == "LANDED":
            self.toggleMotors()
            self.state = "OFF"

        if self.state == "OFF":
            currPose = self.pose.getPose()
            self.setRefPos(currPose[0], currPose[1], .5, currPose[2])
            time.sleep(1)

            self.quadController.send(self.headers["TAKE_OFF"])
            self.state = "TAKING_OFF"
            thread.start_new_thread(self.changeStateHFun, ("TAKING_OFF",
                                                "FLYING", .4, 0))


    def land(self):
        """
        Tells the bird to land and waits for a given amount of time before
        changing states to OFF. Only if it is in flying mode.
        """
        
        if self.state == "FLYING":
            self.quadController.send(self.headers["LAND"])
            self.state = "LANDING"
            thread.start_new_thread(self.changeStateHFun, ("LANDING", "OFF",
                                                           .1, 0))


    def changeStateTFun(self, oState, nState, delay, *args):
        """
        Waits for the given amount of time before it changes the state
        to the new one. If the state is changed by some other process during
        the delay, this thread will not do anything. This should be called
        by a separate thread.
        @param oState: A string with the old state
        @param nState: A string with the new state
        @param delay: A double, the time to wait for in seconds
        """
        time.sleep(delay)
        if self.state == oState:
            self.state = nState
            
    def changeStateHFun(self, oState, nState, height, *args):
        """
        Waits untill it reaches the desired height before changing the state
        to the new one. If the state is changed by some other process during
        the wait, this thread will not do anything. This should be called
        by a separate thread.
        @param oState: A string with the old state
        @param nState: A string with the new state
        @param height: A double, the height to reach in meters
        """
        aprox = .05     # Distance from goal that is considered ok
        
        (x, y, yaw, z) = self.pose.getPose()
        while math.fabs(z - height) > aprox and self.state == oState: 
            time.sleep(.01)
            (x, y, yaw, z) = self.pose.getPose()
        
        time.sleep(1)
        if self.state == oState:
            self.state = nState

    def setRefPos(self, x, y, z, yaw):
        """
        Send the desired reference pose to the QuadrotorControl software.
        """
        if yaw < self.MAX_POS:
            while yaw > math.pi:
                yaw = yaw - 2 * math.pi
            while yaw < -math.pi:
                yaw = yaw + 2 * math.pi
        
        cmd = self.headers["POSITION"] + struct.pack('ffff', x, y, z, yaw)
        self.quadController.send(cmd)



"""
================================================================================
PythonQuadcontrol
================================================================================
This class will allow control for taking off, landing, toggling motors, and
an emergency toggle.
"""
class _PythonQuadControl(wx.Frame):


    bWidth = 290
    bHeight = 50

    def __init__(self, locoHandler):

        self.loco = locoHandler

        wx.Frame.__init__(self, None, wx.ID_ANY, 'wxButton',
            pos = (300, 150), size = (320, 260))

        self.button1 = wx.Button(self, id = -1, label = 'Take Off',
                       pos = (8, 8), size = (self.bWidth, self.bHeight))
        self.button1.Bind(wx.EVT_BUTTON, self.button1Click)

        self.button2 = wx.Button(self, id = -1, label = 'Land',
                       pos = (8, 60), size = (self.bWidth, self.bHeight))
        self.button2.Bind(wx.EVT_BUTTON, self.button2Click)

        self.button3 = wx.Button(self, id =  -1, label = 'Toggle',
            pos = (8, 112), size = (self.bWidth, self.bHeight))
        self.button3.Bind(wx.EVT_BUTTON, self.button3Click)

        self.button4 = wx.Button(self, id = -1, label = 'EmergencyToggle',
            pos = (8, 164), size = (self.bWidth, self.bHeight))
        self.button4.Bind(wx.EVT_BUTTON, self.button4Click)

        # show the frame
        self.Show(True)

    def button1Click(self,event):
        self.loco.takeOff()

    def button2Click(self,event):
        self.loco.land()

    def button3Click(self,event):
        self.loco.toggleMotors()

    def button4Click(self, event):
        self.loco.eToggle()



