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


f = open("total_hveto_trigs.txt", "w")
#Option to get hveto triggers and segments
#elif args.type_dq_flag == 'hveto':
pattern_trigs_hveto = os.path.join(args.directory_path, '{}{:02}','{}{:02}{:02}', '*86400-DARM','*VETO_SEGS_ROUND*.txt')
print pattern_trigs_hveto
pattern_segs_hveto = os.path.join(args.directory_path, '{}{:02}','{}{:02}{:02}', '*86400-DARM', 'segs.txt')
for day in range(start_day, end_day + 1):
        for month in range(start_month, end_month +1):
                for year in range(start_year, end_year +1):
                        wildcard_hveto = pattern_trigs_hveto.format(year, month, year, month, day)
                        for filename in glob.glob(wildcard_hveto):
                                print filename

                                data = numpy.loadtxt(filename)
                                print data

                                #If there is less than 2 lines of data, will get error
                                start_time = [data[i,0] for i in range(len(data))]
                                end_time = [data[i,1] for i in range(len(data))]

                                for index in range(len(start_time)):
                                        f.write(str(start_time[index]) + " " + str(end_time[index]) + "\n")

f = open("total_hveto_segs.txt","w")
for day in range(start_day, end_day + 1):
        for month in range(start_month, end_month +1):
                for year in range(start_year, end_year +1):
        #standardize naming for wildcards
                        wildcard_segs = pattern_segs_hveto.format(year, month,year, month, day)
                        print wildcard_segs
                        for filename in glob.glob(wildcard_segs):
                                knownsegments =numpy.atleast_2d(numpy.loadtxt(filename, delimiter =','))
                                print knownsegments
                                known_start = [knownsegments[i,0] for i in range(len(knownsegments))]
                                known_end = [knownsegments[i,1] for i in range(len(knownsegments))]
                #un-hardcode this name 
                                for index in range(len(known_start)):
                                        f.write(str(known_start[index]) + " " + str(known_end[index]) + "\n")

