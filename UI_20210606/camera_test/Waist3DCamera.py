#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append("../camera_test/")
import Camera_Test

'''
This file will control chest 2D camera result
NOTE: 
Before testing, config result environments as XR-1 2D camera result solution doc.
'''

class Object:
    def __init__(self):
       self.result = 0
       
    def DoTest(self,log_path,name,root,i):
        self.result = 0
        print "Chest 2D Camera Test: DoTest"
        return Camera_Test.camera_running_test(Camera_Test.CAMERA_WAIST_3D)
        
    def DoStop(self):
        self.result = 0
        print "Chest 2D Camera Test: DoStop"
