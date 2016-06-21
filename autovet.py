#############################
#############################
##                         ##
##      autovet.py         ##
##                         ##
##      updated:06/10/16   ##
##                         ##
#############################
#############################

#still needs to be cleaned up according to python style guide
#Need to add comments 

import argparse
import optparse
import glob
import numpy
from gwpy.segments import DataQualityFlag
import ConfigParser
import os,sys
import subprocess
from os import path

#command line parsing
parser = argparse.ArgumentParser(description='Argument Parsing')
parser.add_argument('gps_start_time',type=int,help='Please enter GPS start time')
parser.add_argument('gps_end_time',type=int,help='Please enter GPS end time')
parser.add_argument('directory_path',type=str,help='Please enter directory path for triggers and segments')
parser.add_argument('-s','--start_date', type=str, help='Please enter start date in YYYYMMDD format') 
parser.add_argument('-e','--end_date', type=str, help='Please enter end date in YYYYMMDD format')
parser.add_argument('type_dq_flag', type=str, help='Please enter either hveto, UPVh, OVL')
args = parser.parse_args()

#grabbing start/end years, months, and days and storing them in variables
#this is used in grabbing the directory structure for hveto files
start_year = int(args.start_date[:4])
end_year = int(args.end_date[:4])
start_month = int(args.start_date[4:6])
end_month = int(args.end_date[4:6])
start_day = int(args.start_date[6:8])
end_day = int(args.start_date[6:8])

#A check to make sure we're within the time window of aLIGO, and that end_time is after start_time
if args.gps_start_time < 971574400: #roughly the end of S6
    parser.error("gps_start_time before S6")
if args.gps_end_time < args.gps_start_time:
    parser.error("end_time is before gps_start_time")

###################################################
#each option (hveto, UPVh, OVL) in the elif loop will grab the triggers and segments for the associated vetoing program, over any given time period. It will then compile all of the segments into one .txt file, and all of the triggers, into one .txt file. These text files will be used to create the single DQ-flag in .xml format
###################################################

#choosing to read in hveto!
if args.type_dq_flag == 'hveto':
	print 'Data Quality Flag chosen is hveto, stored in the path ' + args.directory_path + '. (Advance to GO and collect $200.)'
	
	#open the total_hveto_trigs.txt file, and prepare to write to it!
	f = open("total_hveto_trigs.txt", "w")
	
	#create pattern paths for the trigger segment files to loop over
	#NOTE TO SELF: create option to specify which trigger files to loop over. default it to '*VETO_SEGS_ROUND*.txt', and then in the --help, specify how to put in your own list of trigger files.
	pattern_trigs_hveto = os.path.join(args.directory_path, '{}{:02}','{}{:02}{:02}', '*86400-DARM','*VETO_SEGS_ROUND*.txt')	
	pattern_segs_hveto = os.path.join(args.directory_path, '{}{:02}','{}{:02}{:02}', '*86400-DARM', 'segs.txt')

	#begin for loop that loops over the range of all days/months/years: necessary because of the hveto data file structure
	for day in range(start_day, end_day + 1):
		for month in range(start_month, end_month +1)
			for year in range(start_year, end_year +1):
				
				wildcard_trigs_hveto = pattern_trigs_hveto.format(year, month, year, month, day)
				
				#grabbing the trigger files
				for filename in glob.glob(wildcard_trigs_hveto):
					
					#loading the triggers in
					data = numpy.loadtxt(filename)

					#creating and filling arrays to store the data
					#NOTE TO SELF: if there are <2 lines of data, will get an error. Still need to test.
					start_time = [data[i,0] for i in range(len(data))]
					end_time = [data[i,1] for i in range(len(data))]

					#writing the two arrays to total_hveto_trigs.txt
					for index in range(len(start_time)):
						f.write(str(start_time[index]) + " " + str(end_time[index]) + "\n")




#choosing to read in UPVh!
elif args.type_dq_flag == 'UPVh':
	print 'Data Quality Flag chosen is ' + args.type_dq_flag +', stored in the path ' + args.directory_path + '. (Advance to GO and collect $200.)'





#whoops! you forgot to choose hveto, UPVh, or OVL! 
else:
	print 'Did not give correct dq flag. Please choose from hveto, UPVh, OVL in command line. (Go to jail. Go directly to Jail. Do not pass Go. DO NOT COLLECT $200.'
	exit()
















###################################################
'''
#construct flag and filename

flag_name = 'H1:HVT-'+ args.date +':1' #NEEDS TO BE CHANGED
name =  'segments_HVT_RND.xml' #NEEDS TO BE CHANGED

# read the data
data = numpy.loadtxt('total_hveto_segs.txt')

# get an array for the start_time and end_time of each segment
start_time = [data[i,0] for i in range(len(data))]
end_time = [data[i,1] for i in range(len(data))]

# create a data quality flag object 
#zip will truncate the start and end time. is this OK?
flag = DataQualityFlag(flag_name, active=zip(start_time, end_time), known=zip(known_start, known_end))

# write flag
flag.write(name)

config = ConfigParser.RawConfigParser()

config.add_section('plugins')
config.set('plugins','gwvet.tabs', ' ')

config.add_section('states')
config.set('states', 'Science', '%(ifo)s:DMT-ANALYSIS_READY:1')

config.add_section('segment-database')
config.set('segment-database','url','https://segments.ligo.org')

config.add_section('')
config.set('','type','veto-flag')
config.set('','event-channel','%(ifo)s:GDS-CALIB_STRAIN')
config.set('','event-generator','Omicron')
config.set('','metrics',"'Deadtime',\n'Efficiency', \n'Efficiency/Deadtime', \n'Efficiency | SNR>=8', \n'Efficiency/Deadtime | SNR>=8', \n'Efficiency | SNR>=20', \n'Efficiency/Deadtime | SNR>=20', \n'Efficiency | SNR>=100', \n'Efficiency/Deadtime | SNR>=100',\n'Use percentage', \n'Loudest event by SNR'")

config.add_section('tab-SNR-5.5')
config.set('tab-SNR-5.5', 'name','SNR 5.5')
config.set('tab-SNR-5.5', 'type', 'veto-flag')
config.set('tab-SNR-5.5', 'shortname', 'SNR 5.5')
config.set('tab-SNR-5.5', 'flags', 'H1:HVT-'+ args.date +':1')
config.set('tab-SNR-5.5', 'states', "Science")
config.set('tab-SNR-5.5', 'segmentfile', 'segments_HVT_RND.xml')

with open('hveto_segs.ini','wb') as configfile:
	config.write(configfile)
'''
