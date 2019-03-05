######################################################################
##  This is a basic attempt at a 'green screen'                     ##
##                                                                  ##
##  The panel allows the user to adjust HSV parameters for          ##
##  the desired color (H) and other values to compensate for        ##
##  other conditions.                                               ##
##  Good results for green are around 30-70 for LH and UH           ##
##                                                                  ##
##                                                                  ##
##  Be sure to set bg_img to something suitable                     ##
##                                                                  ##
##  This uses a default webcam. On my Raspberry Pi, I use a         ##  
##  modified videostream.py that has usePiCamera=True as default    ##
##  because it makes life easier.                                   ##
######################################################################


import imutils, time
import cv2 as cv
import numpy as np
from imutils.video import VideoStream

#initialize video stream && allow camera to warm up
print('[INFO] starting video stream...')
##  using custom videostream.py for raspi, the following should normally read:
##  vs = VideoStream(src=0, usePiCamera=True).start()
vs = VideoStream().start()
time.sleep(2)   #give camera time to warm up

panel = np.zeros([50,700], np.uint8)
cv.namedWindow('panel')

##test background image
bg_img = cv.imread('/home/pi/Pictures/grad.jpg')

##remove hardcoding!!!
rows, cols = 400, 300

def nothing(x):
    pass


cv.createTrackbar('Lh', 'panel', 0, 179, nothing)
cv.createTrackbar('Uh', 'panel', 179, 179, nothing)

cv.createTrackbar('Ls', 'panel', 0, 255, nothing)
cv.createTrackbar('Us', 'panel', 255, 255, nothing)

cv.createTrackbar('Lv', 'panel', 0, 255, nothing)
cv.createTrackbar('Uv', 'panel', 255, 255, nothing)

cv.createTrackbar('y1', 'panel', 0, 300, nothing)
cv.createTrackbar('y2', 'panel', 300, 300, nothing)
cv.createTrackbar('x1', 'panel', 0, 400, nothing)
cv.createTrackbar('x2', 'panel', 400, 400, nothing)


while True:
    frame = imutils.rotate(vs.read(), 180)
    frame = imutils.resize(frame, width=400)
    ## For Pi Camera, this results in 300x400
    ## Dimensions for other platforms would need to be verified   


    lh = cv.getTrackbarPos('Lh', 'panel')
    uh = cv.getTrackbarPos('Uh', 'panel')
    ls = cv.getTrackbarPos('Ls', 'panel')
    us = cv.getTrackbarPos('Us', 'panel')
    lv = cv.getTrackbarPos('Lv', 'panel')
    uv = cv.getTrackbarPos('Uv', 'panel')

    y1 = cv.getTrackbarPos('y1', 'panel')
    y2 = cv.getTrackbarPos('y2', 'panel')
    x1 = cv.getTrackbarPos('x1', 'panel')
    x2 = cv.getTrackbarPos('x2', 'panel')
    
    roi = frame[x1:x2, y1:y2]
    hsv = cv.cvtColor(roi, cv.COLOR_RGB2HSV)

    lower_green = np.array([lh, ls, lv])
    upper_green = np.array([uh, us, uv])

    mask = cv.inRange(hsv, lower_green, upper_green)
    mask_inv = cv.bitwise_not(mask)
    
    bg = cv.bitwise_and(roi, roi, mask=mask)
    fg = cv.bitwise_and(roi, roi, mask=mask_inv)

    image = cv.bitwise_and(roi, roi, mask = mask_inv)
    gs = cv.bitwise_and(bg_img, bg_img, mask = mask)

    
    dst = cv.add(image, gs)

##    cv.imshow('frame', frame)
##    cv.imshow('mask', mask)
##    cv.imshow('bg', bg)
##    cv.imshow('fg', fg)
##    cv.imshow('im', image)
##    cv.imshow('gs', gs)
    cv.imshow('dst', dst)
    cv.imshow('panel', panel)

    k = cv.waitKey(1) & 0xFF
    if k == ord('q'):
        break

cv.destroyAllWindows()
vs.stop()
