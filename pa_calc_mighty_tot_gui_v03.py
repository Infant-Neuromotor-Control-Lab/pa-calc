# @file pa_calc_mighty_tot_gui_v03.py
#
# @brief Calculate physical activity intensity for infants.
#
# Calculate based on a single ankle-worn accelerometer. Infants should be 
# pre-ambulatory) not yet walking. 
#
# Need time (s) and 3D accelerometer data (m/s2) sampled  at 20 Hz. Code can be 
# modified for higher sampling rates.the approach should work the same, i.e.
# intergrating over 2 seconds, regardless of sampling rate.
# 
# Based on the following paper:
#
# Ghazi MA, Zhou J, Havens KL, Smith BA. Accelerometer Thresholds for Estimating 
# Physical Activity Intensity Levels in Infants: A Preliminary Study. Sensors. 
# 2024; 24(14):4436
#
# Based on pa_calc_mighty_tot_v03 which in turn is based on mighty_tot_calc_v01
#
# Computation steps:
#
# -Calculate magnitude
#
# -Calculate baseline, a_G  
# ****************  TRY DO DO ALL OF THESE IN ONE LOOP? *****************
# -Calculate gravity independent magnitude of acceleration, a_IND, 
# -Scale the acceleration by leg length, a_ADJ
# -Calculate computed quantity (jerk or accel), left
# -Assign label based on threshold
# ****************  TRY DO DO ALL OF THESE IN ONE LOOP? *****************
# -Compile statistics (num points in each category, percentage activity)
#
# Known bugs:
# -Last line of raw output file may have just zeros
#
# -Tkinter general guide
#  https://realpython.com/python-gui-tkinter/#displaying-text-and-images-with-label-widgets
# -Combobox widget
#  https://www.geeksforgeeks.org/combobox-widget-in-tkinter-python/
# -Display background image
#  https://www.activestate.com/resources/quick-reads/how-to-add-images-in-tkinter/
# -Modify fonts for combobox list elements (not selected entry)
#  https://stackoverflow.com/questions/28938758/combobox-fontsize-in-tkinter
# -Modify fonts for combobox entry/selected element only
#   https://thelinuxcode.com/tkinter-combobox/
# TODO Scroll bar on textbox
#  https://pythonguides.com/python-tkinter-text-box/
# -Autoscroll textbox to the end
#  https://stackoverflow.com/questions/49245807/tkinter-autoscroll-to-bottom
# -Tkinter file open dialog box
#  https://www.w3resource.com/python-exercises/tkinter/python-tkinter-dialogs-and-file-handling-exercise-3.php
#
#
# Created 09 May 2024
# Modified 10 July 2024 (V02)
# Modified 20 July 2024 (V03)
# -Added load from .tsv
# -Fixed full results write (raw)
# -Removed some unused commented code
# -Merged mightytotutils messages with GUI messages
# -Fixed user input global variable changing bug
# -Fixed output file name global variables bug
# -Fixed global output file extension global variable bug
# -Added heading yyy, mm, dd, hh, mm, ss
# -Fixed picture resolution and positions
#
# @author Mustafa Ghazi

# graphical user interface
import tkinter
from tkinter import ttk
import tkinter.font
import tkinter.filedialog
from PIL import Image, ImageTk
# analysis
import numpy as np
# handling time
from datetime import datetime, timezone
import time
import pytz
# text for the messages to display
import displaytexts
# based on pa_calc_mighty_tot_v03
import mightytotutilsv03 as pa

# Global variables
# file load will populate these variables, data type can be different too
fileInReadSensorTime = 0 
fileInReadSensorAccelXYZ = 0 
minInputFileTime = 0 
maxInputFileTime = 0


def funcButtonExample ():
    print("Exmaple button pressed")
 
# @brief Load sensor data from file
#
def funcButtonLoadFile ():
    
    # file read input
    global fileInReadSensorTime 
    global fileInReadSensorAccelXYZ
    global minInputFileTime
    global maxInputFileTime
    
    printToPrintBuffer("Load file button pressed")
    printToPrintBuffer("INFO: Please be patient. Loading a file can take 5-10 minutes depending on file size.")
    filePath = tkinter.filedialog.askopenfilename(title="Select a file",filetypes=[("Tab separated text files", "*.tsv"), ("All files", "*.*")])
    if(filePath):
        # a file path has been selected
        thisFilePathStr, thisFileNameNoExtensionStr, thisFileExtensionStr = parseFilePathString (filePath, "/", ".t")
        printToPrintBuffer("Full file path is " + filePath)
        printToPrintBuffer("File directory is "+ thisFilePathStr + " name is" + thisFileNameNoExtensionStr + " extension is " + thisFileExtensionStr)
        # STEP 1: LOAD FILE, DISPLAY FILE START/END TIME 
        labelFileName.config(text=thisFileNameNoExtensionStr + thisFileExtensionStr)
        fileInReadSensorTime, fileInReadSensorAccelXYZ, minInputFileTime, maxInputFileTime = pa.loadFileDisplayFile(thisFilePathStr, thisFileNameNoExtensionStr, thisFileExtensionStr)
        displayTimeFromFileGUI(minInputFileTime, maxInputFileTime)
        displayPrintBufferToGUI() # update any prints generates in mightytotutils
        pa.fileNameNoExtension = thisFileNameNoExtensionStr # update global info about this
        pa.outputFileExtension = ".txt"
        pa.fileReadErrorFlag = 0 # 0 if no error, 1 if error
    else:
        printToPrintBuffer("File path does not exist. TODO: Need to set a flag for file selection, etc.")
        pa.fileReadErrorFlag = 1 # 0 if no error, 1 if error


# @brief Look up typical leg lengths for infants at different ages
#
def funcButtonLookUp ():
    print("Look up button pressed")
    tkinter.messagebox.showinfo("Look up typical leg lengths of infants", displaytexts.textLookUp)
 
    
# @brief Show brief instructions on using the software
#
def funcButtonHelp ():
    printToPrintBuffer("Help button pressed")
    tkinter.messagebox.showinfo("Help", displaytexts.textHelp)

# @brief Calculate physical activity
#    
def funcButtonCalculate ():
    

    pa.constRefLegLength3To5MonthCm
    
    # file io stuff
    # global fileNameNoExtension  # same 3 day above
    # global fileNameAppendRaw # time, type, 0.05 s interval
    # global fileNameAppendBouts # start time, end time, type
    # global fileNameAppendSummary  # OVer pct and time
    # global fileNameAppendErrorLog  # All messages and errors from code
    # global inputFileExtension
    #global outputFileExtension 
    # global inputDir
    pa.outputDir 
    
    # file read input (global)
    global fileInReadSensorTime 
    global fileInReadSensorAccelXYZ
    global minInputFileTime
    global maxInputFileTime
        
    printToPrintBuffer("Calculate button pressed")
    # textboxConsoleWindow.config(state="normal")
    # textboxConsoleWindow.delete('0.0', "end")
    # textboxConsoleWindow.insert("0.0", displaytexts.textTest)
    # textboxConsoleWindow.config(state="disabled")
    
    sError, sDateTime = funcButtonGetUserStartDateTime()
    eError, eDateTime = funcButtonGetUserEndDateTime()
    
    # set those global variables for processing by processDataSaveResults()
    # processing options
    qError, pa.computedQttyOption = funcGetUserComputedQuantity()
    oError, pa.optimizationTypeOption = funcGetUserThresholdType()
    gError, pa.infantLegLengthCm = funcGetUserLegLength()
    
    # start time, epoch time UTC time zone
    pa.userInputStartYear = sDateTime[0,0]
    pa.userInputStartMonth = sDateTime[1,0]
    pa.userInputStartDay = sDateTime[2,0] 
    pa.userInputStartHour = sDateTime[3,0] 
    pa.userInputStartMinute = sDateTime[4,0]
    pa.userInputStartSecond = sDateTime[5,0]
    # end time, epoch time UTC time zone
    pa.userInputEndYear = eDateTime[0,0]
    pa.userInputEndMonth = eDateTime[1,0]
    pa.userInputEndDay = eDateTime[2,0] 
    pa.userInputEndHour = eDateTime[3,0] 
    pa.userInputEndMinute = eDateTime[4,0]
    pa.userInputEndSecond = eDateTime[5,0]
    
    
    if (sError == 0) and (eError == 0) and (qError == 0) and (oError == 0) and (gError == 0):
        myStartStr = "%04d-%02d-%02d %02d:%02d:%02d" % (sDateTime[0,0], sDateTime[1,0], sDateTime[2,0], sDateTime[3,0], sDateTime[4,0], sDateTime[5,0])
        myEndStr = "%04d-%02d-%02d %02d:%02d:%02d" % (eDateTime[0,0], eDateTime[1,0], eDateTime[2,0], eDateTime[3,0], eDateTime[4,0], eDateTime[5,0])
        #myStartStr = "%04d-%02d-%02d %02d:%02d:%02d" % ((sDateTime[0,0]), (sDateTime[0,1]), (sDateTime[0,2]), (sDateTime[0,3]), (sDateTime[0,4]), (sDateTime[0,5]))
        #myEndStr = "%04d-%02d-%02d %02d:%02d:%02d" % ((eDateTime[0,0]), (eDateTime[0,1]), (eDateTime[0,2]), (eDateTime[0,3]), (eDateTime[0,4]), (eDateTime[0,5]))
        printToPrintBuffer("User entered start time: " + myStartStr + "\nUser entered end time: " + myEndStr)
        pa.processDataSaveResults(fileInReadSensorTime, fileInReadSensorAccelXYZ, minInputFileTime, maxInputFileTime)
        printToPrintBuffer("INFO: GUI done!") # This last line won't be logged to file but it will trigger display of all messages from mightytotutils
 
    
def funcButtonGetUserStartDateTime ():
    
    error = 0 # 0 if no error, 1 if error
    result = np.zeros((6,1),dtype=np.int64)
    # first check if any blank
    if (listboxUserStartTimeYear.get() == "") or (listboxUserStartTimeMonth.get() == "") or (listboxUserStartTimeDay.get() == "") or (listboxUserStartTimeHour.get() == "") or (listboxUserStartTimeMinute.get() == "") or (listboxUserStartTimeSecond.get() == ""):
        printToPrintBuffer("ERROR: One of the start date/time fields are blank.")
        error = 1
    else:
        # get the values
        thisYear = int(listboxUserStartTimeYear.get())
        thisMonth = int(listboxUserStartTimeMonth.get())
        thisDay = int(listboxUserStartTimeDay.get())
        thisHour = int(listboxUserStartTimeHour.get())
        thisMinute = int(listboxUserStartTimeMinute.get())
        thisSecond = int(listboxUserStartTimeSecond.get())
        result = np.array(([[thisYear],
                            [thisMonth],
                            [thisDay],
                            [thisHour],
                            [thisMinute],
                            [thisSecond]]),dtype=np.int64)
        
        # further, check if any months are incorrectly 31
        # Apr, Jun, Sep, Nov (4, 6, 9, 11) cannot be > 30
        # Feb (2) cannot be > 29
        if  ( (((thisMonth == 4) or (thisMonth == 6) or (thisMonth == 9) or (thisMonth == 11)) and (thisDay > 30)) or ((thisMonth == 2) and (thisDay > 29))  ):
            printToPrintBuffer("ERROR: Incorrect start date. Entered month does not have this many days.")
            error = 1
        else:
            error = 0
        
    return error, result
        
        
 
    
def funcButtonGetUserEndDateTime ():
     
    error = 0 # 0 if no error, 1 if error
    result = np.zeros((6,1),dtype=np.int64)
     # first check if any blank
    if (listboxUserEndTimeYear.get() == "") or (listboxUserEndTimeMonth.get() == "") or (listboxUserEndTimeDay.get() == "") or (listboxUserEndTimeHour.get() == "") or (listboxUserEndTimeMinute.get() == "") or (listboxUserEndTimeSecond.get() == ""):
        printToPrintBuffer("ERROR: One of the end date/time fields are blank.")
        error = 1
    else:
        # get the values
        thisYear = int(listboxUserEndTimeYear.get())
        thisMonth = int(listboxUserEndTimeMonth.get())
        thisDay = int(listboxUserEndTimeDay.get())
        thisHour = int(listboxUserEndTimeHour.get())
        thisMinute = int(listboxUserEndTimeMinute.get())
        thisSecond = int(listboxUserEndTimeSecond.get())
        result = np.array(([[thisYear],
                            [thisMonth],
                            [thisDay],
                            [thisHour],
                            [thisMinute],
                            [thisSecond]]),dtype=np.int64)
        # further, check if any months are incorrectly 31
        # Apr, Jun, Sep, Nov (4, 6, 9, 11) cannot be > 30
        # Feb (2) cannot be > 29
        if  ( (((thisMonth == 4) or (thisMonth == 6) or (thisMonth == 9) or (thisMonth == 11)) and (thisDay > 30)) or ((thisMonth == 2) and (thisDay > 29))  ):
            printToPrintBuffer("ERROR: Incorrect start date. Entered month does not have this many days.")
            error = 1
        else:
            error = 0
        
    return error, result
        

# @brief Read the computed quantity option, with checks
#
def funcGetUserComputedQuantity():
    
    error = 0 # 0 if no error, 1 if error
    result = ""
    
    # first check if not blank
    if (listboxUserComputedQuantity.get() == ""):
        printToPrintBuffer("Error: Computed quantity option is blank.")
        error = 1
    else:
        result = listboxUserComputedQuantity.get()
    
    return error, result


# @brief Read the threshold type option, with checks
#
def funcGetUserThresholdType():
    
    error = 0 # 0 if no error, 1 if error
    result = ""
    
    # first check if not blank
    if (listboxUserThresholdType.get() == ""):
        printToPrintBuffer("Error: Threshold type option is blank.")
        error = 1
    else:
        result = listboxUserThresholdType.get()
    
    return error, result


# @brief Read the leg legnth, with checks
#
def funcGetUserLegLength():
    
    error = 0 # 0 if no error, 1 if error
    result = ""
    
    # first check if not blank
    if (listboxUserLegLength.get() == ""):
        printToPrintBuffer("Error: Leg length option is blank.")
        error = 1
    else:
        result = float(listboxUserLegLength.get())
    
    return error, result


# @brief Add a string to the print buffer
#
# @param thisString String to print
#
def printToPrintBuffer(thisString):
        
    displaytexts.printBufferStr = displaytexts.printBufferStr + '\n' + thisString
    displayPrintBufferToGUI()
    
    
# @brief Display the full print buffer to the display area
#
# 
def displayPrintBufferToGUI():
      
    textboxConsoleWindow.config(state="normal")
    textboxConsoleWindow.delete("0.0", "end")
    textboxConsoleWindow.insert("0.0", displaytexts.printBufferStr)
    textboxConsoleWindow.yview(tkinter.END)
    textboxConsoleWindow.config(state="disabled")
    

# @brief Given a full file path, parse the directory/file name
# 
# directoryChar is usually '/' and this also mostly works on Windows OS, but 
# sometimes may need to use '\' on Windows OS.
#
# @param inputStr Complete file path string (dir, name, extension)
# @param directoryChar Character used to separate the directory, typically '/' 
# @param fExtensionStr First two characters in file extension, including "." e.g. ".t" for ".txt" 
#
# @return The file path without the file name and the last '/'
# @return The file name without the extension
# @return The complete file extension with "." e.g. ".txt"
#
def parseFilePathString (inputStr, directoryChar, fExtensionStr):
    
    
    maxNum = len(inputStr) 
    i = maxNum-1
    fNameIndex = maxNum-1
    fExtensionIndex = maxNum-1-1
    
    myFilePathStr = ''
    myFileNameNoExtensionStr = ''
    myFileExtensionStr = ''
    
    # check if both are present in there
    if (directoryChar in inputStr) and (fExtensionStr in inputStr):
        
        # search for the start of file name
        # start form end of string
        while(i >=0):
            if(inputStr[i] == directoryChar):
                fNameIndex = i
                break
            i = i - 1
          
        fNameIndex = fNameIndex + 1 # start of file name is at +1, so fix that 
    
        # search for the start of file extension
        # start form end of string
        i = maxNum-1-1
        while(i >=0):
            if(inputStr[i] == fExtensionStr[0]) and (inputStr[i+1] == fExtensionStr[1]):
                fExtensionIndex = i
                break
            i = i - 1
    
        
        i = 0
        while(i < (fNameIndex - 1)):
            myFilePathStr = myFilePathStr + inputStr[i]
            i = i + 1
            
        i = fNameIndex
        while (i < fExtensionIndex):        
            myFileNameNoExtensionStr = myFileNameNoExtensionStr + inputStr[i]
            i = i + 1
        
        i = fExtensionIndex
        while (i < maxNum):
            myFileExtensionStr = myFileExtensionStr + inputStr[i]
            i = i + 1
    
    else:
        print("ERROR: Directory character or file extension are missing from file path")
        
    return myFilePathStr, myFileNameNoExtensionStr, myFileExtensionStr


# @brief Show the user the start and end times from file
#    
# TODO: format single/double digit?
#
def displayTimeFromFileGUI(startTime, endTime):
    myStartTimeObj = datetime.utcfromtimestamp(startTime)
    myEndTimeObj = datetime.utcfromtimestamp(endTime)
    
    labelFileStartTimeYear.config(text=str(myStartTimeObj.year))  
    labelFileStartTimeMonth.config(text=str(myStartTimeObj.month)) 
    labelFileStartTimeDay.config(text=str(myStartTimeObj.day)) 
    labelFileStartTimeHour.config(text=str(myStartTimeObj.hour)) 
    labelFileStartTimeMinute.config(text=str(myStartTimeObj.minute)) 
    labelFileStartTimeSecond.config(text=str(myStartTimeObj.second)) 
    
    labelFileEndTimeYear.config(text=str(myEndTimeObj.year))  
    labelFileEndTimeMonth.config(text=str(myEndTimeObj.month)) 
    labelFileEndTimeDay.config(text=str(myEndTimeObj.day)) 
    labelFileEndTimeHour.config(text=str(myEndTimeObj.hour)) 
    labelFileEndTimeMinute.config(text=str(myEndTimeObj.minute)) 
    labelFileEndTimeSecond.config(text=str(myEndTimeObj.second)) 
    
    
root = tkinter.Tk()
root.wm_title("Mighty Tot Physical Activity Calculator")
root.geometry("830x1080")
labelColorBackground = "#00B0F0"
buttonColorBackground = "#70AD47"
guiColorBackground = "#4472C4"
root.configure(bg=guiColorBackground)

# ****************************************************************************

# This modifies fonts of all of the elements within a listbox created after this call
# This does not modify the font of the selected/entered element
# To modify font for selected/entered element, use .config(font='Arial 12 bold')
listboxListFont = tkinter.font.Font(family="Arial",size=12,weight="bold") # also add bold
root.option_add("*TCombobox*Listbox*Font", listboxListFont)

buttonFontTuple = ("Arial", 12, "bold") # font for all of the buttons
labelFontTuple = ("Arial", 12, "bold") # font for all of the labels


# Baby image
# ****************************************************************************
# image1 = Image.open("pexels-goda-morgan-121487563-18649618-gif.gif")
image1 = Image.open("pexels-goda-morgan-121487563-18649618_png.png")
imageTkImage1 = ImageTk.PhotoImage(image1)
labelBabyImage = tkinter.Label(image=imageTkImage1)
labelBabyImage.image = imageTkImage1

# Buttons
# ****************************************************************************
buttonExample = tkinter.Button(
    master=root, 
    text="EXAMPLE", 
    width=10, 
    height=1, 
    font=buttonFontTuple, 
    background=buttonColorBackground,
    command=funcButtonExample
    )

buttonLoadFile = tkinter.Button(
    master=root, 
    text="Load file", 
    width=10, 
    height=1, 
    font=buttonFontTuple, 
    background=buttonColorBackground,
    command=funcButtonLoadFile
    )

buttonLookUp = tkinter.Button(
    master=root, 
    text="Look up \ntypical leg \nlengths", 
    width=10, 
    height=3,
    font=buttonFontTuple, 
    background=buttonColorBackground,
    command=funcButtonLookUp
    )

buttonHelp = tkinter.Button(
    master=root, 
    text="Help", 
    width=10, 
    height=1, 
    font=buttonFontTuple,
    background=buttonColorBackground,
    command=funcButtonHelp
    )

buttonCalculate = tkinter.Button(
    master=root, 
    text="Calculate", 
    width=10, 
    height=1, 
    font=buttonFontTuple, 
    background=buttonColorBackground,
    command=funcButtonCalculate
    )

# filestats labels
# ****************************************************************************
labelFileStats = tkinter.Label(
    master=root, text="File stats:", width=12, background=labelColorBackground, font=labelFontTuple)

labelFileName = tkinter.Label(
    master=root, text="sample_file_name.txt", background=labelColorBackground, font=labelFontTuple)

# File start time labels
# ****************************************************************************
labelFileStartTime = tkinter.Label(
    master=root, text="File start time:", width=12, background=labelColorBackground, font=labelFontTuple)

labelFileStartTimeYear = tkinter.Label(
    master=root, text="YYYY", width=5, background=labelColorBackground, font=labelFontTuple)

labelFileStartTimeMonth = tkinter.Label(
    master=root, text="MM", width=5, background=labelColorBackground, font=labelFontTuple)

labelFileStartTimeDay = tkinter.Label(
    master=root, text="DD", width=5, background=labelColorBackground, font=labelFontTuple)

labelFileStartTimeHour = tkinter.Label(
    master=root, text="hh", width=5, background=labelColorBackground, font=labelFontTuple)

labelFileStartTimeMinute= tkinter.Label(
    master=root, text="mm", width=5, background=labelColorBackground, font=labelFontTuple)

labelFileStartTimeSecond = tkinter.Label(
    master=root, text="ss", width=5, background=labelColorBackground, font=labelFontTuple)

# File end time labels
# ****************************************************************************
labelFileEndTime = tkinter.Label(
    master=root, text="File end time:", width=12, background=labelColorBackground, font=labelFontTuple)

labelFileEndTimeYear = tkinter.Label(
    master=root, text="YYYY", width=5, background=labelColorBackground, font=labelFontTuple)

labelFileEndTimeMonth = tkinter.Label(
    master=root, text="MM", width=5, background=labelColorBackground, font=labelFontTuple)

labelFileEndTimeDay = tkinter.Label(
    master=root, text="DD", width=5, background=labelColorBackground, font=labelFontTuple)

labelFileEndTimeHour = tkinter.Label(
    master=root, text="hh", width=5, background=labelColorBackground, font=labelFontTuple)

labelFileEndTimeMinute= tkinter.Label(
    master=root, text="mm", width=5, background=labelColorBackground, font=labelFontTuple)

labelFileEndTimeSecond = tkinter.Label(
    master=root, text="ss", width=5, background=labelColorBackground, font=labelFontTuple)

# User input time labels
# ****************************************************************************
labelUserInTimeYear = tkinter.Label(
    master=root, text="YYYY", width=5, background=labelColorBackground, font=labelFontTuple)

labelUserInTimeMonth = tkinter.Label(
    master=root, text="MM", width=5, background=labelColorBackground, font=labelFontTuple)

labelUserInTimeDay = tkinter.Label(
    master=root, text="DD", width=5, background=labelColorBackground, font=labelFontTuple)

labelUserInTimeHour = tkinter.Label(
    master=root, text="hh", width=5, background=labelColorBackground, font=labelFontTuple)

labelUserInTimeMinute= tkinter.Label(
    master=root, text="mm", width=5, background=labelColorBackground, font=labelFontTuple)

labelUserInTimeSecond = tkinter.Label(
    master=root, text="ss", width=5, background=labelColorBackground, font=labelFontTuple)

# User start time stuff
# ****************************************************************************
labelUserStartTime = tkinter.Label(
    master=root, text="Start time:", width=12, background=labelColorBackground, font=labelFontTuple)

varUserStartYears = tkinter.StringVar()
listboxUserStartTimeYear = tkinter.ttk.Combobox(
    root,
    state="readonly",
    width = 5,
    textvariable = varUserStartYears
    )
listboxUserStartTimeYear['values'] = ("2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024","2025","2026","2027","2028","2029","2030","2031","2032","2033","2034","2035","2036","2037","2038","2039")
listboxUserStartTimeYear.config(font='Arial 12 bold') # Modify font for selected/entered element

varUserStartMonths = tkinter.StringVar()
listboxUserStartTimeMonth = tkinter.ttk.Combobox(
    root,
    state="readonly",
    width = 5,
    textvariable = varUserStartMonths
    )
listboxUserStartTimeMonth['values'] = ("1","2","3","4","5","6","7","8","9","10","11","12")
listboxUserStartTimeMonth.config(font='Arial 12 bold') # Modify font for selected/entered element

varUserStartDays = tkinter.StringVar()
listboxUserStartTimeDay = tkinter.ttk.Combobox(
    root,
    state="readonly",
    width = 5,
    textvariable = varUserStartDays
    )
listboxUserStartTimeDay['values'] = ("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31")
listboxUserStartTimeDay.config(font='Arial 12 bold') # Modify font for selected/entered element

varUserStartHours = tkinter.StringVar()
listboxUserStartTimeHour = tkinter.ttk.Combobox(
    root,
    state="readonly",
    width = 5,
    textvariable = varUserStartHours
    )
listboxUserStartTimeHour['values'] = ("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23")
listboxUserStartTimeHour.config(font='Arial 12 bold') # Modify font for selected/entered element

varUserStartMinutes = tkinter.StringVar()
listboxUserStartTimeMinute = tkinter.ttk.Combobox(
    root,
    state="readonly",
    width = 5,
    textvariable = varUserStartMinutes
    )
listboxUserStartTimeMinute['values'] = ("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59")
listboxUserStartTimeMinute.config(font='Arial 12 bold') # Modify font for selected/entered element

varUserStartSeconds= tkinter.StringVar()
listboxUserStartTimeSecond = tkinter.ttk.Combobox(
    root,
    state="readonly",
    width = 5,
    textvariable = varUserStartSeconds
    )
listboxUserStartTimeSecond['values'] = ("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59")
listboxUserStartTimeSecond.config(font='Arial 12 bold') # Modify font for selected/entered element

# User end time stuff
# ****************************************************************************
labelUserEndTime = tkinter.Label(
    master=root, text="End time:", width=12, background=labelColorBackground, font=labelFontTuple)

varUserEndYears = tkinter.StringVar()
listboxUserEndTimeYear = tkinter.ttk.Combobox(
    root,
    state="readonly",
    width = 5,
    textvariable = varUserEndYears
    )
listboxUserEndTimeYear['values'] = ("2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024","2025","2026","2027","2028","2029","2030","2031","2032","2033","2034","2035","2036","2037","2038","2039")
listboxUserEndTimeYear.config(font='Arial 12 bold') # Modify font for selected/entered element

varUserEndMonths = tkinter.StringVar()
listboxUserEndTimeMonth = tkinter.ttk.Combobox(
    root,
    state="readonly",
    width = 5,
    textvariable = varUserEndMonths
    )
listboxUserEndTimeMonth['values'] = ("1","2","3","4","5","6","7","8","9","10","11","12")
listboxUserEndTimeMonth.config(font='Arial 12 bold') # Modify font for selected/entered element

varUserEndDays = tkinter.StringVar()
listboxUserEndTimeDay = tkinter.ttk.Combobox(
    root,
    state="readonly",
    width = 5,
    textvariable = varUserEndDays
    )
listboxUserEndTimeDay['values'] = ("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31")
listboxUserEndTimeDay.config(font='Arial 12 bold') # Modify font for selected/entered element

varUserEndHours = tkinter.StringVar()
listboxUserEndTimeHour = tkinter.ttk.Combobox(
    root,
    state="readonly",
    width = 5,
    textvariable = varUserEndHours
    )
listboxUserEndTimeHour['values'] = ("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23")
listboxUserEndTimeHour.config(font='Arial 12 bold') # Modify font for selected/entered element

varUserEndMinutes = tkinter.StringVar()
listboxUserEndTimeMinute = tkinter.ttk.Combobox(
    root,
    state="readonly",
    width = 5,
    textvariable = varUserEndMinutes
    )
listboxUserEndTimeMinute['values'] = ("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59")
listboxUserEndTimeMinute.config(font='Arial 12 bold') # Modify font for selected/entered element

varUserEndSeconds= tkinter.StringVar()
listboxUserEndTimeSecond = tkinter.ttk.Combobox(
    root,
    state="readonly",
    width = 5,
    textvariable = varUserEndSeconds
    )
listboxUserEndTimeSecond['values'] = ("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59")
listboxUserEndTimeSecond.config(font='Arial 12 bold') # Modify font for selected/entered element

# leg length stuff
labelUserLegLength = tkinter.Label(
    master=root, text="Leg length (cm):", width=15, background=labelColorBackground, font=labelFontTuple)

varUserLegLength = tkinter.StringVar()
listboxUserLegLength = tkinter.ttk.Combobox(
    root,
    state="readonly",
    width = 15,
    textvariable = varUserLegLength
    )
listboxUserLegLength['values'] = ("10","10.5","11","11.5","12","12.5","13","13.5","14","14.5","15","15.5","16","16.5","17","17.5","18","18.5","19","19.5","20","20.5","21","21.5","22","22.5","23","23.5","24","24.5","25","25.5","26","26.5","27","27.5","28","28.5","29","29.5","30","30.5","31","31.5","32","32.5","33","33.5","34","34.5","35","35.5","36","36.5","37","37.5","38","38.5","39","39.5","40","40.5","41","41.5","42","42.5","43","43.5","44","44.5","45","45.5","46","46.5","47","47.5","48","48.5","49","49.5","50","50.5","51","51.5","52","52.5","53","53.5","54","54.5","55")
listboxUserLegLength.config(font='Arial 12 bold') # Modify font for selected/entered element

# Computed quantity stuff
# ****************************************************************************
labelUserComputedQuantity = tkinter.Label(
    master=root, text="Computed quantity:", width=15, background=labelColorBackground, font=labelFontTuple)

varUserComputedQuantity = tkinter.StringVar()
listboxUserComputedQuantity = tkinter.ttk.Combobox(
    root,
    state="readonly",
    width = 15,
    textvariable = varUserComputedQuantity
    )
listboxUserComputedQuantity['values'] = ("acceleration", "jerk")
listboxUserComputedQuantity.config(font='Arial 12 bold') # Modify font for selected/entered element

# Threshold type stuff
# ****************************************************************************
labelUserThresholdType = tkinter.Label(
    master=root, text="Threshold type:", width=15, background=labelColorBackground, font=labelFontTuple)

varUserThresholdType = tkinter.StringVar()
listboxUserThresholdType = tkinter.ttk.Combobox(
    root,
    state="readonly",
    width = 15,
    textvariable = varUserThresholdType
    )
listboxUserThresholdType['values'] = ("TP", "PAP")
listboxUserThresholdType.config(font='Arial 12 bold') # Modify font for selected/entered element


# Console window
# ****************************************************************************
textboxConsoleWindow = tkinter.Text(
    master=root, 
    wrap=tkinter.WORD,
    width=62, 
    height=8,
    background="black", 
    foreground="white", 
    font=labelFontTuple
    )
textboxConsoleWindow.config(state="disabled")

# ****************************************************************************
# ****************************************************************************

# buttonExample.place(x=800, y=800)

# Baby image
# ****************************************************************************
labelBabyImage.place(x=300, y=40)

# File stats labels
# ****************************************************************************
labelFileStats.place(x=10, y=130+50+25)
labelFileName.place(x=10, y=130+50+1*75)
buttonLoadFile.place(x=660, y=130+50)

# File start time labels
# ****************************************************************************
lfstOffsetX = 120
lfstSpacerX = 100
lfstY = 130+75+2*50
labelFileStartTime.place(x=10, y=lfstY)
labelFileStartTimeYear.place(x=lfstOffsetX+1*lfstSpacerX, y=lfstY)
labelFileStartTimeMonth.place(x=lfstOffsetX+2*lfstSpacerX, y=lfstY)
labelFileStartTimeDay.place(x=lfstOffsetX+3*lfstSpacerX, y=lfstY)
labelFileStartTimeHour.place(x=lfstOffsetX+4*lfstSpacerX, y=lfstY)
labelFileStartTimeMinute.place(x=lfstOffsetX+5*lfstSpacerX, y=lfstY)
labelFileStartTimeSecond.place(x=lfstOffsetX+6*lfstSpacerX, y=lfstY)

# File end time labels
# ****************************************************************************
lfetOffsetX = 120
lfetSpacerX = 100
lfetY = 130+75+3*50
labelFileEndTime.place(x=10, y=lfetY)
labelFileEndTimeYear.place(x=lfetOffsetX+1*lfetSpacerX, y=lfetY)
labelFileEndTimeMonth.place(x=lfetOffsetX+2*lfetSpacerX, y=lfetY)
labelFileEndTimeDay.place(x=lfetOffsetX+3*lfetSpacerX, y=lfetY)
labelFileEndTimeHour.place(x=lfetOffsetX+4*lfetSpacerX, y=lfetY)
labelFileEndTimeMinute.place(x=lfetOffsetX+5*lfetSpacerX, y=lfetY)
labelFileEndTimeSecond.place(x=lfetOffsetX+6*lfetSpacerX, y=lfetY)

# User input time labels
# ****************************************************************************
lfetOffsetX = 120
lfetSpacerX = 100
lfetY = 130+75+4*50

labelUserInTimeYear.place(x=lfetOffsetX+1*lfetSpacerX, y=lfetY)
labelUserInTimeMonth.place(x=lfetOffsetX+2*lfetSpacerX, y=lfetY)
labelUserInTimeDay.place(x=lfetOffsetX+3*lfetSpacerX, y=lfetY)
labelUserInTimeHour.place(x=lfetOffsetX+4*lfetSpacerX, y=lfetY)
labelUserInTimeMinute.place(x=lfetOffsetX+5*lfetSpacerX, y=lfetY)
labelUserInTimeSecond.place(x=lfetOffsetX+6*lfetSpacerX, y=lfetY)

# User start time stuff
# ****************************************************************************
lustOffsetX = 120
lustSpacerX = 100
lustY = 130+75+5*50
labelUserStartTime.place(x=10, y=lustY)
listboxUserStartTimeYear.place(x=lustOffsetX+1*lustSpacerX, y=lustY)
listboxUserStartTimeMonth.place(x=lustOffsetX+2*lustSpacerX, y=lustY)
listboxUserStartTimeDay.place(x=lustOffsetX+3*lustSpacerX, y=lustY)
listboxUserStartTimeHour.place(x=lustOffsetX+4*lustSpacerX, y=lustY)
listboxUserStartTimeMinute.place(x=lustOffsetX+5*lustSpacerX, y=lustY)
listboxUserStartTimeSecond.place(x=lustOffsetX+6*lustSpacerX, y=lustY)

# User end time stuff
# ****************************************************************************
luetOffsetX = 120
luetSpacerX = 100
luetY = 130+75+6*50
labelUserEndTime.place(x=10, y=luetY)
listboxUserEndTimeYear.place(x=luetOffsetX+1*luetSpacerX, y=luetY)
listboxUserEndTimeMonth.place(x=luetOffsetX+2*luetSpacerX, y=luetY)
listboxUserEndTimeDay.place(x=luetOffsetX+3*luetSpacerX, y=luetY)
listboxUserEndTimeHour.place(x=luetOffsetX+4*luetSpacerX, y=luetY)
listboxUserEndTimeMinute.place(x=luetOffsetX+5*luetSpacerX, y=luetY)
listboxUserEndTimeSecond.place(x=luetOffsetX+6*luetSpacerX, y=luetY)

# leg length stuff
# ****************************************************************************
lullOffsetX = 180
lullSpacerX = 75
lullY = 130+75+7*50
labelUserLegLength.place(x=10, y=lullY)
listboxUserLegLength.place(x=lullOffsetX+1*lullSpacerX, y=lullY)

lucqOffsetX = 180
lucqSpacerX = 75
lucqY = 130+75+8*50
labelUserComputedQuantity.place(x=10, y=lucqY)
listboxUserComputedQuantity.place(x=lucqOffsetX+1*lucqSpacerX, y=lucqY)

luttOffsetX = 180
luttSpacerX = 75
luttY = 130+75+9*50
labelUserThresholdType.place(x=10, y=luttY)
listboxUserThresholdType.place(x=luttOffsetX+1*luttSpacerX, y=luttY)

# Buttons
# ****************************************************************************
buttonLookUp.place(x=660, y=lullY)
bottomButtonsY = 130+75+10*50
buttonHelp.place(x=10, y=bottomButtonsY)
buttonCalculate.place(x=660, y=bottomButtonsY)

# Console window
# ****************************************************************************
consoleWindowY = 130+75+12*50
textboxConsoleWindow.place(x=10, y=consoleWindowY)


tkinter.mainloop()

