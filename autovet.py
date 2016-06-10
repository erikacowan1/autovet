#############################
#############################
##                         ##
##      autovet.py         ##
##                         ##
##      Erika Cowan        ##
##      Steven Forsyth     ##
##                         ##
##      updated:04/11/16   ##
##                         ##
#############################
#############################

#version of autovet that reads and compiles segments from a specific time period, not reading in channels, as well as creating a new hveto_segs.ini file 
#still needs to be cleaned up according to python style guide

import argparse
import glob
import numpy
from gwpy.segments import DataQualityFlag
import ConfigParser
import os,sys


#command line parsing
parser = argparse.ArgumentParser(description='Argument Parsing')
parser.add_argument('start_time',type=int,help='Please enter start_time in UTC')
parser.add_argument('end_time',type=int,help='Please enter end_time in UTC')
parser.add_argument('directory_path',type=str,help='Please enter directory path for stored txt/xml files')
parser.add_argument('date',type=str, help='Please enter correct date for xml path number')
parser.add_argument('start_day', type=int, help='Please enter start day in format DD')
parser.add_argument('end_day', type=int, help='Please enter end day in format DD')
parser.add_argument('start_month', type=int, help='Please enter start month in format MM')
parser.add_argument('end_month', type=int, help='Please enter end month in format MM')
parser.add_argument('year', type=int, help='Please enter year in format YYYY')

args = parser.parse_args()

#A check to make sure we're within the time window of aLIGO, and that end_time is after start_time
if args.start_time < 971574400: #roughly the end of S6
    parser.error("start_time before S6")
if args.end_time < args.start_time:
    parser.error("end_time is before start_time")

#Path for location of the hveto triggers. Eventually expand to hveto_directory_path, ovl_dir_path, upv_dir_path    
print args.directory_path

pattern_hveto = os.path.join(args.directory_path, '{}{:02}','{}{:02}{:02}', '*86400-DARM','*VETO_SEGS_ROUND*.txt')
pattern_segs = pattern = os.path.join(args.directory_path, '{}{:02}','{}{:02}{:02}', '*86400-DARM', 'segs.txt')

for day in range(args.start_day, args.end_day + 1):
    for month in range(args.start_month, args.end_month +1):
        wildcard_hveto = pattern_hveto.format(args.year, month,args.year, month, day)
        for filename in glob.glob(wildcard_hveto):
            print filename
            
            #for file in filename:
            data = numpy.loadtxt(filename)
            print data    
            
            #If there is less than 2 lines of data, will get error
            start_time = [data[i,0] for i in range(len(data))]
            end_time = [data[i,1] for i in range(len(data))]
                
            f = open("total_hveto_segs.txt", "a")
            for index in range(len(start_time)):
                    f.write(str(start_time[index]) + " " + str(end_time[index]) + "\n")



for day in range(args.start_day, args.end_day + 1):
    for month in range(args.start_month, args.end_month +1):	
	# define known start and end times
	wildcard_segs = pattern_segs.format(args.year, month,args.year, month, day)
	for filename in glob.glob(wildcard_segs):
		knownsegments =numpy.atleast_2d(numpy.loadtxt(filename, delimiter =','))
		known_start = [knownsegments[i,0] for i in range(len(knownsegments))]
		known_end = [knownsegments[i,1] for i in range(len(knownsegments))]
		
		f = open("total_segs.txt","a")
		for index in range(len(known_start)):
			f.write(str(known_start[index]) + " " + str(known_end[index]) + "\n")

# define known start and end times
try: knownsegments =numpy.atleast_2d(numpy.loadtxt('total_segs.txt'))
except:
        print 'No total_segs.txt file in current working directory. It should have been produced from last loop.' 
known_start = [knownsegments[i,0] for i in range(len(knownsegments))]
known_end = [knownsegments[i,1] for i in range(len(knownsegments))]


#os.system("mkdir %s_xml" % args.date)

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
'''
# get all veto-seg-round txt files in the current directory
files = glob.glob(args.directory_path + '*VETO_SEGS_ROUND*.txt')
if not files:
        print 'No veto_segs_round.txt files in %s' % date

for file in files:
	# read the data
        data = numpy.loadtxt(file)
	

        # get an array for the start_time and end_time of each segment
        start_time = [data[i,0] for i in range(len(data))]
        end_time = [data[i,1] for i in range(len(data))]
	#data is not truncated in array.
	#it is truncated somewhere in printing to file. FIXME!

	#print start and stop times for all round winners to file
	f = open("total_hveto_segs.txt", "a")
	for index in range(len(start_time)):
		f.write(str(start_time[index]) + " " + str(end_time[index]) + "\n")
'''
'''
# define known start and end times
try: knownsegments =numpy.atleast_2d(numpy.loadtxt(args.directory_path + 'segs.txt', delimiter =','))
except:
        print 'No segs.txt file in %s' % args.date
known_start = [knownsegments[i,0] for i in range(len(knownsegments))]
known_end = [knownsegments[i,1] for i in range(len(knownsegments))]

#os.system("mkdir %s_xml" % args.date)

#construct flag and filename

flag_name = 'H1:HVT-'+ args.date + ':1' #NEEDS TO BE CHANGED
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

#for time in range(args.start_time, arg.start_time, 86400): #not sure about time to increment over, for N>1 days
 '''

#creating the .ini file

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
config.set('tab-SNR-5.5', 'segmentfile', '/home/erika.cowan/public_html/vet/autovet_segs')

with open('hveto_segs.ini','wb') as configfile:
	config.write(configfile)

#code that can loop over channels, not necessary for now
'''p = 1
for i in winning_channels:
    config.add_section("tab-" + i)
    config.set("tab-" + i, 'name', "Round " + str(p)+ ":" + i)
    config.set("tab-" + i, 'shortname','Round ' + str(p))
    config.set("tab-" + i, 'flags','H1:HVT-ER7_RND' + str(p) + ':1')
    config.set("tab-" + i, 'states','Science')
    config.set("tab-" + i, 'segmentfile','segments_HVT_RND' + str(p) + '.xml' )
    p += 1
    
    with open('hveto.ini','wb') as configfile:
        config.write(configfile)     
'''
