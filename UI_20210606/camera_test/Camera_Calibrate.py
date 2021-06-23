#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Ginger 2D Camera Test Utilities
NOTE: 
Before testing, config test environments as XR-1 2D camera test solution doc.
'''


import os
import sys


# Definitions
CAMERA_MATRIX_KEY = 'K = '


def back_camera_calibration():
    print ("***back_camera_calibration: E...")

    #'''
    #calib_cmd = 'ls -l'
    #calib_res = os.system(calib_cmd)
    #print calib_res
    calib_cmd = 'rosrun camera_calibration cameracalibrator.py --size 11x8 --square 0.025 --no-service-check image:=/usb_cam/image_raw camera:=/usb_cam'
    retObj = os.popen(calib_cmd)
    print "-------------------------------------------------------------------------"
    camera_matrix_line_str = ""
    for line in retObj.readlines():
        print "%s" % (line),
        if (line.find(CAMERA_MATRIX_KEY) > 0):
            camera_matrix_line_str = line
    print "-------------------------------------------------------------------------"
    retObj.close()
    #'''
    
    #parse matrix line to get parameters
    #camera_matrix_line_str="('K = ', [1524.301650079095, 0.0, 612.012824159285, 0.0, 1555.256448867172, 378.78505867338373, 0.0, 0.0, 1.0])"
    print "camera_matrix_line_str=%s"%camera_matrix_line_str
    fx = ""
    fy = ""
    cx = ""
    cy = ""
    
    if camera_matrix_line_str.strip() == '':
        print 'ERROR: invalid camera matrix string'
        return -1
    else:
        try:
            fx = camera_matrix_line_str.split(',')[1].split('[')[1][:10]
            fy = camera_matrix_line_str.split(',')[5].strip()[:10]
            cx = camera_matrix_line_str.split(',')[3].strip()[:9]
            cy = camera_matrix_line_str.split(',')[6].strip()[:9]
        except:
            print 'ERROR: parse camera matrix string failed'
            return -2
    
    print "fx = %s"%fx
    print "fy = %s"%fy
    print "cx = %s"%cx
    print "cy = %s"%cy
    
    #camera_param.json
    #{"ppx": 627.957092, "ppy": 350.391327, "fx": 941.246643, "fy": 941.246826}
    param_file = open("camera_param_back.json","w")
    param_file.write("{\"ppx\": " + cx + ", \"ppy\": " + cy + ", \"fx\": " + fx + ", \"fy\": " + fy + "}")
    param_file.close()
    
    '''
    #unnecessary for parse from result
    print "Sync data to ginger TX2..."
    os.system("rm -rf tmp")
    os.system("mkdir tmp")
    os.system("tar zxvf /tmp/calibrationdata.tar.gz -C ./tmp")
    os.system("rm /tmp/calibrationdata.tar.gz")
    
    # todo: transfer data format to json
    os.system("mv ./tmp/ost.txt ./tmp/camera_param_back.json")
    '''
    
    # upload camera param file to ginger
    ret = os.system("./scp.sh")

    print ("***back_camera_calibration: X, ret = " + str(ret))
    return ret
# def back_camera_calibration


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
    
    back_camera_calibrations()
        
    print (get_cmd_line() + ", exit.\n")
    #os.system('pause')
