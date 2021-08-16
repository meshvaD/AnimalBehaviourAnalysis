import cv2 as cv
import numpy as np

#constants
RESIZE_FRAC = 0.5
BOX_WIDTH = 45
BOX_LENGTH = 45

vid = cv.VideoCapture('C:/Users/HS student/Desktop/20210730/MOVs/FILE210730-081413F_PD5-22.MOV')

ret, copy = vid.read()
first = copy.copy()
refCoords = []

global prevCoords

def centroid(contour):
    m = cv.moments(contour)
    #add 1e-5 to avoid division by 0
    cx = int(m['m10'] / (m['m00'] + 1e-5))
    cy = int(m['m01'] / (m['m00'] + 1e-5))
    
    return (cx, cy)

def find_distance(x1, y1, x2, y2, window):
    x = (abs(x1-x2) / window.shape[1]) * BOX_WIDTH
    y = (abs(y1-y2) / window.shape[0]) * BOX_LENGTH
    
    return ((x)**2 + (y)**2)**0.5

def click_crop(event, x, y, flags, param):
    global refCoords
    if event == cv.EVENT_LBUTTONDOWN:
        refCoords = [(x,y)]
    elif event == cv.EVENT_LBUTTONUP:
        refCoords.append((x,y))
        
        #draw bounding rec
        cv.rectangle(first, refCoords[0], refCoords[1], (0,255,0), 3)
        
def resize(frame, fraction):
    return cv.resize(frame, ((int)(frame.shape[1] * fraction), (int)(frame.shape[0] * fraction)), 
                     interpolation = cv.INTER_AREA)

first = resize(first, RESIZE_FRAC)

while True:
    cv.setMouseCallback('first', click_crop)
    cv.imshow('first', first)
    
    key = cv.waitKey(10) & 0xFF
    
    if key == ord('r'):
        first = resize(copy, RESIZE_FRAC) #reset 
    elif key == ord('c'):
        break
    
map_path = np.zeros(first[refCoords[0][1] : refCoords[1][1], refCoords[0][0] : refCoords[1][0]].shape)

distance = 0

while True:
    ret, frame = vid.read()
    if not ret:
        break
    elif ret:
        frame = resize(frame, RESIZE_FRAC)
        frame = frame[refCoords[0][1] : refCoords[1][1], refCoords[0][0] : refCoords[1][0]]
    
        #thresh and find contours
        frame_copy = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(frame_copy, 190, 255, cv.THRESH_BINARY)
        #cv.imshow('thresh', thresh)
        
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        #contour w largest area
        max_cont = contours[0]
        for cont in contours:
            if cv.contourArea(cont) > cv.contourArea(max_cont):
                max_cont = cont     
                
        currCoords = centroid(max_cont)
        try:
            #print(prevCoords)
            #find distance between two + connect to form line
            cv.line(map_path, prevCoords, currCoords, (255,0,0), 1)
            
            #scale coords to real dist
            distance += find_distance(prevCoords[0], prevCoords[1], currCoords[0], currCoords[1], map_path)
        
        except:
            print('start')
            
        prevCoords = currCoords
        cv.imshow('center', map_path)
        
        cv.waitKey(1)

vid.release()
cv.destroyAllWindows()

print(distance)
cv.imshow('path', map_path)
cv.waitKey(0)
