#!/bin/bash

cmd="adb shell getprop ro.build.display.id"
timeout 6 sshpass -p ginger ssh -t -o StrictHostKeyChecking=no ginger@192.168.1.200 $cmd
