#!/usr/bin/env python

"""
=================================================
QuadrotorSensor.py - Sensor Handler for Quadrotor
=================================================
"""
import threading
#import cv2.cv as cv

class sensorHandler:
    
    def __init__(self, proj, shared_data):
        self.leftlimit = 300
        self.rightlimit = 340
        self.abovelimit = 230
        self.belowlimit = 250
        # if tracked object is in box at (300-340, 230-250)
        # then robot believes object is in camera's center         
#        self.obj = _objTracked()
#        self.colorT = _colorTracker(self.obj)
#        self.colorT.start()
#        
#        ###################################
#        ### Available sensor functions: ###
#        ###################################
#        
#    def trackColor(self, hueMin, hueMax, initial = False):
#        """
#        Uses the quadrotor's onboard camera to track a color.
#        
#        hueMin (int): lower value of hue range to detect (default=140)
#        hueMax (int): upper value of hue range to detect (default=180)
#        """
#		 if initial:
#			 return False
#        self.colorT.hueMin = hueMin
#        self.colorT.hueMax = hueMax
#        if self.colorT.obj.objArea > 100000:
#            return True
#        return False
#        
#    def isLeft(self, initial = False):
#        """
#        Checks if the object being tracked is to the camera's left.
#        """
#		 if initial:
#			 return False
#        if self.colorT.obj.objX < self.leftlimit:
#            return True
#        return False
#    
#    def isRight(self, initial = False):
#        """
#        Checks if the object being tracked is to the camera's right.
#        """
#		 if initial:
#			 return False
#        if self.colorT.obj.objX > self.rightlimit:
#            return True
#        return False
#    
#    def isAbove(self, initial = False):
#        """
#        Checks if the object being tracked is above camera's center.
#        """
#		 if initial:
#			 return False
#        if self.colorT.obj.objY < self.abovelimit:
#            return True
#        return False
#    
#    def isBelow(self, initial = False):
#        """
#        Checks if the object being tracked is below camera's center.
#        """
#		 if initial:
#			 return False
#        if self.colorT.obj.objY > self.belowlimit:
#            return True
#        return False
#
#class _objTracked:
#    objX = None
#    objY = None
#    objArea = None
#
#class _colorTracker(threading.Thread):
#         
#    def __init__(self, o): 
#        #o is an objTracked object being color tracked
#        threading.Thread.__init__(self)
#        self.hueMin = 140
#        self.hueMax = 180
#        self.obj = o
#    
#    def run(self): 
#        color_tracker_window = "Eye of the Hummingbird"
#        cv.NamedWindow(color_tracker_window, 1 ) 
#        self.capture = cv.CaptureFromCAM(1)
#        
#        while True: 
#            newObj = _objTracked() 
#            img = cv.QueryFrame( self.capture ) 
#                        
#            #blur the source image to reduce color noise 
#            cv.Smooth(img, img, cv.CV_BLUR, 3); 
#            
#            #convert the image to hsv(Hue, Saturation, Value) so its  
#            #easier to determine the color to track(hue) 
#            hsv_img = cv.CreateImage(cv.GetSize(img), 8, 3) 
#            cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV) 
#            
#            #limit all pixels that don't match our criteria, in this case we are  
#            #looking for red but if you want you can adjust the first value in  
#            #both red which is the hue range(140,180).  OpenCV uses 0-180 as  
#            #a hue range for the HSV color model - multiply MS Paint value by 180/240
#            thresholded_img =  cv.CreateImage(cv.GetSize(hsv_img), 8, 1) 
#            cv.InRangeS(hsv_img, (self.hueMin, 130, 130), (self.hueMax, 255, 255), thresholded_img) 
#            
#            #determine the objects moments and check that the area is large  
#            #enough to be our object 
#            moments = cv.Moments(cv.GetMat(thresholded_img,1), 0)
#            area = cv.GetCentralMoment(moments, 0, 0)
#            newObj.objArea = area
#            
#            #there can be noise in the video so ignore objects with small areas 
#            if(area > 100000): 
#                #determine the x and y coordinates of the center of the object 
#                #we are tracking by dividing the 1, 0 and 0, 1 moments by the area 
#                x = cv.GetSpatialMoment(moments, 1, 0)/area 
#                newObj.objX = x
#                y = cv.GetSpatialMoment(moments, 0, 1)/area 
#                newObj.objY = y
#            
##                print 'x: ' + str(self.obj.objX) + ' y: ' + str(self.obj.objY) + ' area: ' + str(self.obj.objArea) 
#                
#                #create an overlay to mark the center of the tracked object 
#                overlay = cv.CreateImage(cv.GetSize(img), 8, 3) 
#                
#                cv.Circle(overlay, (int(x), int(y)), 2, (255, 255, 255), 20) 
#                cv.Add(img, overlay, img) 
#                #add the thresholded image back to the img so we can see what was  
#                #left after it was applied 
#                cv.Merge(thresholded_img, None, None, None, img) 
#             
#            #display the image  
#            cv.ShowImage(color_tracker_window, img) 
#            
#            if cv.WaitKey(10) == 27: 
#                break 
#            self.obj = newObj