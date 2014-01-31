#!/usr/bin/env python
"""
=================================================
differentialDrive.py - Differential Drive Handler
=================================================

Converts a desired global velocity vector into translational and rotational rates for a differential-drive robot,
using feedback linearization.
"""

from math import sin, cos

class driveHandler:
    def __init__(self, proj, shared_data,velScale,d=0.6):
        """
        Initialization method of differential drive handler.

        velScale (float): Will scale the incoming velocities by this much. (default=.29)
        d (float): Distance from front axle to point we are abstracting to [m] (default=0.6,max=0.8,min=0.2)
        """   

        try:
            self.loco = proj.h_instance['locomotionCommand']
            self.coordmap = proj.coordmap_lab2map
        except NameError:
            print "(DRIVE) Locomotion Command Handler not found."
            exit(-1)

        self.velScale = velScale
        self.d = d
        
    def setVelocity(self, x, y, theta=0):
        #print "VEL:%f,%f" % tuple(self.coordmap([x, y]))

        # Feedback linearization code:
        vx = self.velScale*x
        vy = self.velScale*y
        w = (1/self.d)*(-sin(theta)*vx + cos(theta)*vy)
        v = cos(theta)*vx + sin(theta)*vy

        self.loco.sendCommand([v,w])

