#!/bin/bash

grep_result=`rosservice list |grep iris_camera/system_version `
echo $grep_result
if [ -z "$grep_result" ]; then
 echo "irisnode  connect failed!"
else
 rosservice call  iris_camera/system_version >>../version/temp_iris_camera.txt
fi
