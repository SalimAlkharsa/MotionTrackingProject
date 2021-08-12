import cv2 as cv
import numpy as np
import csv

# Reading Videos
capture = cv.VideoCapture('Test4.mp4') ####input file name

#I want to make the video smaller because that should make it more efficient, actually it became less efficient due to overlap
def FrameScale(Frame, scale=.25):
    # Images, Videos and Live Video
    width = int(Frame.shape[1] * scale)
    height = int(Frame.shape[0] * scale)
    dimensions = (width,height)
    return cv.resize(Frame, dimensions, interpolation=cv.INTER_AREA)

print("Instructions")
print("You will be asked to create the headers by the same order players will be selected")
print("You can either label players by their full first and last names or you can label them by role")
print("For the last 2 data points, you want to enter Ball and Ref Point")

header = []
for i in range(12):
    value = input("Object Name: ")
    for j in range(4):
        if j == 0:
            variable = 'x'
        elif j == 1:
            variable = 'y'
        elif j == 2:
            variable = 'width'
        elif j == 3:
            variable = 'height'
        header.append(value+"_"+variable)
'''
The following loop is modified off a tututorial to match what I want it to do.
The reason I needed the tuturial code was because I needed a wa to end the video 
when the video is done and that is what the 2 if statements do.
'''
Tracker = cv.legacy.MultiTracker_create()

x = 0
FrameNo = 2
ArrayRows = []
while True:
    try:
        isTrue, frame = capture.read()
        FrameScaled = FrameScale(frame, scale=1)
        if x == 0:
            x = 1
            Objects = [5,5,1,1] #This here for game tracking
            ##Objects = [1] #How many items to track for other purposes
            '''
            The Objects are Team 1, Team 2, Ball, Ref
            '''
            for i in Objects:
                for j in range(i):
                    bbi = cv.selectROI('Frame',FrameScaled)
                    Tracker.add(cv.legacy.TrackerCSRT_create(),FrameScaled,bbi)
        if isTrue: 
            FrameScaled = FrameScale(frame, scale=1)
            (success,boxes) = Tracker.update(FrameScaled)
            #np.savetxt('frame_'+str(FrameNo)+'.txt',boxes,fmt='%f')
            ArrayRows.append(boxes)
            #I need to get the data made into a single excel file
            FrameNo+=1
            for box in boxes:
                (x,y,w,h) = [int(a) for a in box]
                cv.rectangle(FrameScaled,(x,y),(x+w,y+h),(0,0,255),2)
            cv.imshow('Video Resized', FrameScaled)
            key = cv.waitKey(5) & 0xFF
            if key == ord('q'):
                break   
        else:
            break
    except:
        continue
print("Done")    
capture.release()
cv.destroyAllWindows()
cv.waitKey(1)

Rows = []
for i in ArrayRows:
    x = i.reshape(-1)
    z = x.tolist()
    Rows.append(z)
with open('2kSample2.csv', 'w') as csvfile: ###This here is what the location data is saved as
    writer = csv.writer(csvfile)
    writer.writerow(header)
    for i in Rows:
       writer.writerow(i)
       
print("Done")
