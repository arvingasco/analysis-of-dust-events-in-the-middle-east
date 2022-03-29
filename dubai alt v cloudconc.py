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

#finds the list of files in the path
filelist = os.listdir(path)

CITY = 'Dubai'

#counter for kth .txt files
k = 0
for i in filelist:
    #only opens the .txt files
    if i.endswith('.txt'):
        with open(path + i, 'r') as f:
            #reads the lines
            lines = f.readlines()
            
            #files with no extra H2O and CO2 lines
            try:
                #this is first to trigger index error in case of extra H2O and CO2 files
                #airport city 
                cty = lines[57].split(', ')[1]
                #only doha flights
                if cty == CITY:
                   city.append(cty) 
                   country.append(lines[57].split(', ')[2].rstrip('\n'))
                   
                   #tail number
                   tailnum.append(lines[3].split(', ')[3])
                   
                   #date of flight
                   year.append(lines[6].split(' ')[0])
                   month.append(lines[6].split(' ')[1])
                   day.append(lines[6].split(' ')[2])
                   
                   #ascent or descent profile
                   profile.append(lines[46].split(' ')[1].rstrip('_profile\n'))
                
                   #relevant measurements
                   for i in range(68, len(lines)):
                       #relevant measurements
                       UTCsec[k].append(int(lines[i].split(' ')[0]))
                       long[k].append(float(lines[i].split(' ')[1]))
                       lat[k].append(float(lines[i].split(' ')[2]))
                       alt[k].append(float(lines[i].split(' ')[3]))
                       cloudconc[k].append(float(lines[i].split(' ')[28]))
                       cloudconcerr[k].append(float(lines[i].split(' ')[29]))        
                   k += 1
            #files with extra H2O and CO2 lines
            except:
                #airport city and country
                cty = lines[65].split(', ')[1]
                #only doha flights
                if cty == CITY:
                    country.append(lines[65].split(', ')[2].rstrip('\n'))
                    #profile
                    profile.append(lines[54].split(' ')[1].rstrip('_profile\n'))
              
                    #tail number
                    tailnum.append(lines[3].split(', ')[3])
                   
                    #date of flight
                    year.append(lines[6].split(' ')[0])
                    month.append(lines[6].split(' ')[1])
                    day.append(lines[6].split(' ')[2])
                   
                    #relevant measurements
                    for i in range(76, len(lines)):
                        #relevant measurements
                        UTCsec[k].append(int(lines[i].split(' ')[0]))
                        long[k].append(float(lines[i].split(' ')[1]))
                        lat[k].append(float(lines[i].split(' ')[2]))
                        alt[k].append(float(lines[i].split(' ')[3]))
                        cloudconc[k].append(float(lines[i].split(' ')[28]))
                        cloudconcerr[k].append(float(lines[i].split(' ')[29]))           
                    k += 1
        #close the file
        f.close()
        
#number of doha files
numfile = k
#----------------------------------------------------------------------------------------------------
"""
Plotting the data points
"""
#removes empty lists
UTCsec2 = [x for x in UTCsec if x != []]
long2 = [x for x in long if x != []]
lat2 = [x for x in lat if x != []]
alt2 = [x for x in alt if x != []]
cloud = [x for x in cloudconc if x != []]
clouderr = [x for x in cloudconcerr if x != []]

#when the value is -9999 it screws up the graph
#the instrument is turned off, so converting the number to 0
for p in range(0,numfile):
    for s in range(0,len(cloud[p])):
        if cloud[p][s] == -9999:
            cloud[p][s] = 0
    for s in range(0,len(clouderr[p])):
        if clouderr[p][s] == -9999:
            clouderr[p][s] = 0
    for s in range(0,len(alt[p])):
        if alt[p][s] == -9999:
            alt[p][s] = 0

#rounds up the maximum altitude to the nearest 100
maxalt = math.ceil(max(max(alt2))/ 100) * 100

#declare average cloud concentration arrays
avg_cloud = [[[] for y in range(0, maxalt, 100)] for x in range(0,2)]
#declare altitude intervals        
alt_int = []
actavg_cloud = [[] for y in range(0,2)]
actavg_clouderr = [[] for y in range(0,2)]     
altaxis = []

#seasons array for if statement check
seasons = []
summer = [3, 4, 5, 6, 7, 8]
seasons.append(summer)
winter = [9, 10, 11, 12, 1, 2]
seasons.append(winter)

#appends all particle concentration in an altitude interval into one array
for a in range(0, numfile):  
    for b in range(0, len(alt2[a])):
        for i in range(0, 1):
            x = 0
            if int(month[a]) in seasons[i]:
                for c in range(0, maxalt, 100):
                    if c < alt2[a][b] <= c + 100:
                        avg_cloud[i][x].append(cloud[a][b])
                    else:
                        pass
                    x += 1
            else:
                pass

#finds the average concentration of each altitude interval
for i in range(0,1):
    for d in range(0, maxalt, 100):
        #mean average
        z = int(d/100)
        try:
            avg = sum(avg_cloud[i][z])/len(avg_cloud[i][z])
        except:
            avg = 0
        #standard deviation
        std = np.std(avg_cloud[i][z])
        #append data to array
        actavg_clouderr[i].append(std)
        actavg_cloud[i].append(avg)
        
        if i == 0:
            alt_int.append(str(d) + '-' + str(d + 100))
            altaxis.append(d)  

#setting y ticks to every 500m 
ypos = []
ylabels = []
for a in range(0, z):
    if a % 5 == 0:
        ypos.append(altaxis[a])
        ylabels.append(alt_int[a])
        
#colour code by seasons
summer = mptch.Patch(color = 'red', label = 'Summer') 
winter = mptch.Patch(color = 'blue', label = 'Winter')
plt.legend(handles = [summer, winter], loc = 'upper left', bbox_to_anchor = (1, 1), fancybox = True)    

colour = []
colour.append('red')
colour.append('blue')

#setting the minimum and maximum for the axes
xmax = max(max(actavg_cloud)) 
xmin = (10**-5)
ymin = 0
ymax = max(max(alt))
axes = plt.gca()
axes.set_xlim([xmin, xmax])
axes.set_ylim([ymin,ymax])
#axes.set_xscale('log')
            
#Plotting cloud concetration against altitude         
plt.xlabel('Average Concentration of Cloud Particles in Interval/ number cm\u207B\u00b3')
plt.ylabel('Altitude Interval/ m')
plt.title(f'Altitude against Cloud Particle Concentration for {numfile} ascents/ descents through dust events in {city[0]}')     
plt.yticks(ypos, ylabels)

#plots graph
for i in range(0,1):
    plt.plot(actavg_cloud[i], altaxis, c = colour[i])
plt.grid()
plt.show()
#----------------------------------------------------------------------------------------------------------------