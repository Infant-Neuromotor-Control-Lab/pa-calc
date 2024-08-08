# -*- coding: utf-8 -*-
"""
Created on Sat May 11 15:58:52 2024

@author: mghazi
"""

# textLookUp = "Note that these are median rump-sole lengths and are therefore overestimates." + " For a more accurate estimate, multiply by 0.87. These data are for typically developing infants. \nage (mo), length (cm) \n0-2, 23.3, \n3-5, 26.5, \n6-8, 29.4, \n9-11, 33.3, \n12-15, 35.0, \n16-19, 37.4, \n20-23, 39.5"

# without scale factor
# "\nage (mo), length (cm) " +\
# "\n0-2, 23.3, " +\
# "\n3-5, 26.5, " +\
# "\n6-8, 29.4, " +\
# "\n9-11, 33.3, " +\
# "\n12-15, 35.0, " +\
# "\n16-19, 37.4, " +\
# "\n20-23, 39.5"

textLookUp = "Note that these are median rump-sole lengths scaled by a " +\
    "factor of 0.87. These data are for typically developing infants. " +\
    "\nage (mo),\tlength (cm) " +\
    "\n0-2,\t\t20.3, " +\
    "\n3-5,\t\t23.1, " +\
    "\n6-8,\t\t25.6, " +\
    "\n9-11,\t\t29.0, " +\
    "\n12-15,\t\t30.5, " +\
    "\n16-19,\t\t32.5, " +\
    "\n20-23,\t\t34.4"


textHelp = "1. Click \"Load\" to select file to process. The start and end date/time of the file will be displayed. " +\
    "\n\n2. Enter the start and end date/time range that you want to process. " +\
    "\n\n3. Enter the leg length of the infant. Look it up for an approximation if you don't have the leg length but if you know the approximate age. " +\
    "\n\n4. Enter the computed quantity and threshold type for your analysis. " +\
    "\n\n5. Click \"Calculate\" and keep an eye on the console window for any potential issues."

textTest = "Sample text"

printBufferStr = "********************\nMIGHTY TOT OUTPUT LOG\n********************"