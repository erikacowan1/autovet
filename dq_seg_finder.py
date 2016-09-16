import argparse
import glob
import numpy
from gwpy.segments import DataQualityFlag
from gwpy.time import tconvert
import datetime
import os, sys
from gwpy.segments import SegmentList,Segment

#command line parsing
parser = argparse.ArgumentParser(
        description='dq_seg_finder.py is a program that grabs triggers and segments for hveto, UPVh, and OVL for any time period, and concatenates them into one segment file, and one trigger file.It then creates a DQ Flag for the given type and time period, spits out a .xml file, and generates the .ini file needed to run VET. For questions or concerns, contact Erika Cowan at erika.cowan@ligo.org')
parser.add_argument('gps_start_time',type=int,help='Please enter GPS start time')
parser.add_argument('gps_end_time',type=int,help='Please enter GPS end time')
parser.add_argument('directory_path',type=str,help='Please enter directory path for triggers and segments')
parser.add_argument('type_dq_flag', type=str, help='Please enter either hveto, UPVh, OVL')
parser.add_argument('-a', '--hveto_analysis_seg', type=str, help='Please enter offline hveto O1 offline analysis segment, 4,5,6,8,9')
parser.add_argument('-o','--online_offline', type=str, help='Please enter either offline or online. This is for hveto.')
args = parser.parse_args()

#algorithm that loads in triggers from file for any time segment
def grab_time_triggers(glob_wildcard):
    time_segs = SegmentList([])
    start_time_utc = tconvert(args.gps_start_time)
    for filename in glob.glob(glob_wildcard):
        data = SegmentList.read(filename)
        print 'grabbing trigger file:' + filename
        time_segs +=data
	#print time_segs
        start_time_utc += datetime.timedelta(days=1)
    return time_segs

def grab_time_segments(glob_wildcard):
    known_start = []
    known_end = []
    start_time_utc = tconvert(args.gps_start_time)
    for filename in glob.glob(wildcard_segs_hveto):
        if os.path.isfile(filename):
            segments =numpy.atleast_2d(numpy.loadtxt(filename, delimiter =','))
            known_start = [segments[i,0] for i in range(len(segments))]
            known_end = [segments[i,1] for i in range(len(segments))]
            start_time_utc += datetime.timedelta(days=1)

    for index in range(len(known_start)):
        g.write(str(known_start[index]) + " " + str(known_end[index]) + "\n")

#algorithm that takes segment/trigger list and writes to file
def write_segs(trig_seg_list,output_file):    
    start_end_seg = Segment(args.gps_start_time, args.gps_end_time)
    total_triggers = triggers & SegmentList([start_end_seg])

    total_triggers.coalesce()
    total_triggers.write(output_file)
        
#A check to make sure we're within the time window of aLIGO, and that end_time is after start_time
if args.gps_start_time < 971574400: #roughly the end of S6
    parser.error("gps_start_time before S6")
if args.gps_end_time < args.gps_start_time:
    parser.error("end_time is before gps_start_time")
    
#finds beginning of day for given gps time
start_of_day = tconvert(args.gps_start_time)
start_of_day = start_of_day.replace(hour=0,minute=0,second=0)
start_of_day = tconvert(start_of_day)

#finds UTC version of start/end times
start_time_utc = tconvert(args.gps_start_time)
end_time_utc = tconvert(args.gps_end_time)

###################################################
#######CREATING TOTAL TRIGGER/SEGMENT FILES########
###################################################

###choosing to read in hveto!###
if args.type_dq_flag == 'hveto':

    #opens files to be ready for writing
    f = open("total_hveto_trigs.txt", "w") #file that will hold collection of all triggers
    g = open("total_hveto_segs.txt","w") #file that will hold collection of all segments 

    print 'Data Quality Flag chosen is hveto, stored in the path ' + args.directory_path

        #choosing the offline hveto option for O1, runs by Josh Smith
    if args.online_offline == 'offline':
        analysis_segs_45689 = ['4', '5', '6', '7', '9']
        analysis_segs_237 = ['2', '3']
        if args.hveto_analysis_seg in analysis_segs_45689:
            pattern_trigs_hveto= os.path.join(args.directory_path, 'analysis' + args.hveto_analysis_seg , 'H1-omicron_BOTH-*-DARM','*VETO_SEGS_ROUND*.txt')
            pattern_segs_hveto = os.path.join(args.directory_path, 'analysis' + args.hveto_analysis_seg , 'H1-omicron_BOTH-*-DARM','segs.txt')

        elif args.hveto_analysis_seg in analysis_segs_237:
            pattern_trigs_hveto = os.path.join(args.directory_path,'H1-omicron_BOTH-*-DARM','*VETO_SEGS_ROUND*.txt')
            pattern_segs_hveto = os.path.join(args.directory_path,'H1-omicron_BOTH-*-DARM','segs.txt')

        elif args.hveto_analysis_seg == '8':
            pattern_trigs_hveto = os.path.join(args.directory_path,'*VETO_SEGS_ROUND*.txt')
            pattern_segs_hveto = os.path.join(args.directory_path,'segs.txt')
        else:
            print 'Did not choose O1 analysis segment 1,2,3,4,5,6,7,8,9. Please choose.'
            exit()
        print pattern_trigs_hveto
        print 'Data Quality Flag chosen is hveto, stored in the path ' + args.directory_path


        while start_time_utc < end_time_utc:
            day = start_time_utc.day
            month = start_time_utc.month
            year = start_time_utc.year

            triggers = grab_time_triggers(pattern_trigs_hveto)
            

            #ideally we'd be able to use the same algorithm, but the SegmentList.read doesn't support csv,
            #which is what the segment files are. So, want to temporarily use other method to read segs in.
            segments = grab_time_segments(pattern_segs_hveto)

            start_time_utc += datetime.timedelta(days=1)

        write_segs(triggers,f)
        #segments.write(g) 


    elif args.online_offline == 'online':

        #These paths are currently hardwired for online searches. 
	pattern_trigs_hveto = os.path.join(args.directory_path, '{}{:02}','{}{:02}{:02}', '*86400-DARM','*VETO_SEGS_ROUND*.txt')
	pattern_segs_hveto = os.path.join(args.directory_path, '{}{:02}','{}{:02}{:02}', '*86400-DARM', 'segs.txt')
	
	triggers = SegmentList([])
        segments = SegmentList([])

        while start_time_utc < end_time_utc:
	    day = start_time_utc.day
	    month = start_time_utc.month
	    year = start_time_utc.year

            wildcard_trigs_hveto = pattern_trigs_hveto.format(year, month, year, month, day)
	    wildcard_segs_hveto = pattern_segs_hveto.format(year, month,year, month, day)

            triggers = grab_time_triggers(wildcard_trigs_hveto)

            #ideally we'd be able to use the same algorithm, but the SegmentList.read doesn't support csv,
            #which is what the segment files are. So, want to temporarily use other method to read segs in.
            segments = grab_time_segments(wildcard_segs_hveto)

            start_time_utc += datetime.timedelta(days=1)

        write_segs(triggers,f)
        #segments.write(g) 

    else:
        print 'Did not choose online or offline. Please choose.'

###choosing to read in UPVh!###
elif args.type_dq_flag == 'UPVh':
    f = open("total_UPVh_trigs.txt","w")
    g = open("total_UPVh_segs.txt","w")
    
    print 'Data Quality Flag chosen is ' + args.type_dq_flag +', stored in the path ' + args.directory_path 

    pattern_trigs_UPVh = os.path.join(args.directory_path, 'DARM_LOCK_{}_{}-H', 'H1:*veto.txt')
    pattern_segs_UPVh = os.path.join(args.directory_path, 'DARM_LOCK_{}_{}-H', 'segments.txt')

    while start_time_utc < end_time_utc:
        day = start_time_utc.day
        nextday = start_time_utc + datetime.timedelta(days=1)
	day_gps = tconvert(start_time_utc)
        nextday_gps = tconvert(nextday)
      
        wildcard_UPVh_trigs = pattern_trigs_UPVh.format(day_gps, nextday)
        wildcard_UPVh_segs = pattern_trigs_UPVh.format(day_gps, nextday)

        triggers = grab_time_triggers(wildcard_UPVh_trigs)
        segments = grab_time_segments(wildcard_UPVh_segs)

        start_time_utc += datetime.timedelta(days=1)
    write_segs(triggers,f)


###whoops! you forgot to choose hveto, UPVh, or OVL!###
else:
        print 'Did not give correct dq flag. Please choose from hveto, UPVh, OVL in command line.'
        exit()

###################################################
###########CREATING DQ FLAG .XML  FILE#############
###################################################

#construct flag and filename
flag_name = 'H1:' + args.type_dq_flag + '-RND:1'
name = 'segments_' + args.type_dq_flag + '_RND.xml'

#reading in segment files
try: knownsegments = numpy.loadtxt('total_'+ args.type_dq_flag + '_segs.txt')
except:
    print 'No total_'+ args.type_dq_flag + '_segs.txt file in current working directory. It should have been produced from last loop. \n If this  file is empty, that may mean you have no active segments during this time period.'

#NOTE TO SELF: If there were no active segments, so we still want to produce the DQ Flag? Or should we tell it to quit out? 

known_start = [knownsegments[i,0] for i in range(len(knownsegments))]
known_end = [knownsegments[i,1] for i in range(len(knownsegments))]

# reading in trigger files
data = numpy.loadtxt('total_'+ args.type_dq_flag + '_trigs.txt')

# get an array for the start_time and end_time of each segment
start_time = [data[i,0] for i in range(len(data))]
end_time = [data[i,1] for i in range(len(data))]

# create a data quality flag object 
#zip will truncate the start and end time. is this OK?
flag = DataQualityFlag(flag_name, active=zip(start_time, end_time), known=zip(known_start, known_end))

# write flag
flag.write(name)

print "Created DQ Flag: " + flag_name + " in .xml form as: " + name 
###################################################
##############CREATING VET .INI FILE###############
###################################################

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

config.add_section('tab-SNR-6')
config.set('tab-SNR-6', 'name','SNR 6')
config.set('tab-SNR-6', 'type', 'veto-flag')
config.set('tab-SNR-6', 'shortname', 'SNR 6')
config.set('tab-SNR-6', 'flags', flag_name )
config.set('tab-SNR-6', 'states', "Science")
config.set('tab-SNR-6', 'segmentfile', name )

with open(args.type_dq_flag + '_segs.ini','wb') as configfile:
    config.write(configfile)

print "\n Created " + args.type_dq_flag + '_segs.ini. You have everything you need to run VET now! \n(Advance to GO and collect $200.)'
print "To run VET,first go into " + args.type_dq_flag + "_segs.ini, and delete the line that only contains []. Save and exit the .ini file.\n"
print "Now, use the command: gw_summary gps " + str(args.gps_start_time) + " " + str(args.gps_end_time) +  " -f /home/detchar/etc/summary/configurations/defaults.ini -f "+ args.type_dq_flag + "_segs.ini" 

