#!/usr/bin/expect -f

#NOTE:
#this script need installing expect on local machine first
#sudo apt-get install expect

set timeout 30
spawn scp ./camera_param_back.json ginger@192.168.0.200:/ftm/camera
expect "*password:"
send "ginger\r"
expect eof
