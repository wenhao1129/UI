#!/bin/bash

grep_result=`rosservice list |grep /ecu_version`
echo $grep_result
if [ -z "$grep_result" ]; then
 echo "irisnode  connect failed!"
else
 rosservice call  /ecu_version >>../compare_version/temp_ecu_version.txt
fi
