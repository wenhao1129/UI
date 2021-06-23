#coding=UTF-8
'''
Ginger 2D Camera Test Utilities
NOTE: 
Before testing, config test environments as XR-1 2D camera test solution doc.
'''

import os
import sys

CAMERA_HEAD_FRONT = 0
CAMERA_HEAD_BACK = 1
CAMERA_CHEST_FRONT = 2
CAMERA_WAIST_3D = 3
CAMERA_HEAD_3D = 4
CAMERA_HEAD_3D_B =5
TEST_PASS = 1
TEST_FAILED = 0


def camera_running_test(camera_id):
    print("***camera_running_test: " + str(camera_id))
    # As setup.bash already called, here rosrun directly
    if (camera_id == CAMERA_HEAD_FRONT):
        cmd = "rosrun camera_test camera_subscriber /camera0/usb_cam/image_raw bgr8"
    elif (camera_id == CAMERA_HEAD_BACK):
        cmd = "rosrun camera_test camera_subscriber /camera2/usb_cam/image_raw bgr8"
    elif (camera_id == CAMERA_CHEST_FRONT):
        cmd = "rosrun camera_test camera_subscriber /camera1/usb_cam/image_raw bgr8"
    elif (camera_id == CAMERA_WAIST_3D):
        cmd = "rosrun camera_test camera_subscriber /camera/depth/image"
    elif (camera_id == CAMERA_HEAD_3D):
        cmd = "rosrun camera_test camera_subscriber /cam2/image_depth"
    elif (camera_id == CAMERA_HEAD_3D_B):
        cmd = "rosrun camera_test camera_subscriber /cam3/trichromatic"
    else:
        print("ERROR: unsupport camera id: " + str(camera_id))
        return TEST_FAILED
    print("Test Command: " + cmd)
    
    retObj = os.popen(cmd)
    retStr = str(retObj.readlines())
    retObj.close()
    ret = TEST_FAILED
    if (retStr.find("Success") != -1):
        ret = TEST_PASS
    
    print("Test Result: " + str(ret))
    return ret
# def camera_running_test


def get_cmd_line():
    ret = "***"
    arg_num = len(sys.argv)
    for i in range(0, arg_num):
        ret += sys.argv[i]
        if (i != arg_num - 1):
            ret += " "
    return ret
#def get_cmd_line


'''
----------MAIN FUNC----------
'''
if __name__ == '__main__':
    print(get_cmd_line() + ", enter...\n")
    
    camera_running_test(CAMERA_HEAD_BACK)
        
    print(get_cmd_line() + ", exit.\n")
