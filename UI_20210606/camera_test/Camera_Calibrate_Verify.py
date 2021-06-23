#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Ginger 2D Camera Test Utilities
NOTE: 
Before testing, config test environments as XR-1 2D camera test solution doc.
'''


import os
import sys
import time

# Using this CvBridge Tutorial for converting
# ROS images to OpenCV2 images
# http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython

# Using this OpenCV2 tutorial for saving Images:
# http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html

# rospy for the subscriber
import rospy
# ROS Image message
from sensor_msgs.msg import Image
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for showing image
import cv2

import Camera_Verify


# Definitions
ROS_NODE_NAME = "HeadBackCameraCalibrateVerifySubscriber"
IMAGE_TOPIC_NAME = "/usb_cam/image_raw"
CALIBRATE_VERIFY_WINDOW = "Calibrate Verify Window"
SUCCESS = 0
FAILED = -1
WAIT_IMAGE_MAX_TIMES = 10
WAIT_IMAGE_INTERVAL = 0.5  # unit by second


# Global Variables
g_CvBridge = CvBridge()  # Instantiate CvBridge
g_FrameCount = 0
g_CallTimes = 0
g_CvImage = None
g_CaptureImage = False


def camera_image_callback(msg):
    global g_FrameCount
    global g_CvBridge
    global g_CvImage
    global g_CaptureImage
    
    g_FrameCount += 1
    #print("camera_image_callback: g_FrameCount = " + str(g_FrameCount) + ", g_CaptureImage = " + str(g_CaptureImage))
    
    if g_CaptureImage:
        g_CvImage = g_CvBridge.imgmsg_to_cv2(msg, "bgr8")
        '''
        # check image
        if g_CvImage is None:
            print "ERROR: None image from CvBridge"
        else:
            print "Get image from CvBridge, shape = " + str(g_CvImage.shape)
        #'''

    #can't start again once shut down?
    #rospy.signal_shutdown('Quit') 
# def camera_image_callback


def do_verify():
    global g_CallTimes
    global g_CaptureImage
    global g_CvImage
    
    g_CallTimes += 1
    print ("Camera_Calibrate_Verify: do_verify: E, g_CallTimes = " + str(g_CallTimes) + "...")
    

    #
    # grab camera images by ros
    #
    # In ROS, nodes are uniquely named. If two nodes with the same node are launched, 
    # the previous one is kicked off. 
    # The anonymous=True flag means that rospy will choose a unique name for our 'listener' 
    # node so that multiple listeners can run simultaneously.
    # rospy.init_node('listener', anonymous=True)
    # rospy.Subscriber("chatter", String, callback)
    # rospy.spin()
    # rospy.spin() simply keeps your node from exiting until the node has been shutdown. 
    # Unlike roscpp, rospy.spin() does not affect the subscriber callback functions, as those have their own threads.
    #
    #if (g_CallTimes == 1 or rospy.is_shutdown()):
    if g_CallTimes == 1:
        rospy.init_node(ROS_NODE_NAME)
        rospy.Subscriber(IMAGE_TOPIC_NAME, Image, camera_image_callback)
        #rospy.spin()

    # open flag to capture image from callback
    g_CvImage = None
    g_CaptureImage = True
    wait_times = 0
    while g_CvImage is None and wait_times < WAIT_IMAGE_MAX_TIMES:
        wait_times += 1
        print "Image not available, wait " + str(wait_times) + "/" + str(WAIT_IMAGE_MAX_TIMES) + "..."
        time.sleep(WAIT_IMAGE_INTERVAL)
    if g_CvImage is None:
        print "ERROR: Can't capture image"
        return FAILED
    else:
        print "Get image, shape = " + str(g_CvImage.shape)
        g_CaptureImage = False

    # check result base on captured image
    ret = Camera_Verify.check_image(g_CvImage)
    if ret == 0:
        check_result = SUCCESS
    else:
        print "ERROR: Camera verify check failed, error = " + str(ret)
        check_result = FAILED

    # show image and result
    try:
        if (check_result == SUCCESS):
            text = 'SUCCESS'
            fontcolor = (0, 255, 0)  # BGR
        else:
            text = 'FAILED'
            fontcolor = (0, 0, 255)  # BGR

        org = (550, 60)
        fontFace = cv2.FONT_HERSHEY_COMPLEX
        fontScale = 1
        thickness = 1
        lineType = 4
        cv2.putText(g_CvImage, text, org, fontFace, fontScale,
                    fontcolor, thickness, lineType)
        cv2.imshow(CALIBRATE_VERIFY_WINDOW, g_CvImage)
        cv2.waitKey(5000)
        cv2.destroyWindow(CALIBRATE_VERIFY_WINDOW)
    except Exception as e:
        print("ERROR: camera_image_callback: show result error = " + str(e))

    print ("Camera_Calibrate_Verify: do_verify: X, ret = " + str(check_result))
    return check_result
# def do_verify


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
    print (get_cmd_line() + ", enter...\n")
    
    do_verify()
        
    print (get_cmd_line() + ", exit.\n")
    #os.system('pause')
