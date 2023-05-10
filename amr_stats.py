# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 16:13:28 2017

Run the BISICLES stats module for all plot.*.hdf5 files within a directory and dump the output nicely in a csv file
Chosen directory is from the command line argument
Run as: "python stats.py [directory]"
@author: matt
"""

import os
import sys
import subprocess
import glob


if len(sys.argv) == 1:
    print('No directory specified. Select one by running the command "python stats.py [directory]"')
    sys.exit()

directory = sys.argv[1]
if not directory.endswith('/'):
    directory = directory + '/'
outfile = 'stats.csv'
filetoolsPath = '/usr/people/donnelly/bisicles/BISICLES/code/filetools/'
filetoolStats = 'stats2d.Linux.64.g++.gfortran.DEBUG.ex'

if os.path.exists(directory+outfile):
    os.remove(directory+outfile)

print("Running stats for directory: " + directory)

# Write the header
header = 'file,time,iceVolumeAll,iceVolumeAbove,groundedArea,floatingArea,totalArea,groundedPlusOpenLandArea'
writeCommand = 'echo ' + header + ' >> ' + directory + outfile
os.system(writeCommand)

count = 0
for infile in sorted(os.listdir(directory)):
    if infile.endswith(".2d.hdf5") and infile.startswith("plot.") and not infile.endswith(".flat.2d.hdf5"):
        count = count + 1
        
        #Run the filetools stats executable
        statsCommand = filetoolsPath + filetoolStats + ' ' + directory + infile + ' 918 1028 9.81 ' + ' | grep time'
        statsOutput = subprocess.check_output(statsCommand,shell=True)
        statsOutput = statsOutput.decode('utf-8')

        #These two lines are required when running on Porthos - otherwise remove them
        #statsOutput = str(statsOutput)
        #statsOutput = 'time' + statsOutput.split('time')[1].split('.\n')[0]
        
        #Clean up the output and write to the csv
        statsOutput = statsOutput.replace('=','').replace('  ',' ').replace(' ',',').split('.\n')[0]
        time = statsOutput.split('time')[1].split('iceVolumeAll')[0]
        volumeAll = statsOutput.split('iceVolumeAll,')[1].split('iceVolumeAbove')[0]
        volumeAbove = statsOutput.split('iceVolumeAbove,')[1].split('groundedArea')[0]
        groundedArea = statsOutput.split('groundedArea,')[1].split('floatingArea')[0]
        floatingArea = statsOutput.split('floatingArea,')[1].split('totalArea')[0]
        totalArea = statsOutput.split('totalArea,')[1].split('groundedPlusOpenLandArea')[0]
        groundedPlusLand = statsOutput.split('groundedPlusOpenLandArea,')[1].split(',')[0]
        statsRow = infile + time + volumeAll + volumeAbove + groundedArea + floatingArea + totalArea + groundedPlusLand
        print(statsRow)
        writeCommand = 'echo ' + statsRow + ' >> ' + directory + outfile
        os.system(writeCommand)

if count == 0:
    print("No plot.*.hdf5 files found")
    #os.remove(directory+outfile)
else:
    print(str(count) + " plot.*.hdf5 files found. Created stats file " + directory + outfile)