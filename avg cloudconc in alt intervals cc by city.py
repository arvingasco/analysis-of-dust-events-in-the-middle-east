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
import math

#path directory
path = r"C:\Users\alain\Documents\University files\4th year\Dust Masters Project\Data sets\\" 
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
#----------------------------------------------------------------------------------------
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

#finds the list of files in the path
filelist = os.listdir(path)

#counter for kth .txt files
k = 0
for i in filelist:
    #only opens the .txt files
    if i.endswith('.txt'):
        with open(path + i, 'r') as f:
            #reads the line
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
                for i in range(68, len(lines)):
                    #relevant measurements
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
                for i in range(76, len(lines)):
                    #relevant measurements
                    UTCsec[k].append(int(lines[i].split(' ')[0]))
                    long[k].append(float(lines[i].split(' ')[1]))
                    lat[k].append(float(lines[i].split(' ')[2]))
                    alt[k].append(float(lines[i].split(' ')[3]))
                    cloudconc[k].append(float(lines[i].split(' ')[28]))
                    cloudconcerr[k].append(float(lines[i].split(' ')[29]))               
        k += 1     
#----------------------------------------------------------------------------------------------------
"""
Calculations with the data
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

#rounds up the maximum altitude to the nearest 100
maxalt = math.ceil(max(max(alt))/ 100) * 100

#finds the unique cities
cities = np.unique(city)

#declare average cloud concentration arrays
avg_cloud = [[[] for y in range(0, maxalt, 100)] for x in range(0,len(cities))]

#declare altitude intervals        
alt_int = []
actavg_cloud = [[] for y in range(0,len(cities))]
actavg_clouderr = [[] for y in range(0,len(cities))]     
altaxis = []

#appends all particle concentration in an altitude interval into one array, based on cities
for a in range(0, num_files()):  
    for b in range(0, len(alt[a])):
        for i in range(0, len(cities)):
            x = 0
            if str(city[a]) == str(cities[i]):
                for c in range(0, maxalt, 100):
                    if c < alt[a][b] <= c + 100:
                        avg_cloud[i][x].append(cloudconc[a][b])
                    else:
                        pass
                    x += 1
            else:
                pass
            
#finds the average concentration of each altitude interval
for i in range(0,len(cities)):
    for d in range(0, maxalt, 100):
        
        z = int(d/100)
        #mean average
        try:
            avg = sum(avg_cloud[i][z])/len(avg_cloud[i][z])
        except:
            avg = 0
        #standard deviation
        std = np.std(avg_cloud[i][z])
        #append data to array
        actavg_clouderr[i].append(std)
        actavg_cloud[i].append(avg)
        
        if i == 1:
            alt_int.append(str(d) + '-' + str(d + 100))
            altaxis.append(d)  
#-------------------------------------------------------------------------------------------------------
"""
Plotting the data
"""
#setting y ticks to every 500m 
ypos = []
ylabels = []

for a in range(0, z):
    if a % 5 == 0:
        ypos.append(altaxis[a])
        ylabels.append(alt_int[a])
  
#setting the minimum and maximum for the axes
xmax = max(max(actavg_cloud)) 
xmin = 1.5*(10**(-5))
ymin = 0
ymax = max(max(alt))
axes = plt.gca()
axes.set_xlim([xmin, xmax])
axes.set_ylim([ymin,ymax])
#logs the graph
axes.set_xscale('log')

a1 = mptch.Patch(color = 'blue', label = str(cities[0]))
a2 = mptch.Patch(color = 'red', label = str(cities[1]))
a3 = mptch.Patch(color = 'green', label = str(cities[2]))
a4 = mptch.Patch(color = 'black', label = str(cities[3]))
a5 = mptch.Patch(color = 'purple', label = str(cities[4]))
a6 = mptch.Patch(color = 'lime', label = str(cities[5]))
a7 = mptch.Patch(color = 'orange', label = str(cities[6]))
plt.legend(handles = [a1, a2, a3, a4, a5, a6, a7], loc = 'upper left', bbox_to_anchor = (1, 1), fancybox = True)

#data point coloura
colour = []
colour.append('blue')
colour.append('red')
colour.append('green')
colour.append('black')
colour.append('purple')
colour.append('lime')
colour.append('orange')

#Plotting cloud concetration against altitude         
plt.xlabel('Average Concentration of Cloud Particles in Interval/ number cm\u207B\u00b3')
plt.ylabel('Altitude Interval/ m')
plt.title('Altitude against Cloud Particle Concentration for ' + str(num_files()) + ' ascents/ descents')     
plt.yticks(ypos, ylabels)

for i in range(0, len(cities)):
    plt.scatter(actavg_cloud[i], altaxis, s = 60, c = colour[i], edgecolors = 'black')
plt.grid()
plt.show()
#----------------------------------------------------------------------------------------------------------------