#!/usr/bin/expect -f

#NOTE:
#this script need installing expect on local machine first
#sudo apt-get install expect

set timeout 30
spawn scp -r ginger@192.168.1.200:/home/ginger/camera_param.json ./head_camera.txt
expect "*password:"
send "ginger\r"
expect eof
