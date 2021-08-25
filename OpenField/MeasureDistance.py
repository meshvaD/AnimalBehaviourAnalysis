import cv2 as cv
import numpy as np

#constants
RESIZE_FRAC = 0.5
BOX_WIDTH = 45
BOX_LENGTH = 45

vid = cv.VideoCapture('C:/Users/HS student/Desktop/Behavioural Analysis/Raw Data/20210803/MOVs/FILE210803-084612F_PD5-22.MOV')

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

def shoelace(p):
    s = 0
    for i in range(0, len(p)-1):
        s += (p[i][0]*p[i+1][1])
        s -= (p[i+1][0]*p[i][1])
    s += (p[-1][0]*p[0][1] - p[0][0]*p[-1][1])
    s = abs(s)/2

    return s

def centroid_points(points):
    #convex hull
    hull = cv.convexHull(points)
    area = shoelace(points)

    if len (points) > 0:
        x = 0
        y = 0
        for p in points:
            x += p[0]
            y += p[1]
        return (int(x/len(points)), int(y/len(points)))
    else:
        return -1

def corner(c, frame, center):
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])

    extremes = [extLeft, extRight, extTop, extBot]

    max_dst = extremes[0]

    for point in extremes:
        #frame = cv.circle(frame, point, 3, (255,0,255), 2)

        if relative_distance(point, center) > relative_distance(max_dst, center):
            max_dst = point

    cv.circle(frame, max_dst, 3, (255,255,0), 2)

    cv.imshow('extreme points', frame)

    return max_dst

def relative_distance(a, b):
    x = abs(a[0]-b[0])
    y = abs(a[1]-b[1])
    
    return ((x)**2 + (y)**2)**0.5

def scaled_distance(x1, y1, x2, y2, window):
    x = (abs(x1-x2) / window.shape[1]) * BOX_WIDTH
    y = (abs(y1-y2) / window.shape[0]) * BOX_LENGTH
    
    return ((x)**2 + (y)**2)**0.5

def click_crop(event, x, y, flags, param):
    global refCoords
    if event == cv.EVENT_LBUTTONUP:
        refCoords.append((x,y))
        
        #draw bounding rec
        rec = cv.rectangle(first, refCoords[0], refCoords[1], (0,255,0), 1)
        
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
trim = False
frame_count = 0
points = []

while True:
    ret, frame = vid.read()
    if not ret:
        break
    elif ret:
        frame = resize(frame, RESIZE_FRAC)
        frame = frame[refCoords[0][1] : refCoords[1][1], refCoords[0][0] : refCoords[1][0]]
    
        cv.imshow('cropped', frame)

        frame_count +=1 

        #thresh and find contours
        frame_copy = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(frame_copy, 50, 150, cv.THRESH_BINARY_INV)

        #dilate and erode removes tail
        thresh = cv.dilate(thresh, cv.getStructuringElement(cv.MORPH_RECT, (3,3)), iterations=4)
        #thresh = cv.erode(thresh, cv.getStructuringElement(cv.MORPH_RECT, (3,3)), iterations=2)
        
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        #contour w largest area
        if len(contours) > 1:
            max_cont = contours[0]
            for cont in contours:
                if cv.contourArea(cont) > cv.contourArea(max_cont):
                    max_cont = cont 
     
            currCoords = centroid(max_cont)
            currCoords = corner(max_cont, frame, currCoords)

            draw = cv.drawContours(frame, max_cont, -1, (0,0,255), cv.FILLED)
            cv.circle(draw, currCoords, 2, (0,255,0), 2)

            if trim:
                #check if currCoords part of circle, then append to all points
                print('curr coords: ', currCoords)
                points.append(currCoords)

                circ_center = centroid_points(points)
                print('center of circle: ', circ_center, '\n')

                cv.circle(map_path, currCoords, 1, (255,255,255))

                radial = cv.circle(map_path.copy(), circ_center, 1, (255,255,0))

                #try:
                #    #find distance between two + connect to form line
                #    cv.line(map_path, prevCoords, currCoords, (255,255,255), 1)
            
                #except:
                #    print('start')
            
                prevCoords = currCoords
                cv.imshow('center', radial)
        
        key = cv.waitKey(1) & 0xFF
        if key == ord('t'):
            print('trim')
            trim = True

            frame_count = 0

        if frame_count % 60 == 0:
            print(frame_count)

        if frame_count == 7200: #TEST
            break


vid.release()
cv.destroyAllWindows()

cv.imshow('path', map_path)
cv.waitKey(0)
