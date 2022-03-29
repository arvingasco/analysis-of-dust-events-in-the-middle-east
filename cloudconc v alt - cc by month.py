"""
Created on Tue Oct 27 20:11:53 2020

author:Alain Gasco 10114980
Dust Masters Project
"""
#----------------------------------------------------------------------------------------------------------
"""
Importing python modules
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mptch
import numpy as np
#---------------------------------------------------------------------------------------------------------
"""
Defining functions to make code nicer
"""
#function to find the number of .txt files in the directory
def num_files():
    filelist = os.listdir(path)
    m = 0
    for i in filelist:
        if i.endswith('.txt'):
            m += 1
    return m 

#function to make colour coding neater
def colcode(dummy, col, lab):
    try:
        dummy = mptch.Patch(color = col, label = dummy[lab])
        key.append(dummy)
    except:
        pass
#----------------------------------------------------------------------------------------------------------
"""
Extracting the flight data from the profiles
"""
#declaring the arrays
#date of departure/ arrival
year = []
month = []
day = []

#aircraft tail number
tailnum = []

#airport location
city = []
country = []

#ascent or descent
profile = []

#relevant measurements
#creates number of lists equal to the number of files
UTCsec = [[] for i in range(1, num_files() + 1)]
long = [[] for i in range(1, num_files() + 1)]
lat = [[] for i in range(1, num_files() + 1)]
alt = [[] for i in range(1, num_files() + 1)]
cloudconc = [[] for i in range(1, num_files() + 1)]
cloudconcerr = [[] for i in range(1, num_files() + 1)]
h2o = [[] for i in range (1, num_files() + 1)]

#path directory
path = r"C:\Users\alain\Documents\University files\4th year\Dust Masters Project\Data sets\\" 

#finds the list of files in the path
filelist = os.listdir(path)

#counter for kth .txt files
k = 0
for i in filelist:
    #only opens the .txt files
    if i.endswith('.txt'):
        with open(path + i, 'r') as f:
            #reads the lines
            lines = f.readlines()
            
            #tail number
            tailnum.append(lines[3].split(', ')[3])
            #date of flight
            year.append(lines[6].split(' ')[0])
            month.append(lines[6].split(' ')[1])
            day.append(lines[6].split(' ')[2])
            #ascent or descent profile
            prof = lines[46].split(' ')[1].rstrip('_profile\n')
            
            #files with no extra H2O and CO2 lines
            try:
                #this is first to trigger index error in case of extra H2O and CO2 files
                #airport city and country
                city.append(lines[57].split(', ')[1])
                country.append(lines[57].split(', ')[2].rstrip('\n'))
                #now append profile
                profile.append(prof)
                n = 0
                #relevant measurements
                for i in range(68, len(lines)):
                    UTCsec[k].append(int(lines[i].split(' ')[0]))
                    long[k].append(float(lines[i].split(' ')[1]))
                    lat[k].append(float(lines[i].split(' ')[2]))
                    alt[k].append(float(lines[i].split(' ')[3]))
                    cloudconc[k].append(float(lines[i].split(' ')[28]))
                    cloudconcerr[k].append(float(lines[i].split(' ')[29]))           
            #files with extra H2O and CO2 lines
            except:
                #profile
                prof = lines[54].split(' ')[1].rstrip('_profile\n')
                profile.append(prof)
                #airport city and country
                city.append(lines[65].split(', ')[1])
                country.append(lines[65].split(', ')[2].rstrip('\n'))
                
                
                #relevant measurements
                for i in range(76, len(lines)):
                    UTCsec[k].append(int(lines[i].split(' ')[0]))
                    long[k].append(float(lines[i].split(' ')[1]))
                    lat[k].append(float(lines[i].split(' ')[2]))
                    alt[k].append(float(lines[i].split(' ')[3]))
                    cloudconc[k].append(float(lines[i].split(' ')[28]))
                    cloudconcerr[k].append(float(lines[i].split(' ')[29]))            
                    h2o[k].append(float(lines[i].split(' ')[36]))
        k += 1     
#----------------------------------------------------------------------------------------------------
"""
Plotting the data points
"""
#when the value is -9999 it screws up the graph
#the instrument is turned off, so converting the number to 0
for p in range(0,num_files()):
    for s in range(0,len(cloudconc[p])):
        if cloudconc[p][s] == -9999:
            cloudconc[p][s] = 0
    for s in range(0,len(cloudconcerr[p])):
        if cloudconcerr[p][s] == -9999:
            cloudconcerr[p][s] = 0
    for s in range(0,len(alt[p])):
        if alt[p][s] == -9999:
            alt[p][s] = 0
    for s in range(0,len(h2o[p])):
        if h2o[p][s] == -9999:
            h2o[p][s] = 0        
            
#declare colour array for colour coding
colour = [[] for i in range(1, num_files() + 1)]

#finds unique cities
cities = np.unique(city)

#colour coding by city
for i in range(0,num_files()):
    for j in range(0,len(cloudconc[i])):
        try:
            if city[i] == cities[0]:
                colour[i].append('blue')
            elif city[i] == cities[1]:
                colour[i].append('red')
            elif city[i] == cities[2]:
                colour[i].append('green')
            elif city[i] == cities[3]:
                colour[i].append('black')
            elif city[i] == cities[4]:
                colour[i].append('purple')
            elif city[i] == cities[5]:
                colour[i].append('lime')
            elif city[i] == cities[6]:
                colour[i].append('orange')
        except:
            pass
        
#array for the legend
key = []

#colours
blue = 'blue'
red = 'red'
green = 'green'
black = 'black'
purple = 'purple'
lime = 'lime'
orange = 'orange'
cyan = 'cyan'
silver = 'silver'

#Creating a legend
colcode(cities, blue, 0)
colcode(cities, red, 1)
colcode(cities, green, 2)
colcode(cities, black, 3)
colcode(cities, purple, 4)
colcode(cities, lime, 5)
colcode(cities, orange, 6)
colcode(cities, cyan,7)
colcode(cities, silver, 8)
plt.legend(handles = key, loc = 'upper left', bbox_to_anchor = (1,1), fancybox = True)

#setting the minimum and maximum for the axes
xmax = max(max(cloudconc)) 
xmin = min(min(cloudconc))
ymax = max(max(alt))
ymin = min(min(alt))
axes = plt.gca()
axes.set_xlim([xmin, xmax])
axes.set_ylim([ymin, ymax])

#Plotting cloud concetration against altitude         
plt.xlabel('Concentration of Cloud Particles/ number cm\u207B\u00b3')
plt.ylabel('Altitude/ m')
plt.title('Altitude against Cloud Particle Concentration for ' + str(num_files()) + ' ascents/ descents')     

#plots the scatter graph
for j in range(0,num_files()):
    plt.scatter(cloudconc[j], alt[j], s = 30, c = colour[j])
plt.grid()
plt.show()
#----------------------------------------------------------------------------------------------------------------