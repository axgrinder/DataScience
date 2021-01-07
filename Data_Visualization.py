# -*- coding: utf-8 -*-
# **************************************************************************************************************************
# *File: Data_Visualization C:\Users\mb89539\.spyder-py3
# *
# *Copyright: 2020 Michael Bourg michaelbourg72@gmail.com
# *All rights reserved
# *
# *The information in this file is meant to be used to analyze the data output by a Data Acquisition unit 
# *(DAQ). The copying and/or distribution of this file without the written consent of the author 
# *is strictly prohibited.
# *
# *Author: Michael Bourg
# *Date: Last Edited April 2020
# *
# *Description:    A Python script that asks the user to provide a data file and stores that file in the variable
# *                "data".
# *                Then, data is parsed of the unwanted header rows and unused columns. The user will then be asked to input
# *                number of sensors and and to name the columns, the new file is saved in the users folder of choice. The
# *                user is also asked if any of the columns require calculation, if so, a multiplier is entered.
# *                Then, the user is asked if they would like to create plots. If so, the user is asked to select a type of
# *                plot (high temp, current, etc.). The program will then prompt the user to provide the number of series
# *                in the plot and then to enter the column names to be plotted together (same figure). The plots are
# *                created, displayed, and saved in the folder of the users choice. 
# *                sensors (temperature (thermocouples), or voltage (sensing)). Then asks the user if a mutliplier is 
# *                required to perform calculations such as:
# *                    - Votage to current (Ohm's Law)
# *                        -I=V/R, where I = current, V = voltage, R = known shunt resistance                  
# *                    - Voltage to pressure (device dependent)
# *                        - Transducers typically require calculation to convert the voltage signal to psi or other unit of
# *                          pressure.
# *                    - Temperature
# *                        - Depending on device, the voltage typically requires no additional calculation.
# *                
# *                Once the data has been retrieved and the number of sensors and type has been selected, the user is then
# *                asked what graphs are required. the user then selects whether the graphs are single series sets or a 
# *                combination of series in a data set. The selection of the first graph creates a file in a predetermined 
# *                directory, then each subsequent graph will be stored in the same file folder With the tilte of the data
# *                set.
# *
# **************************************************************************************************************************

###Import required packages
import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

### Functions
    
def pickDAQ():
    """    
    **********************************************************************************************************************
    *Function: pickDAQ()
    *Decription: 
        *    This function lets the user select the DAQ from which the data comes
                -0 : TO QUIT
                 1 : Agilent 34972A "RawData"
                 2 : Agilent 34972A "Processed""
                 3 : HBM MX403B "Raw Data"            (to be implemented in future revision)
                 4 : HBM MX840B "Processes"
                 5 : SMUToolBox          (to be implemented in future revision)
                 6 : BMMToolBox          (to be implemented in future revision)
        *    The function prints the DAQ list (above) to the screen and prompts the user for a selection. 
        
        *Parameters:
            *    User input for DAQ selection
            
            *Return
            *    Variable "DAQ" to be used to call the appropriate functions
    **********************************************************************************************************************
    """
    
    daq_list = {
    0: {'name': "TO QUIT"},
    1: {'name': 'Agilent 34972A "Raw Data"'},
    2: {'name': 'Agilent 34972A "Processed"'},
    3: {'name': 'HBM MX403B "Raw Data"'},
    4: {'name': 'HBM MX403B "Processed"'}
    }
    print("Data Acquisition Units:")
    
    for x, y in daq_list.items():
        print(x, ':', daq_list[x]['name'])
 
    while x != 0:
        print("\nSelect a data acquisition unit: ")
        x = int(input())
 
        if x in daq_list.keys():
            x = int(x)
            print("\nYou have chosen {0}".format(daq_list[x]['name']))
            if x == 1 or 2:
                return x
            
        elif x == 0:
            quit()
            
        else:
            print("Your choice is not available.")

def getARawData():
    """    
    **********************************************************************************************************************
    *Function: getARawData()
    *Decription: 
        *    This function gets the raw data set from the user and asks:
                -For Agilent 34972A raw data sets
                    -The number of sensors
                    -If multiplier is needed (to provide data corrections andimprove analysis)(to be implemented in future
                    updates)
        *    The function performs a visual inspection of the data through the head(), tail(), info(), len(), size 
             functions or attributes to provide verification of correct files
             
        *Parameters:
            *    User input for number of sensors
            *    User input for file name
            *    User input for multiplier (for data correction and analysis)
            
            *Return
            *    Variable in which data is stored and passed for global usage
    **********************************************************************************************************************
    """
    
    numSense = int(input('Please enter number of sensors used: '))
    
    data = input("Please enter the location of the raw data: ")
    data = pd.DataFrame(pd.read_csv(data, dialect = csv.excel, skiprows = (numSense + 8),encoding ='UTF-16'))
    
    data = data.set_index('Scan')
    #drop alarm columns out of the dataframe
        #can be disabled if alarms are in use
    for i in range (2, numSense+2):
        data.drop(data.columns[[i]], axis = 1, inplace = True)
    #split the 'Time' column
    data[['Time','HMS']] = data['Time'].str.split(' ',expand=True)
    #drop "Time" column
    data.drop('Time', axis = 1, inplace = True)
    data[['HMS', 'min', 'sec', 'msec']] = data['HMS'].str.split(':',expand=True)
    data.rename(columns = {'HMS':'Hour'}, inplace = True)
    data['temp'] = data['Hour'].str.cat(data['min'],sep=" ")
    data['HMS'] = data['temp'].str.cat(data['sec'],sep=" ")
    data = data.set_index('HMS')
    
        
    data = nameCols(data)
    
    fileName = input('Save file as? ')
    data.to_csv('C:/Users/mb89539/Desktop/Data_Analysis_workbook/create_csvs/' + fileName + '.csv')
    
    return(data)

def getHBMRawData():
    """    
    **********************************************************************************************************************
    *Function: getHBMRawData()
    *Decription: 
        *    This function gets the raw data set from the user and asks:
                -For Agilent 34972A raw data sets
                    -The number of sensors
                    -If multiplier is needed (to provide data corrections andimprove analysis)(to be implemented in future
                    updates)
        *    The function performs a visual inspection of the data through the head(), tail(), info(), len(), size 
             functions or attributes to provide verification of correct files
             
        *Parameters:
            *    User input for number of sensors
            *    User input for file name
            *    User input for multiplier (for data correction and analysis)
            
            *Return
            *    Variable in which data is stored and passed for global usage
    **********************************************************************************************************************
    """
    
    #numSense = int(input('Please enter number of sensors used: '))
    
    data = input("Please enter the location of the raw data: ")
    data = pd.read_csv(data, sep = '\s+', skiprows = 38)
    #data.set_index('Time', inplace = True)
    data.dropna(axis = 1, inplace = True)
    data.head()
        
    data = nameCols(data)
    
    fileName = input('Save file as? ')
    data.to_csv('C:/Users/mb89539/Desktop/Data_Analysis_workbook/create_csvs/' + fileName + '.csv')
    
    return(data)

def nameCols(data):
    """    
    **********************************************************************************************************************
    *Function: nameCols()
    *Decription: 
        *    This function lets the user name the colums in order.
            *    Future revision will replace with text boxes in a GUI dialog box
            
        *Parameters:
            *    User input for column names
            
            *Return
            *    DataFrame named data with user named columns
    **********************************************************************************************************************
    """
    
    colNames = []
    if DAQ == 1:
        for i in range(0, len(data.columns)-1):
            print("Please enter sensor ", i+1, "name: ")
            item = input()
            colNames.append(item)
            
        data.columns = colNames
        
    if DAQ == 2:
        defaultColNames = ['Scan']
        for i in range(1, len(data.columns)):
            print("Please enter sensor ", i, "name: ")
            item = input()
            colNames.append(item)
            
        colNames = defaultColNames + colNames
        data.columns = colNames
        data.set_index(defaultColNames, inplace = True)
        
    if DAQ == 3:
        defaultColNames = ['Time']
        for i in range(1, len(data.columns)):
            print("Please enter sensor ", i, "name: ")
            item = input()
            colNames.append(item)
            
        colNames = defaultColNames + colNames
        data.columns = colNames
        data.set_index(defaultColNames, inplace = True)
    
    # for i in range(1, len(data.columns)):
    #     print("Please enter sensor ", i, "name: ")
    #     item = input()
    #     colNames.append(item)
        
    # colNames = defaultColNames + colNames
    # data.columns = colNames
    # data.set_index(defaultColNames, inplace = True)
        
    return(data)
    
def showInfo(data):
    """
     *********************************************************************************************************************
    *Function: showInfo()
    *Decription: 
        *    This function shows data attributes for the user to confirm that the data
             is the correct data set. It also allows the user to remove any bad
             data
        *    The function performs a visual inspection of the data through the head(), tail(), 
             info(), len(), size functions or attributes to provide verification of correct files
             
        *Parameters:
            *    The data frame created in the getXXXData() function
            
            *Return
            *    Variable in which data is stored and passed for global usage
    **********************************************************************************************************************
    """
    
    print(data.head())                          # Inspect first 5 lines of data
    #print(data.tail())                          # Inspect last 5 lines of data
    #print(data.info())                          # get information regarding data types
    #print(len(data))                            # provide to number of rows
    #print(data.size)                            # provide total number of entries in data
    
def makeGraph(data):
    """
     *********************************************************************************************************************
    *Function: makeGraph()
    *Decription: 
        *    This function allows the user to select from a list of predesigned graphs
        *    The function calls graphing functions and prompts the user to provide required information to the graph's
             design.
             
        *Parameters:
            *    The processed data frame (cleaned and named columns)
            
            *Return
            *    figures of selected series' graphs
    **********************************************************************************************************************
    """
    
    graph_list = {
    0: {'name': "TO QUIT"},
    1: {'name': 'Temperature Graph'},
    2: {'name': 'Pressure Graph'},
    3: {'name': 'Current'},
    4: {'name': 'Custom Graph'}
    }
    print("Graph List:")
    
    for x, y in graph_list.items():
        print(x, ':', graph_list[x]['name'])
 
    while x != 0:
        print("\nSelect a graph type: ")
        x = int(input())
 
        if x in graph_list.keys():
            x = int(x)
            print("\nYou have chosen {0}".format(graph_list[x]['name']))
            
            return x
        
        elif x == 0:
            quit()
            
        else:
            print("Your choice is not available.")
                
def TempGraph(data):
    """
     *********************************************************************************************************************
    *Function: TempGraph()
    *Decription: 
        *    This function sets up the figure for a temperature graph with axis titles already hard 
             coded. This is a good function for providing a quick temperature graph.
             
        *Parameters:
            *    The processed data frame created in the getXXXData() function
            
            *Return
            *    Variable in which data is stored and passed for global usage
    **********************************************************************************************************************
    """
    
    howMany = []
    n = int(input("How many series in this figure? "))
    
    for i in range(0, n):
        print("Please enter series ", i + 1, "name: ")
        item = input()
        howMany.append(item)
        
    df = pd.DataFrame(data[howMany])
    df.plot(figsize = (8, 4.5), grid = True, legend=None)
    limit = int(input("Please enter the upper limit for the 'Temperature' axis (typically 1200C): "))
    plt.ylim(0, limit)
    plt.legend(loc='best')
    title = input('Enter Graph Title: ')
    plt.title(title)
    plt.xlabel("Time (sec)")
    plt.ylabel("Temp (C)")
    
    plt.savefig('C:/Users/mb89539/Desktop/Data_Analysis_workbook/create_csvs/' + title + '.pdf')
    
def PressureGraph(data):
    """
    **********************************************************************************************************************
    *Function: PressureGraph()
    *Decription: 
        *    This function sets up the figure for a temperature graph with axis titles already hard 
             coded. This is a good function for providing a quick temperature graph.
             
        *Parameters:
            *    The processed data frame created in the getXXXData() function
            
            *Return
            *    Variable in which data is stored and passed for global usage
    **********************************************************************************************************************
    """
    
    howMany = []
    n = int(input("How many series in this figure? "))
    
    for i in range(0, n):
        print("Please enter series ", i + 1, "name: ")
        item = input()
        howMany.append(item)
        
    df = pd.DataFrame(data[howMany])
    df = df *50
    df.plot(figsize = (8, 4.5), grid = True)
    limit = int(input("Please enter the upper limit for the 'Temperature' axis (typically 60): "))
    plt.ylim(0, limit)
    plt.legend(loc='best')
    title = input('Enter Graph Title: ')
    plt.title(title)
    plt.xlabel("Time (sec)")
    plt.ylabel("Pressure (psi)")
    
    plt.savefig('C:/Users/mb89539/Desktop/Data_Analysis_workbook/create_csvs/' + title + '.pdf')
    
def CurrentGraph(data):
    """
     *********************************************************************************************************************
     *Function: PressureGraph()
    *Decription: 
        *    This function sets up the figure for a temperature graph with axis titles already hard 
             coded. This is a good function for providing a quick temperature graph.
             
        *Parameters:
            *    The processed data frame created in the getXXXData() function
            
            *Return
            *    Variable in which data is stored and passed for global usage
    **********************************************************************************************************************
    """
    howMany = []
    n = int(input("How many series in this figure? "))
    for i in range(0, n):
        print("Please enter series ", i + 1, "name: ")
        item = input()
        howMany.append(item)
        
    df = pd.DataFrame(data[howMany])
    mult = float(input('Enter known resistance: '))
    df = df / mult
    df.plot(figsize = (8, 4.5), grid = True)
    limit = int(input("Please enter the upper limit for the 'Temperature' axis (typically 60): "))
    plt.ylim(0, limit)
    plt.legend(loc='best')
    title = input('Enter Graph Title: ')
    plt.title(title)
    plt.xlabel("Time (sec)")
    plt.ylabel("Pressure (psi)")
    
    plt.savefig('C:/Users/mb89539/Desktop/Data_Analysis_workbook/create_csvs/' + title + '.pdf')
        
def CustomGraph(data):
    """
     *********************************************************************************************************************
     *Function: PressureGraph()
    *Decription: 
        *    This function sets up the figure for a temperature graph with axis titles already hard 
             coded. This is a good function for providing a quick temperature graph.
             
        *Parameters:
            *    The processed data frame created in the getXXXData() function
            
            *Return
            *    Variable in which data is stored and passed for global usage
    **********************************************************************************************************************
    """
    howMany = []
    #projName = input('Enter the plot file name: ')
    n = int(input("How many series in this figure? "))
    for i in range(0, n):
        print("Please enter series ", i + 1, "name: ")
        item = input()
        howMany.append(item)
        
    df = pd.DataFrame(data[howMany])
    doYa = input('Do you have a multiplier Y/n? ')
    if doYa == 'Y':
        mult = int(input('Enter multiplier value: '))
        df = df * mult
        
    with PdfPages('multipage_pdf.pdf') as pdf:
        plt.figure(figsize=(8, 4.5))
        df.plot(figsize = (8, 4.5), grid = True)
        plt.xticks(rotation = 45)
        plt.ylim(data.min().min(), data.max().max())
        plt.legend(loc='best')
        title = input('Enter Graph Title: ')
        plt.title(title)
        xLab = input('Enter x-axis title: ')
        plt.xlabel(xLab)
        yLab = input('Enter y-axis title: ')
        plt.ylabel(yLab)
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()
    
    # fig = plt.figure()
    
    # df.plot(figsize = (8, 4.5), grid = True)
    # uLimit = float(input("Please enter the upper limit for the y-axis: "))
    # lLimit = float(input("Please enter the lower limit for the y-axis: "))
    # plt.ylim(lLimit, uLimit)
    # plt.legend(loc='best')
    # title = input('Enter Graph Title: ')
    # plt.title(title)
    # xLab = input('Enter x-axis title: ')
    # plt.xlabel(xLab)
    # yLab = input('Enter y-axis title: ')
    # plt.ylabel(yLab)
    
    # plt.show()
    
    # #plt.savefig('C:/Users/mb89539/Desktop/Data_Analysis_workbook/create_csvs/' + title + '.pdf')
    # pp = PdfPages('C:/Users/mb89539/Desktop/Data_Analysis_workbook/SDBuldgingCell/' + projName + '.pdf')
    # pp.savefig(fig)
    # pp.close()
    
def selectGraph(graph):
    """
     *********************************************************************************************************************
    *Function: showInfo()
    *Decription: 
        *    This function shows data attributes for the user to confirm that the data
             is the correct data set. It also allows the user to remove any bad
             data
        *    The function performs a visual inspection of the data through the head(), tail(), 
             info(), len(), size functions or attributes to provide verification of correct files
             
        *Parameters:
            *    The data frame created in the getXXXData() function
            
            *Return
            *    Variable in which data is stored and passed for global usage
    **********************************************************************************************************************
    """
    while graph == 'Y':
        if graph == 'Y':
            make = makeGraph(data)
            if make == 1:
                TempGraph(data)
            elif make ==2:
                PressureGraph(data)
            elif make ==3:
                CurrentGraph(data)
            elif make == 4:
                CustomGraph(data)
        else:
            quit()
        graph = input("Would you like to make a graph, Y/n? ")
        
###Main progran starts here

DAQ = pickDAQ()
if DAQ == 1:
    data = getARawData()
    showInfo(data)
    graph = input("Would you like to make a graph, Y/n? ")
    selectGraph(graph)
    
if DAQ == 2:
    data = input("Please enter your file name: ")
    data = pd.DataFrame(pd.read_csv(data, dialect = csv.excel))
    showInfo(data)
    graph = input("Would you like to make a graph, Y/n? ")
    selectGraph(graph)
    
if DAQ == 3:
    data = getHBMRawData()
    showInfo(data)
    graph = input("Would you like to make a graph, Y/n? ")
    selectGraph(graph)

    
# if DAQ == 4:
#    # data = getProcData()
#     #showInfo()
#     graph = input("Would you like to make a graph, Y/n?")
    
# if DAQ == 5:
#     # data = getProcData()
#     # showInfo()
#     graph = input("Would you like to make a graph, Y/n?")
    
# if DAQ == 6:
#     # data = getProcData()
#     # showInfo()
#     graph = input("Would you like to make a graph, Y/n?")