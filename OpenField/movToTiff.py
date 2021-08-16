import cv2 as cv
import tifffile as tiff
import os

basepath = 'C:/Users/HS student/Desktop/20210803/'

for i in range (11, len(os.listdir(basepath + 'MOVs'))):
    file = os.listdir(basepath + 'MOVs')[i]
    print(file)
    filename = file.split('.')[0]

    if file.split('.')[-1] == 'MOV':

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
