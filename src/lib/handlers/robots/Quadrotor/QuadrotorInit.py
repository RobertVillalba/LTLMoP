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
    place a message of connecting to the pipes
    ask if there is a better way to check on the state
    update the robot file
    TCP pipes dont close on clean exit must kill spec
    Too many quadrotorcontroll.exe running on task
    Do we want to have a semi fixed fly height and fly yaw?

LTLMoP ISSUES:
    If input for config has something wrong spec does not open to allow change
    Have an off function to close the pipes and other commands?

'''


class initHandler:

    

    # Headers for the commands
    headers = {"POSITION": '\xa0\xf0', "TOGGLE": '\xa0\xf1', "TAKE_OFF": '\xa0\xf2',
                "LAND": '\xa0\xf3'}

    def __init__(self, proj, path=None, comPort="COM3", vicSubj="Quadrotor01",
                 vicIP='10.0.0.102', vicPort=800):
        """
        The initialization for the Quadrotor

        path (string): The path to QuadrotorControl.exe. If None will throw exception. (default="")
        comPort (string): The com port to the xBee (default=COM3)
        vicSubj (string): The vicon subject for the robot (default="Quadrotor01")
        vicIP (string): The IP address for vicon (default="10.0.0.102")
        vicPort (int): The port for vicon (default=800)
        """
        self.finishedSetup = False   # Will be set to true once C# finishes

        self.setPipe = None     # The pipe used for setup
        self.cmdPipe = None     # The pipe used to send commands
        self.statePipe = None   # The pipe used to receive the state

        print "OPENING PIPES"

        # Open TCP ports
        try:
            context = zmq.Context()
            self.setPipe = context.socket(zmq.REP)
            self.setPipe.bind("tcp://*:5555")

            context = zmq.Context()
            self.cmdPipe = context.socket(zmq.PUB)
            self.cmdPipe.bind("tcp://*:5556")

            context = zmq.Context()
            self.statePipe = context.socket(zmq.SUB)
            self.statePipe.bind("tcp://*:5557")
            self.statePipe.setsockopt(zmq.SUBSCRIBE, b"")
        except:
            print "(INIT) ERROR: Could not open TCP pipes"
            
        print "STARTED SETUP"

        self.runSetup(comPort, vicSubj, vicIP, vicPort)
        time.sleep(1)

        # QuadrotorControl.exe
        if path == None:
            raise Exception("Path to QuadrotorControl.exe is undefined")
        try:
            self.openQuadController(path)
        except:
            print "(INIT) ERROR: Could not open QuadrotorControler.exe"
            
        print "WAITING FOR QUAD TO FINISH"

        # Wait until QuadrotorControl is done
        while not(self.finishedSetup):
            time.sleep(.1)

        print "QUAD FINISHED"


    def getSharedData(self):
        """
        Return a dictionary of any objects that will need to be shared with
        other handlers
        """
        return {"Headers": self.headers, "CommandPipe": self.cmdPipe,
                "StatePipe":self.statePipe}

    def runSetup(self, comPort, vicSubj, vicIP, vicPort):
        """
        Run the setup thread.

        @param comPort: String
        @param vicSubj: String
        @param vicIp: String
        @param vicPort: Int
        """
        thread.start_new_thread(self.runSetupThreadFunc, (comPort, vicSubj,
                                                          vicIP, vicPort))

    def runSetupThreadFunc(self, comPort, vicSubj, vicIP, vicPort):
        """
        Supplies all the needed setup information to QuadrotorControl.exe
        """
        msgIn = ("cp", "vs", "vi", "vp")
        msgOut = (comPort, vicSubj, vicIP, str(vicPort))

        for i in range(4):
            msg = self.setPipe.recv()
            if msg != msgIn[i]:
                raise Exception("(INIT) QuadrotorControl message was not " \
                                "what was expected")
            self.setPipe.send(msgOut[i])

        # Wait for finished confirmation
        msg = self.setPipe.recv()
        if msg != "done":
            raise Exception("(INIT) Did not receive 'done' from " \
                            "QuadrotorControl.exe")
        self.finishedSetup = True

    def openQuadController(self, path):
        """
        Runs the C# software that controls the quadrotor on a separate thread.
        """
        thread.start_new_thread(self.programThreadFunc, (path, 0))

    def programThreadFunc(self, path, *arg):
        """
        Called by openQuadController
        """
        os.system(path)

# TODO: REMOVE AFTER DONE DEBUGGING 
#def test():
#    path = "C://Users//rdv28//Dropbox//ASL//VisualStudio//CS_Development//Quadrotors//QuadrotorControl//QuadrotorControl//bin//Debug//QuadrotorControl.exe"
#    initObj = initHandler(None, path)
