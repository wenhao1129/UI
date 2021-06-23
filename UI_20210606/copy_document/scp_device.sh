#!/usr/bin/expect -f

#NOTE:
#this script need installing expect on local machine first
#sudo apt-get install expect

set timeout 30
spawn scp -r ../setup_param/device.cfg ginger@192.168.1.200:/ftm
expect "*password:"
send "ginger\r"
expect eof
