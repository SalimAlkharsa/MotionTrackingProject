import cv2 as cv
import numpy as np
import csv
#Above we have the necessary libraries imported

#############
#The code and functions to make the program run:

# Reading Videos
capture = cv.VideoCapture('2kTest.mp4') ####input file name


#I want to make the video smaller because that should make it more efficient, actually it became less efficient due to overlap
def FrameScale(Frame, scale=.25):
    print("Now running FrameScale")
    
    # Images, Videos and Live Video
    width = int(Frame.shape[1] * scale)
    height = int(Frame.shape[0] * scale)
    dimensions = (width,height)
    return cv.resize(Frame, dimensions, interpolation=cv.INTER_AREA)


def IntroduceLabels():
    '''
    This function simply introduces the labels, it will see how many objects the operator
    wants to track, the operator will also get to specify the names of the objects

    Returns
    -------
    A list that contains:
        header: this variable will represent all the titles of the objects that are tracked
        iterations: this will show how many objects are being tracked

    '''
    print("Now running IntroduceLabels")
    
    header = []
    value = "hi"
    iterations = -1
    while value != "end":
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
        iterations += 1
    
    return [header, iterations]
    


def TrackerDeploy(iterations, capture):
    '''
    This function will actually take in the video and complete the tracking, spitting it into
    a bunch of numpy arrays which later get sorted to a csv.

    Parameters
    ----------
    iterations : int
        Shows how many objects there are being tracked. It comes from the IntroduceLabels functions and is the
        second index in the return.
    capture : video (?) I do not know what the data structure is called
        This contains the loaded video.

    Returns
    -------
    ArrayRows : numpy array
        Contains the tracked data as a numpy array sorted by frame.

    '''
    
    print("Now running TrackerDeploy")
    
    '''
    The following loop is modified off a tututorial to match what I want it to do.
    The reason I needed the tuturial code was because I needed a way to end the video 
    when the video is done and that is what the 2 if statements do.
    '''
    Tracker = cv.legacy.MultiTracker_create()
    
    x = 0
    FrameNo = 2
    ArrayRows = []
    while True:
        try:
            isTrue, frame = capture.read()
            FrameScaled = FrameScale(frame, scale=1) #This where we can scale the frame, more preprocessing functions can be added if needed
            if x == 0:
                x = 1
                Objects = [iterations] #This here is how many objects are tracked
                for i in Objects: #remember objects was a list of lists so check the logc
                    for j in range(i):
                        bbi = cv.selectROI('Frame',FrameScaled) #selected object
                        Tracker.add(cv.legacy.TrackerCSRT_create(),FrameScaled,bbi) #we track the object
            if isTrue: 
                FrameScaled = FrameScale(frame, scale=1) #This where we can scale the frame, more preprocessing functions can be added if needed
                (success,boxes) = Tracker.update(FrameScaled)
                ArrayRows.append(boxes)
                #I need to get the data made into a single excel file
                FrameNo+=1
                for box in boxes:
                    (x,y,w,h) = [int(a) for a in box] #my friend helped me with the following lines a little bit to work the logic out
                    cv.rectangle(FrameScaled,(x,y),(x+w,y+h),(0,0,255),2)
                cv.imshow('Video Resized', FrameScaled)
                key = cv.waitKey(5) & 0xFF
                if key == ord('q'): #stops tracking at q
                    break   
            else:
                break
        except:
            continue
    print("Done")    
    capture.release()
    cv.destroyAllWindows()
    cv.waitKey(1)
    
    return ArrayRows



def npToCSV(ArrayRows, InitialCSVFileSave):
    '''
    This function will turn the NP array to a csv.
    
    Parameters
    ----------
    ArrayRows : npArray
        Comes from the tracker deploy function.
    InitialCSVFileSave : str
        What the file will be named as in the directory.

    Returns
    -------
    Nothing is returned, the file is simply made and ready to be found in the directory.

    '''
    print("Now running npToCSV")
    
    Rows = []
    for i in ArrayRows:
        x = i.reshape(-1)
        z = x.tolist()
        Rows.append(z)
    with open(InitialCSVFileSave+'.csv', 'w') as csvfile: ###This here is what the location data is saved as
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for i in Rows:
           writer.writerow(i)
           
    print("Done")
    
#############
#The functions and prints called to run the program:
    
print("Instructions")
print("You will be asked to create the headers by the same order players will be selected")
print("You can either label players by their full first and last names or you can label them by role")
print("To stop accepting objects type: end")

IntroduceLabelsList = IntroduceLabels()
header =  IntroduceLabelsList[0]
iterations = IntroduceLabelsList[1]

ArrayRows = TrackerDeploy(iterations, capture)
InitialCSVFileSave = input(str("What would you like the saved csv to be named as? DO NOT INCLUDE CSV: "))

npToCSV(ArrayRows, InitialCSVFileSave)
