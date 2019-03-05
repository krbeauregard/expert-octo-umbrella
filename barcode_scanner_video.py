##################################################################
##  Simple test of ability to decode a QR barcode using pyzbar  ##
##  This is designed to take something in the form              ##
##  [1-8], [text] encoded into a QR code and display the        ##
##  text in a color defined in the dictionary below             ##
##################################################################

import imutils, time
import cv2 as cv
from imutils.video import VideoStream
from pyzbar import pyzbar

#initialize video stream && allow camera to warm up
print('[INFO] starting video stream...')
##  using custom videostream.py for raspi, the following should normally read:
##  vs = VideoStream(src=0, usePiCamera=True).start()
vs = VideoStream().start()
time.sleep(2)

font = cv.FONT_HERSHEY_SIMPLEX

code = ['0',' ']
color = (255,255,255)
colors = {'1':(255,255,255),    #white
          '2':(0, 0, 0),        #black
          '3':(255, 0, 0),      #blue
          '4':(0, 255, 0),      #green
          '5':(0, 0, 255),      #red
          '6':(0, 255, 255),    #yellow
          '7':(255, 0, 255),    #purple
          '8':(255, 255, 0)}    #cyan

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    frame = imutils.rotate(frame, 180)      #comment if video is upside-down
##  For Pi Camera, this results in 300x400
##  Dimensions for other platforms would need to be verified

    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        (x,y,w,h) = barcode.rect
        cv.rectangle(frame, (x,y),(x+w, y+h), (0,0,255),2)

        barcodeData = barcode.data.decode('utf-8')
        barcodeType = barcode.type

        text = '{}({})'.format(barcodeData, barcodeType)
        cv.putText(frame, text, (x,y-10), font, 0.5, (0,0,255),2)

        code = barcodeData.split(',')
    if code[0] in colors:
        color = colors[code[0]]
    txt = code[1]
        
    cv.putText(frame,txt,(40,40), font, 1,color,2,cv.LINE_AA)

    cv.imshow('Barcode Scanner', frame)
    key = cv.waitKey(1) & 0xFF

    if key == ord('q'):
        break

print("[INFO] cleaning up...")

cv.destroyAllWindows()
vs.stop()
