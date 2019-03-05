# expert-octo-umbrella
Raspberry Pi Photo Booth project

This project is meant to be an automated photo booth and an excuse to mess with Computer Vision.

Hardware so far:
  Raspberry Pi 3 B+
  Raspberry Pi Camera
  TV for display using HDMI out
  USB keyboard/trackpad for typing and clicking

Software used so far:
  2018-11-13-raspbian-stretch-full
  Python 3.5.3
  OpenCV 4.0.0
  numpy 1.16
  imutils 0.5.2 (from pyimagesearch.com)
  pyzbar 0.1.7
  
barcode_scanner_video.py
  Will be a cheap means of input through the camera
  
green_screen.py
  Is the beginning of a 'green screen' capability for the system.
  It is grainy and blotchy at the moment. Some erosion and dilation should help.
