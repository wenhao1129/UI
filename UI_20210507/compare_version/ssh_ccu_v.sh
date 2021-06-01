#!/bin/bash

cmd="cat /vendor/buildinfo.prop"

timeout 8 sshpass -p ginger ssh -t -o StrictHostKeyChecking=no ginger@192.168.1.200 $cmd >>../compare_version/temp_ccu_version.txt
