#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file will control head front 2d Camera test
NOTE: 
Before testing, config test environments as XR-1 2D camera test solution doc.
'''

import Camera_Test

class Object:
    def __init__(self):
       self.test = 0
       print "Hello head front 2d Camera test"

    def DoTest(self,log_path,name,root,i):
        self.test = 0
        print "Head Front 2D Camera DoTest"
        return Camera_Test.camera_running_test(Camera_Test.CAMERA_HEAD_FRONT)

    def DoStop(self):
        self.test = 0
        print "Head Front 2D Camera DoStop"
