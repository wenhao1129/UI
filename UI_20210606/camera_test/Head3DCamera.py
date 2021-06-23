
'''
This file will control head front 3d Camera test
'''

import sys
import Camera_Test

class Object:
    def __init__(self, skip):
       self.test = 0
       self.skip = skip
       print "Hello head front 3d Camera test"

    def DoTest(self,log_path,name,root,id):
	ret = Camera_Test.camera_running_test(Camera_Test.CAMERA_HEAD_3D)
        if (ret==1):
            ret = Camera_Test.camera_running_test(Camera_Test.CAMERA_HEAD_3D_B)
        
        print "Head 3D Camera DoTest"
        return ret

    def DoStop(self):
        self.test = 0
        print "Head 3D Camera DoStop"



