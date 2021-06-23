#!/bin/bash

grep_result=`rosservice list |grep /sca_version`
echo $grep_result
if [ -z "$grep_result" ]; then
 echo "irisnode  connect failed!"
else
 rosservice call  /sca_version >>../version/temp_sca_version.txt
fi
