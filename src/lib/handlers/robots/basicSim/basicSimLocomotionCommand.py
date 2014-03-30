#!/usr/bin/env python
# -*- coding: cp1252 -*-
"""
================================================================================
basicSimLocomotionCommand.py - Basic Simulation Locomotion Command Handler
================================================================================
"""
from random import gauss

class locomotionCommandHandler:
    def __init__(self, proj, shared_data,speed):
        """
        LocomotionCommand Handler for basic simulated robot.

        speed (float): The speed multiplier (default=1.0,min=6.0,max=15.0)
        """
        self.speed = speed
        try:
            self.simulator = shared_data['BasicSimulator']
        except KeyError:
            print "(Loco) ERROR: Basic Simulator doesn't seem to be initialized!"
            sys.exit(-1)
        
    def sendCommand(self, cmd):
        addNoise = False
        
        if addNoise:
            cmd[0] += cmd[0] * gauss(0, .1)
            cmd[1] += cmd[1] * gauss(0, .3)
#             cmd[0] += gauss(0, .1)
#             cmd[1] += gauss(0, .3)

        v = self.speed*cmd[0]
        w = self.speed*cmd[1]
        self.simulator.setVel([v,w])
                       
