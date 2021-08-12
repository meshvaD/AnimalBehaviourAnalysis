import cv2 as cv
import tifffile as tiff
import os

basepath = 'C:/Users/HS student/Desktop/20210730/'

#for file in os.listdir(basepath):
filename = 'FILE210730-143018F_PD06-08'
#filename = file.split('.')[0]

#if file.split('.')[-1] == 'MOV':
#print(filename)

vid = cv.VideoCapture(basepath + 'MOVs/' + filename + '.MOV')
stack = tiff.TiffWriter(basepath + filename + '.tiff')

count = 0

while vid.isOpened():
    ret, frame = vid.read()
    count += 1

    if ret:
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        if count % 12 == 0:
            stack.write(frame)
    else:
        vid.release()
        break

print('done:  ' + filename)

