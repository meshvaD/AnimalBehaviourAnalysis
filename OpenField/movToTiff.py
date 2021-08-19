import cv2 as cv
import tifffile as tiff
import os

import tkinter as tk
from tkinter import filedialog

#basepath = 'C:/Users/HS student/Desktop/20210621/'

root = tk.Tk()
root.withdraw()

print('Select directory where the .mov files are located')
mov_dir = filedialog.askdirectory()

target_fps = int(input('Targeted tiff fps: '))

print('Select the full path of the directory where the tiff stacks should be saved')
tiff_dir = filedialog.askdirectory()


#go through each .MOV file in the directory
for i in range (0, len(os.listdir(mov_dir))):
    file = os.listdir(mov_dir)[i]
    print(file)
    filename = file.split('.')[0]

    if file.split('.')[-1] == 'MOV':

        vid = cv.VideoCapture(mov_dir + '/' + filename + '.MOV')
        stack = tiff.TiffWriter(tiff_dir + '/'+ filename + '.tiff')

        orig_fps = vid.get(cv.CAP_PROP_FPS)

        count = 0

        #every 12 frames (60/5fps) write frame to tiff stack
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
