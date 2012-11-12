#!/usr/bin/env python
# -*- coding: cp1252 -*-
"""
================================================================================
QuadrotorLocomotionCommand.py - The Quadrotor's Locomotion Command Handler
================================================================================
Handles communications to QuadrotorControl.exe and stores the current state of
the robot.
"""
import numpy
import thread
import threading
import time
import struct

class locomotionCommandHandler:
    """
    List of possible states:
        OFF         - Motors are toggled off
        TAKING_OFF  - Bird is taking off
        FLYING      - Bird is currently flying and ready to receive commands
        ACTUATION   - Actuator Handler is currently doing something
        LANDING     - Bird is landing

        NOTE: Whoever wrote QuadrotorControl.exe did not account for the state
        where the quadrotor is on the ground but with the motors on thus it must
        also be ignored here.
    """

    MAINTAIN = 120      # Will maintain the current position value

    MAX_CHANGE = .5     # Max displacement allowed

    MAX_Z = .95
    MIN_Z = .15

    def __init__(self, proj, shared_data):

        self.pose = None                    # Reference to pose handler
        self.state = None                   # The current state of the quadrotor
        self.stateLock = threading.Lock()
        self.headers = None                 # Command headers

        self.cmdPipe = None                 # Pipe for sending commands
        self.statePipe = None               # Pipe for getting quadrotor state

        self.flyHeight = .5

        # Get needed shared data
        try:
            self.headers = shared_data["Headers"]
            self.cmdPipe = shared_data["CommandPipe"]
            self.statePipe = shared_data["StatePipe"]
        except:
            print "(LOCO) ERROR: No shared data"

        # Get reference to pose handler
        try:
            self.pose = proj.h_instance['pose']
        except:
            print "(LOCO) ERROR: Pose Handler not found."

        # Start the state update thread
        thread.start_new_thread(self.stateUpdateFunc, ())



    def stateUpdateFunc(self):
        """
        Will continiously check for updates on the state from
        QuadrotorControl.exe. It will then translate the state to an equivalent
        state to allow additional states on the LTLMoP side.
        NOTE: It is important that this be updated for new states
        """
        while True:
            newState = self.statePipe.recv()

            with self.stateLock:
                
                if newState == "OFF":
                    self.state = "OFF"

                elif (newState == "TURNING_ON" or newState == "WAITING" or
                        newState == "TAKING_OFF"):
                    self.state = "TAKING_OFF"

                elif newState == "ACCEPTING_COMMANDS":
                    if self.state != "FLYING" and self.state != "ACTUATION":
                        self.state = "FLYING"

                elif newState == "LANDING" or newState == "SHUTTING_DOWN":
                    self.state = "LANDING"
                    
                else:
                    print "(THREAD) WARNING: Not a valid state"


    def takeOff(self):
        """
        Tells the bird to take off
        """
        if self.state == "OFF":
            currPose = self.pose.getPose()
            self.setRefPos(currPose[0], currPose[1], .5, currPose[3],
                            tkOffCmd=True)
            time.sleep(1)
            self.cmdPipe.send(self.headers["TAKE_OFF"])


    def land(self):
        """
        Tells the bird to land
        """
        if self.state == "LANDING" or self.state == "OFF":
            return

        self.cmdPipe.send(self.headers["LAND"])


    def setRefPos(self, x, y, z, yaw, tkOffCmd=False):
        """
        Send the desired reference pose to the QuadrotorControl software.
        """
        curPose = self.pose.getPose()
        posVec = numpy.array([curPose[0], curPose[1], curPose[2]])

        # Replace MAINTAIN values with current values
        if x == self.MAINTAIN:
            x = curPose[0]
        if y == self.MAINTAIN:
            y = curPose[1]
        if z == self.MAINTAIN:
            z = curPose[2]
        if yaw == self.MAINTAIN:
            yaw = curPose[3]

        # Assure that the displacement is not too large
        if self.dispTooLarge(numpy.array([x, y, z]), posVec):
            print "(LOCO) WARNING: Displacement was too large"
            return

        # Put yaw into the correct range -pi to pi
        while yaw > numpy.pi:
            yaw = yaw - 2 * numpy.pi
        while yaw < -numpy.pi:
            yaw = yaw + 2 * numpy.pi

        cmd = self.headers["POSITION"] + struct.pack('ffff', x, y, z, yaw)
        self.cmdPipe.send(cmd)


    def dispTooLarge(self, v1, v2):
        """
        True if the displacement is larger than the allowed max
        """
        d = v1 - v2
        mag = numpy.sqrt(numpy.vdot(d, d))
        if mag > self.MAX_CHANGE:
            return True
        else:
            return False

