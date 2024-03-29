#Here we want to format our data frame nicely to something that graphs
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.offline import plot
import matplotlib.pyplot as plt

#Loading and formatting the df
df = pd.read_csv('CleanData.csv', error_bad_lines=False)
df = df.drop(["Unnamed: 0"], axis=1)


#Creating the new df in a good format
Tracked = int(input(("How many objects were tracked? ")))
RowsNeeded = Tracked*len(df.index)
NewDF = pd.DataFrame(np.empty((RowsNeeded, 6)) * np.nan) 
NewDF_Cols = ["Object","Category","Frame","x","y","Size"]
NewDF.columns = NewDF_Cols


#Now populating the names
#Creating the objects column properly
    #First I need to get the names without the x and y
Cols = df.columns.values.tolist()
ObjectName = []
for i in Cols:
    if "_x" in i:
        ObjectName.append(str(i))
      
        
    #Now I have the names and I need to make the list properly    
CurrentRows = 0
RowNames = []
while CurrentRows != RowsNeeded:
    RowNames.append(ObjectName)
    CurrentRows = len(RowNames*Tracked)
ObjectName = []
for item in RowNames:
    for i in item:
        ObjectName.append(i)
RowNames = []
NewDF["Object"] = pd.Series(ObjectName)


    #Now I will make frame
CurrentRows = 0
Frames = []
for i in range(int(RowsNeeded/Tracked)):
    for x in range(Tracked):
        Frames.append(i)
NewDF["Frame"] = pd.Series(Frames)  
    #Now I will make size
CurrentRows = 0
size = []
for i in range(RowsNeeded):    
    size.append(25)
NewDF["Size"] = pd.Series(size)


#Now for the player coordinates
def Adjuster(df, NewDF, indicator = "x"):
    Cols = df.columns.values.tolist()
    xdf = df
    for i in Cols:
        if "_y" in i and indicator == "x":
            xdf = xdf.drop([i], axis=1)
        elif "_x" in i and indicator == "y":
            xdf = xdf.drop([i], axis=1)
        elif "Frame" in i or "Size" in i:
            xdf = xdf.drop([i], axis=1)
    xdf = xdf.transpose()
    Cols = xdf.columns.values.tolist()
    values = []
    for i in range(len(Cols)):
        x = xdf[i].tolist()
        values.append(x)
    Vals_to_add = []
    for list in values:
        for i in list:
           Vals_to_add.append(i) 
    return Vals_to_add
    
XVALS = Adjuster(df, NewDF, indicator = "x")
YVALS = Adjuster(df, NewDF, indicator = "y")

NewDF["x"] = pd.Series(XVALS)
NewDF["y"] = pd.Series(YVALS)

NewDF.to_csv("GraphedReady.csv")
