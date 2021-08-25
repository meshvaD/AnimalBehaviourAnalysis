import cv2 as cv
from pynput import keyboard
import pandas as pd

#create empty df with headers: name, count + frame for each direction
df = pd.DataFrame(columns = ['name',  'frame', 'left_count', 'right_count'])

fpath = 'C:/Users/HS student/Desktop/20210803/FILE210803-084612F_PD5-22.MOV'
vid = cv.VideoCapture(fpath)
name = (fpath.split('_')[1]).split('.')[0]

#used to reshape frame to be smaller
RESIZE_FRAC = 0.5

#wait time between frames
fps = int(input('fps to play: '))
wait = int(1000/fps)

pause = left = right = cropped = forward = backward = False

cropped_frame = 0

def resize(frame, frac):
    return cv.resize(frame, (int(frame.shape[1] * frac), int(frame.shape[0] * frac)))

def on_press(key):
    #change var to true when pressed --> action carried out in next frame
    global pause, left, right, frame_count, cropped, forward, backward, cropped_frame

    try:
        k = key.char #char keys a: left, s: right, c: crop

        if (k == 'a'):
            left = True
        elif (k == 's'):
            right = True
        elif (k == 'c' and not cropped): #if already cropped, cannot crop again
            cropped_frame = frame_count
            print('cropped at: ' + str(frame_count))
            frame_count = 0
            cropped = True

    except:
        k = key.name #space: pause/play, left,right: frame navigation 

        #pause/ play with space key
        if (k == 'space'):
            if pause:
                pause = False
            else:
                pause = True
        elif (k == 'right'):
            forward = True
        elif (k == 'left'):
            backward = True


#key listener for key presses
key_List = keyboard.Listener(on_press = on_press)
key_List.start()

frame_count = 0

while vid.isOpened():
    #only play a new frame if the video is not paused and the user isn't navigating frames
    if (not pause or forward or backward):

        #takes more time, goes back one frame
        if backward:
            frame_count -= 1
            vid.set(cv.CAP_PROP_POS_FRAMES, frame_count + cropped_frame)
            ret, frame = vid.read()
        else: #if forward/ regular play, go forward one frame
            frame_count += 1
            ret, frame = vid.read()

        if ret:
            frame = resize(frame, RESIZE_FRAC)

            #display frame count and time stamp
            frame = cv.putText(frame, str(frame_count), (50,50), 
                               cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0))
            min = int(frame_count / 3600)
            sec = int((frame_count / 60) - (60 * min))
            frame = cv.putText(frame, str(min) + " : " + str(sec), (50,100), cv.FONT_HERSHEY_PLAIN, 1, (255,0,0))

            #skip over frames to speed up video even more
            if backward and frame_count % 2 == 0: #skips every otehr frame when rewinding
                cv.imshow(name, frame)
                backward = False
            elif frame_count % 4 == 0: #plays every 4th frame 
                cv.imshow(name, frame)

            #if navigation pressed, wait until pressed again/ unpaused to resume
            if (forward):
                forward = False
                key = cv.waitKey(0)
                if (key == 2555904):
                    break
            if backward:
                key = cv.waitKey(0)
                if (key == 2424832):
                    break

            #exit video stream after 10 min at 60fps or after q key pressed
            if (frame_count == 36000): #36000
                break
            elif (cv.waitKey(wait) & 0xFF == ord('q')):
                break
        else:
            cv.waitKey(0)
            break
    else:
        cv.waitKey(0)
    
    #new data row if left or right clicked, only documents clicks after video is cropped
    if(cropped):
        if (left or right):
            l_count, r_count = 0., 0.

            #insert value 1 if left/right key pressed
            if (left):
                l_count = 1.
                print('left, ' + str(frame_count))
                left = False
            if (right):
                r_count = 1.
                print('right, ' + str(frame_count))
                right = False

            #create new df row and insert left/right vals
            try:
                if (df.iloc[-1][1] == frame_count):
                    if (r_count > 0):
                        df._set_value(len(df.index)-1, 'right_count', 1)
                    else:
                        df._set_value(len(df.index)-1, 'left_count', 1)
                else:
                    df = df.append({'name' : name, 'frame' : frame_count, 'left_count' : l_count,
                            'right_count' : r_count}, ignore_index = True)

            except:
                df = df.append({'name' : name, 'frame' : frame_count, 'left_count' : l_count,
                                'right_count' : r_count}, ignore_index = True)
    
vid.release()
        
#show last frame and export data to csv
key = cv.waitKey(0)
if (key == ord('q')):
    cv.destroyAllWindows()

print(df)
df.to_csv('paw_20210803/' + name + '.csv')



