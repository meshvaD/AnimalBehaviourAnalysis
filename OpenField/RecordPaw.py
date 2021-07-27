import cv2 as cv
from pynput import keyboard
import pandas as pd

#create empty df with headers: name, count + frame for each direction
df = pd.DataFrame(columns = ['name',  'frame', 'left_count', 'right_count'])

fpath = 'C:/Users/HS student/Desktop/20210616/FILE210616-133650F_PD5-04.MOV'
vid = cv.VideoCapture(fpath)
name = (fpath.split('_')[1]).split('.')[0]

RESIZE_FRAC = 0.5

#wait time between frames
fps = int(input('fps to play: '))
wait = int(1000/fps)

pause = left = right = cropped = forward = backward = False

def resize(frame, frac):
    return cv.resize(frame, (int(frame.shape[1] * frac), int(frame.shape[0] * frac)))

def on_press(key):
    global pause, left, right, frame_count, cropped, forward, backward

    try:
        k = key.char #char keys a: left, s: right

        if (k == 'a'):
            left = True
        elif (k == 's'):
            right = True
        elif (k == 'c' and not cropped):
            print('cropped at: ' + str(frame_count))
            frame_count = 0
            cropped = True

    except:
        k = key.name #space: pause/play, left,right: frame navigation --> for later

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



key_List = keyboard.Listener(on_press = on_press)
key_List.start()

frame_count = 0

while vid.isOpened():
    #play/ pause vid: only show next frame if not paused
    if (not pause or forward or backward):

        if backward:
            backward = False
            frame_count -= 1
            vid.set(cv.CAP_PROP_POS_FRAMES, frame_count)
            ret, frame = vid.read()
        else:
            frame_count += 1
            ret, frame = vid.read()

        if ret:
            frame = resize(frame, RESIZE_FRAC)
            frame = cv.putText(frame, str(frame_count), (50,50), 
                               cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0))

            #time stamp
            min = int(frame_count / 3600)
            sec = int((frame_count / 60) - (60 * min))

            frame = cv.putText(frame, str(min) + " : " + str(sec), (50,100), cv.FONT_HERSHEY_PLAIN, 1, (255,0,0))

            cv.imshow('vid', frame)

            #if forward pressed wait until pressed again/ unpaused to resume
            if (forward):
                forward = False
                key = cv.waitKey(0)
                if (key == 2555904):
                    break

            if backward:
                key = cv.waitKey(0)
                if (key == 2424832):
                    break

            if (frame_count == 36000): #36000
                break
            elif (cv.waitKey(wait) & 0xFF == ord('q')):
                break
        else:
            cv.waitKey(0)
            break
    else:
        cv.waitKey(0)
    
    #new data row if left or right clicked
    if(cropped):
        if (left or right):
            l_count, r_count = 0., 0.

            if (left):
                l_count = 1.
                print('left, ' + str(frame_count))
                left = False
            if (right):
                r_count = 1.
                print('right, ' + str(frame_count))
                right = False

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
               
key = cv.waitKey(0)
if (key == ord('q')):
    cv.destroyAllWindows()


print(df)
df.to_csv(name + '.csv')




