'''Demonstrate Python wrapper of C apriltag2 library by running on camera frames.'''
from __future__ import division
from __future__ import print_function

import collections

from argparse import ArgumentParser
import cv2

import apriltag2


# Definitions
TAG_NUM_REQUIRED = 1
FLIP_OPT_HORIZONTAL = 1
VERIFY_WINDOW_NAME = "Camera Verify Window"


def check_image(cvImage):
    print('Camera_Verify: check_image: E...')
    
    if cvImage is None:
        print("ERROR: Image None")
        return -1
    
    print("Camera_Verify: cvImage.shape = " + str(cvImage.shape))

    # since our camera module gives out mirrored image, we need flip images back
    flipImage = cv2.flip(cvImage, FLIP_OPT_HORIZONTAL, dst=None)
    grayImage = cv2.cvtColor(flipImage, cv2.COLOR_RGB2GRAY)
    
    # set up a reasonable search path for the apriltag2 DLL inside the
    # github repo this file lives in;
    #
    # for "real" deployments, either install the DLL in the appropriate
    # system-wide library directory, or specify your own search paths
    # as needed.
    detector = apriltag2.Detector()

    detections, detectImage = detector.detect(grayImage, return_image=True)

    # check tags detected on the image
    num_detections = len(detections)
    if (num_detections < TAG_NUM_REQUIRED):
        print('ERROR: Invalid number of tags ' + num_detections + ", min required " + TAG_NUM_REQUIRED)
        return -2

    '''
    for i, detection in enumerate(detections):
        print('Detection {} of {}:'.format(i+1, num_detections))
        print()
        print(detection.tostring(indent=2))
        print()
    '''
    # we only need one tag for this test
    detection = detections[0]
    
    print()
    print('Camera_Verify: Tag Info')
    print('---------------------------------------------------')
    print(detection.tostring(indent=2))
    print('---------------------------------------------------')
    print()

    overlay = flipImage // 2 + detectImage[:, :, None] // 2
    
    ###@: todo: modify these by real values for testing
    tag_size = 0.08  #unit by meter
    #camera_params = apriltag2._camera_params('(1693.53, 1688.11, 542, 432.14)')
    camera_params = apriltag2._camera_params('(1487, 1473, 656, 374)')

    pose, e0, e1 = detector.detection_pose(
        detection, camera_params, tag_size
        )
    apriltag2._draw_pose(
        overlay, camera_params, tag_size, pose
        )
    print(detection.tostring(
        collections.OrderedDict([('Pose', pose),
                                 ('InitError', e0),
                                 ('FinalError', e1)]),
        indent=2))
    print()

    cv2.imshow(VERIFY_WINDOW_NAME, overlay)
    show_time = 5000  # unit by ms
    print("Camera_Verify: show detect image " + str(show_time) + "ms...")
    cv2.waitKey(show_time)
    cv2.destroyWindow(VERIFY_WINDOW_NAME)

    print('Camera_Verify: check_image: X.')
    return 0
# def check_image


# for some reason pylint complains about members being undefined :(
# pylint: disable=E1101
def cam_video_test():
    print('***cam_video_test: E...')
    parser = ArgumentParser(
        description='test apriltag2 Python bindings')
    parser.add_argument('device_or_movie', metavar='INPUT', nargs='?', default=0,
                        help='Movie to load or integer ID of camera device')
    apriltag2.add_arguments(parser)
    options = parser.parse_args()
    print('***cam_video_test: options.device_or_movie = ' + options.device_or_movie)

    try:
        cap = cv2.VideoCapture(int(options.device_or_movie))
    except ValueError:
        cap = cv2.VideoCapture(options.device_or_movie)

    window_name = 'Camera Image Window'
    cv2.namedWindow(window_name)

    # set up a reasonable search path for the apriltag2 DLL inside the
    # github repo this file lives in;
    #
    # for "real" deployments, either install the DLL in the appropriate
    # system-wide library directory, or specify your own search paths
    # as needed.
    detector = apriltag2.Detector(options,
                                 searchpath=apriltag2._get_demo_searchpath())

    while True:
        success, cap_frame = cap.read()
        if not success:
            print('ERROR: cap.read for image flipImage failed')
            break

        # since our camera module gives out mirrored image, we need flip images back
        flipImage = cv2.flip(cap_frame, FLIP_OPT_HORIZONTAL, dst=None)
        
        grayImage = cv2.cvtColor(flipImage, cv2.COLOR_RGB2GRAY)
        detections, detectImage = detector.detect(grayImage, return_image=True)

        num_detections = len(detections)
        print('Detected {} tags.\n'.format(num_detections))

        # for this camera test, we only have one tag
        if (num_detections != TAG_NUM_REQUIRED):
            print('ERROR: invalid number of tags ' + num_detections + ", required " + TAG_NUM_REQUIRED)
            print('Please check the test environment, ensure test tag num is ' + TAG_NUM_REQUIRED)
            break

        '''
        for i, detection in enumerate(detections):
            print('Detection {} of {}:'.format(i+1, num_detections))
            print()
            print(detection.tostring(indent=2))
            print()
        '''
        detection = detections[0]
        
        print()
        print('***Detection Test Tag')
        print('---------------------------------------------------')
        print(detection.tostring(indent=2))
        print('---------------------------------------------------')
        print()
        
        overlay = flipImage // 2 + detectImage[:, :, None] // 2
        cv2.imshow(window_name, overlay)
        key = cv2.waitKey(1)

        if key == 27:  # Esc
            break
    # while True
# def cam_video_test


if __name__ == '__main__':
    cam_video_test()
