import cv2 as cv

# A list of the paths of your videos
videos = ["C:/Users/HS student/Desktop/20210803/MOVs/FILE210803-134951F.MOV", 
          "C:/Users/HS student/Desktop/20210803/MOVs/FILE210803-135804F.MOV"]

vcap = cv.VideoCapture(videos[0])
width  = vcap.get(cv.CAP_PROP_FRAME_WIDTH)   # float `width`
height = vcap.get(cv.CAP_PROP_FRAME_HEIGHT)  # float `height

# Create a new video
video = cv.VideoWriter("SPLICED_PD06-04.mp4", cv.VideoWriter_fourcc(*"MPEG"), 60, (1280, 720))

# Write all the frames sequentially to the new video
for v in videos:
    curr_v = cv.VideoCapture(v)
    while curr_v.isOpened():
        r, frame = curr_v.read()    # Get return value and curr frame of curr video
        if not r:
            break
        video.write(frame)          # Write the frame

        print('.')
    print('done')

video.release()                     # Save the video
