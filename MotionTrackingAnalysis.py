import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot
import matplotlib.pyplot as plt

#Reading the File
df = pd.read_csv('2kSample2.csv', error_bad_lines=False)

def FixingEarlyDF(df):
    '''
    Fixing the Y Coordinates and removing the box and stuff
    '''
    Cols = df.columns.values.tolist()
    for i in Cols:
        if "_y" in i:
            df[i] = df[i].apply(lambda x: 1080-x)
    for i in Cols:
        if "_width" in i or "_height" in i:
            df = df.drop([i], axis=1)
            
    return df

def Adjuster(xvals, DiffX):
    '''
    This function fixes the movements in the case of a moving camera by working
    into ref point adjuster
    '''
    for i in range(len(xvals)):
        try:
            for j in range(1, len(xvals[i])):
                x = xvals[i][j]-DiffX[j-1]
                xvals[i].append(x)
        except:
            continue
    for list in range(len(xvals)):
        xvals[list] = (xvals[list][1+len(xvals[list])//2:])
            
    return xvals

def RefPointAdjuster(df):
    '''
    This function fixes the movements in the case of a moving camera, and it works
    the coordinate.
    '''
    #Get the ref. point diff
    try:
        Refx = df['Ref_x'].tolist()
        Refy = df['Ref_y'].tolist()
    except: 
    #This exception works when there is no Ref point identified
        Refx = 0
        Refy = 0
        #Because w this exception you find that the last object doesn't matter so we kick it
        Cols = df.columns.values.tolist()
        df = df.drop(Cols[-1], axis=1)
        df = df.drop(Cols[-2], axis=1)
            
    DiffX = []
    DiffY= []
    for i in range(len(df.index)-1):
        if Refx == 0 and Refy == 0:
            try:
                DiffX.append(0)
                DiffY.append(0)
            except IndexError:
                print("Finished Indexing")
        else:
            try:
                x = Refx[i+1]-Refx[i]
                DiffX.append(x)
                y = Refy[i+1]-Refy[i]
                DiffY.append(y)
            except IndexError:
                print("Hi")

            
    #Apply Ref Changes to all the points
    Cols = df.columns.values.tolist()
    xvals = []
    yvals = []
    for i in Cols:
        if "_x" in i:
            x = df[i].tolist()
            xvals.append(x)
        elif "_y" in i:
            y = df[i].tolist()
            yvals.append(y)
            
    AdjX = Adjuster(xvals, DiffX)
    AdjY = Adjuster(yvals, DiffY)
    n = [AdjX,AdjY,df]
    return n

def DF_Fixer(df, AdjX, AdjY):
    #Now I want to put those changes back into the df
    Cols = df.columns.values.tolist()
    indexX = -1
    indexY = -1
    for i in Cols:
        if "_x" in i:
            indexX += 1
            try:
                df[str(i)]= pd.Series(AdjX[indexX])
            except IndexError:
                print("Indexed:",str(i))
                continue
        elif "_y" in i:
            indexY += 1
            try:
                df[str(i)]= pd.Series(AdjY[indexY])
            except IndexError:
                print("Indexed:",str(i))
                continue
    return df

def FormatDF(df, AdjX):
    #Now we add the frame by frame as time
    Frame = []
    Size = []
    for i in range(len(AdjX[0])):
        Frame.append(i)
        Size.append(15)
    try:
        df['Frame']=pd.Series(Frame)
        df['Size']=pd.Series(Size)
    except IndexError:
                print("Added Frames")
    df = df.dropna(axis=0) 
    
    return df

df = FixingEarlyDF(df)

AdjX = RefPointAdjuster(df)[0]
AdjY = RefPointAdjuster(df)[1]

df = RefPointAdjuster(df)[2]

df = DF_Fixer(df, AdjX, AdjY)

df = FormatDF(df, AdjX)

#Saving this cleaned data for further editing to graph
df.to_csv("CleanData.csv")
