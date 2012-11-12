#!/usr/bin/env python
"""
============================================
viconPose.py - Pose Handler for Vicon System
============================================
"""
from numpy import array
import _pyvicon

class poseHandler:
    def __init__(self, proj, shared_data,host,port,x_VICON_name,y_VICON_name,theta_VICON_name, z_VICON_name="None"):
        """
        Pose handler for VICON system

        host (string): The ip address of VICON system (default="10.0.0.102")
        port (int): The port of VICON system (default=800)
        x_VICON_name (string): The name of the stream for x pose of the robot in VICON system (default="SubjectName:SegmentName <t-X>")
        y_VICON_name (string): The name of the stream for y pose of the robot in VICON system (default="SubjectName:SegmentName <t-X>")
        theta_VICON_name (string): The name of the stream for orintation of the robot in VICON system (default="SubjectName:SegmentName <a-Z>")
        z_VICON_name (string): The name of the stream for z pose of the robot in VICON system (default="None")
        """

        self.host = host
        self.port = port
        self.x = x_VICON_name
        self.y = y_VICON_name
        self.theta = theta_VICON_name
        self.z = z_VICON_name

        self.threeD = None
        if self.z == "None":
            self.threeD = False
        else:
            self.threeD = True

        self.s = _pyvicon.ViconStreamer()
        self.s.connect(self.host,self.port)

        if self.threeD:
            self.s.selectStreams(["Time", self.x, self.y, self.z, self.theta])
        else:
            self.s.selectStreams(["Time", self.x, self.y, self.theta])

        self.s.startStreams()

        # Wait for first data to come in
        while self.s.getData() is None: pass
    
    def _stop(self):
        print "Vicon pose handler quitting..."
        self.s.stopStreams()
        print "Terminated."
        
    def getPose(self, cached=False):

        if self.threeD:
            (t, x, y, z, o) = self.s.getData()
            (t, x, y, z, o) = [t/100, x/1000, y/1000, z/1000, o]
            return array([x, y, z, o])
        else:
            (t, x, y, o) = self.s.getData()
            (t, x, y, o) = [t/100, x/1000, y/1000, o]
            return array([x, y, o])

