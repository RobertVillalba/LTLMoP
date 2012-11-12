#!/usr/bin/env python
"""
================================================================================
QuadrotorInit.py -- Quadrotor Initialization Handler
================================================================================
This class will take care of running the C# QuadrotorControll and
establishing TCP connection with it among other things.
"""

import time
import os
import thread
import zmq


'''
TODO:
    sync states
    open extra pipes
    actuators on separate threads
        enums for states
    If more states are added in much of the code needs to change. Any way around this?
        add actuation
        add check for lock
    Place some notes on quadrotor small movements
    Insert safeties in Locomotion for step size
    Change MAINTAING POSITION TO A CONSTATNT and do the calculation on loco
    can you make actuator methods that do not appear on ltlmop?
        ~~~~ use underscore
    change the zPose setup
    change eToggle to eStop
    if you were activating stay there

LTLMoP ISSUES:
    Calibration tool freezes when pressed quit button
    Configurations will not be deleated when I click delete and ok
    Sensor 0Button gave error (sensors starting with numbers?)
'''


class initHandler:

    quadControlPath = "C://Users//rdv28//Dropbox//ASL//CS_Development//Quadrotors//" \
              "QuadrotorControl//QuadrotorControl//bin//Debug//QuadrotorControl.exe"

    # Headers for TCP
    headers = {"POSITION": '\xa0\xf0', "TOGGLE": '\xa0\xf1', "TAKE_OFF": '\xa0\xf2',
                "LAND": '\xa0\xf3'}

    def __init__(self, proj, path=None, comP="COM3", vicSubj="Quadrotor01"):
        """
        The initialization for the Quadrotor

        path (string): The path to QuadrotorControl.exe. If None will throw exception
        comP (string): The com port to the xBee (default=COM3)
        vicSubj (string): The vicon subject for the robot (default="Quadrotor01")
        """
        self.quadController = None      # The TCP port to connect to the controller

        if path == None:
            raise Exception("Path to QuadrotorControl.exe is undefined")
        try:
            self.openQuadController()
        except:
            print "(INIT) ERROR: Could not open QuadrotorControler.exe"

        # TCP port
        try:
            context = zmq.Context()
            self.quadController = context.socket(zmq.PUB)
            self.quadController.bind("tcp://*:5555")
            # TODO: MODIFY TIME NEEDED
            time.sleep(.5)
        except:
            print "(INIT) ERROR: Could not open TCP port"



    def getSharedData(self):
        """
        Return a dictionary of any objects that will need to be shared with
        other handlers
        """
        return {"Headers": self.headers, "QuadController": self.quadController}

    def openQuadController(self):
        """
        Runs the C# software that controls the quadrotor on a separate thread.
        """
        thread.start_new_thread(self.programThredFunc, (self.quadControlPath, 0))

    def programThredFunc(self, path, *arg):
        """
        Called by openQuadController
        """
        os.system(path)

