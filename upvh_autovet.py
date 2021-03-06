
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

#A check to make sure we're within the time window of aLIGO, and that end_time is after start_time
if args.gps_start_time < 971574400: #roughly the end of S6
    parser.error("gps_start_time before S6")
if args.gps_end_time < args.gps_start_time:
    parser.error("end_time is before gps_start_time")

pattern_trigs_UPVh = os.path.join(args.directory_path, 'DARM_LOCK_{}_{}-H', 'H1:*veto.txt')
pattern_segs_UPVh = os.path.join(args.directory_path, 'DARM_LOCK_{}_{}-H', 'segments.txt')

f = open("total_UPVh_trigs.txt", "w")
for day in range(args.gps_start_time, args.gps_end_time + 1, 86400):
	#end_day = day + 86400
	wildcard_UPVh = pattern_trigs_UPVh.format(day, day+86400)
        print wildcard_UPVh
        for filename in glob.glob(wildcard_UPVh):
        	print filename

                data = numpy.loadtxt(filename)
                #print data
                #come up with better in-for loop dummy variables
                start_time = [data[i,0] for i in range(len(data))]
                end_time = [data[i,1] for i in range(len(data))]

                #f = open("total_UPVh_trigs.txt", "a")
                for index in range(len(start_time)):
                	f.write(str(start_time[index]) + " " + str(end_time[index]) + "\n")
f = open("total_UPVh_segs.txt","w")
for day in range(args.gps_start_time, args.gps_end_time +1, 86400):
	wildcard_UPVh_segs = pattern_segs_UPVh.format(day, day + 86400)
        for filename in glob.glob(wildcard_UPVh_segs):
		if os.path.isfile(filename):
			print filename + " exists. Adding to total_UPVh_segs.txt."
			
			knownsegments = numpy.loadtxt(filename)
       	 		#knownsegments = numpy.atleast_2d(numpy.loadtxt(filename))
                	known_start = [knownsegments[i,0] for i in range(len(knownsegments))]
                	known_end = [knownsegments[i,1] for i in range(len(knownsegments))]

                #f = open("total_UPVh_segs.txt","a")
                	for index in range(len(known_start)):
                		f.write(str(known_start[index]) + " " + str(known_end[index]) + "\n")

		else:
			print filename + " does not exist. Looking for the segment file in next time increment."
			break
f.close()

#construct flag and filename
flag_name = 'H1:UPVh-RND:1' #NEEDS TO BE CHANGED
name =  'segments_UPVh_RND.xml' #NEEDS TO BE CHANGED


try: knownsegments = numpy.loadtxt('total_UPVh_segs.txt')
except:
        print 'No total_UPVh_segs.txt file in current working directory. It should have been produced from last loop.'

#knownsegments = numpy.loadtxt(total_UPVh_segs.txt'
known_start = [knownsegments[i,0] for i in range(len(knownsegments))]
known_end = [knownsegments[i,1] for i in range(len(knownsegments))]
# read the data
data = numpy.loadtxt('total_UPVh_trigs.txt', dtype=float)

# get an array for the start_time and end_time of each segment
start_time = [data[i,0] for i in range(len(data))]
end_time = [data[i,1] for i in range(len(data))]

# create a data quality flag object 
#zip will truncate the start and end time. is this OK?
flag = DataQualityFlag(flag_name, active=zip(start_time, end_time), known=zip(known_start, known_end))

# write flag
flag.write(name)
