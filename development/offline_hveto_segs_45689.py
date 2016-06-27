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
parser = argparse.ArgumentParser(
	description='autovet.py is a program that grabs triggers and segments for hveto, UPVh, and OVL for any time period, and concatenates them into one segment file, and one trigger file.It then creates a DQ Flag for the given type and time period, spits out a .xml file, and generates the .ini file needed to run VET. For questions or concerns, contact Erika Cowan at erika.cowan@ligo.org')
parser.add_argument('gps_start_time',type=int,help='Please enter GPS start time')
parser.add_argument('gps_end_time',type=int,help='Please enter GPS end time')
parser.add_argument('directory_path',type=str,help='Please enter directory path for triggers and segments')
parser.add_argument('-s','--start_date', type=str, help='Please enter start date in YYYYMMDD format, required for the hveto option') 
parser.add_argument('-e','--end_date', type=str, help='Please enter end date in YYYYMMDD format, required for the hveto option')
parser.add_argument('type_dq_flag', type=str, help='Please enter either hveto, UPVh, OVL')
parser.add_argument('-h', 'hveto_analysis_seg', type=int, help='Please enter offline hveto O1 offline analysis segment, 4,5,6,8,9')
args = parser.parse_args()

#A check to make sure we're within the time window of aLIGO, and that end_time is after start_time
if args.gps_start_time < 971574400: #roughly the end of S6
    parser.error("gps_start_time before S6")
if args.gps_end_time < args.gps_start_time:
    parser.error("end_time is before gps_start_time")

###choosing to read in hveto!###
if args.type_dq_flag == 'hveto':
	print 'Data Quality Flag chosen is hveto, stored in the path ' + args.directory_path + '. (Take a Walk on the Board Walk. Advance Token to Board Walk.'

	#grabbing start/end years, months, and days and storing them in variables
	start_year = int(args.start_date[:4])
	end_year = int(args.end_date[:4])
	start_month = int(args.start_date[4:6])
	end_month = int(args.end_date[4:6])
	start_day = int(args.start_date[6:8])
	end_day = int(args.end_date[6:8])	

	#TRIGGER HANDLING: begin for loop that loops over the range of all days/months/years
	f = open("total_hveto_trigs.txt", "w") #file that will hold collection of all triggers
	
	#create pattern paths for the trigger segment files to loop over
	#NOTE TO SELF: create option to specify which trigger files to loop over. default it to '*VETO_SEGS_ROUND*.txt', and then in the --help, specify how to put in your own list of trigger files.
	pattern_trigs_hveto = os.path.join(args.directory_path, '{}{:02}','{}{:02}{:02}', '*86400-DARM','*VETO_SEGS_ROUND*.txt')	

	for day in range(start_day, end_day + 1):
		for month in range(start_month, end_month +1):
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




	#SEGMENT HANDLING: begin for loop that loops over the range of all days/months/years

	f = open("total_hveto_segs.txt","w") #file that will hold collection of all segments
	pattern_segs_hveto = os.path.join(args.directory_path, '{}{:02}','{}{:02}{:02}', '*86400-DARM', 'segs.txt')
		
	for day in range(start_day, end_day + 1):
		for month in range(start_month, end_month +1):
			for year in range(start_year, end_year +1):
			
				wildcard_segs_hveto = pattern_segs_hveto.format(year, month,year, month, day)
			
				#grabbing segment files
				for filename in glob.glob(wildcard_segs_hveto):
					if os.path.isfile(filename):
						print filename + " exists. Adding to total_hveto_segs.txt."

						#loading segments in
						knownsegments =numpy.atleast_2d(numpy.loadtxt(filename, delimiter =','))		

						#storing the segments in these two arrays
						known_start = [knownsegments[i,0] for i in range(len(knownsegments))]
                                		known_end = [knownsegments[i,1] for i in range(len(knownsegments))]

						#writing the two arrays to total_hveto_segs.txt
						for index in range(len(known_start)):
							f.write(str(known_start[index]) + " " + str(known_end[index]) + "\n")
					else:
						print filename + " does not exist. Looking for the segment file in next time increment."
						break
	f.close()

###whoops! you forgot to choose hveto, UPVh, or OVL!###
else:
	print 'Did not give correct dq flag. Please choose from hveto, UPVh, OVL in command line. (Go to jail. Go directly to Jail. Do not pass Go. DO NOT COLLECT $200.'
	exit()
