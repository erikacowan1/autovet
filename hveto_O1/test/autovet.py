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
parser = argparse.ArgumentParser(
	description='autovet.py is a program that grabs triggers and segments for hveto, UPVh, and OVL for any time period, and concatenates them into one segment file, and one trigger file.It then creates a DQ Flag for the given type and time period, spits out a .xml file, and generates the .ini file needed to run VET. For questions or concerns, contact Erika Cowan at erika.cowan@ligo.org')
parser.add_argument('gps_start_time',type=int,help='Please enter GPS start time')
parser.add_argument('gps_end_time',type=int,help='Please enter GPS end time')
parser.add_argument('directory_path',type=str,help='Please enter directory path for triggers and segments')
parser.add_argument('-s','--start_date', type=str, help='Please enter start date in YYYYMMDD format, required for the hveto option') 
parser.add_argument('-e','--end_date', type=str, help='Please enter end date in YYYYMMDD format, required for the hveto option')
parser.add_argument('type_dq_flag', type=str, help='Please enter either hveto, UPVh, OVL')
parser.add_argument('hveto_analysis_seg', type=str, help='Please enter offline hveto O1 offline analysis segment, 4,5,6,8,9')
parser.add_argument('online_offline', type=str, help='Please enter either offline or online. This is for hveto.')
args = parser.parse_args()

#A check to make sure we're within the time window of aLIGO, and that end_time is after start_time
if args.gps_start_time < 971574400: #roughly the end of S6
    parser.error("gps_start_time before S6")
if args.gps_end_time < args.gps_start_time:
    parser.error("end_time is before gps_start_time")

###################################################
#######CREATING TOTAL TRIGGER/SEGMENT FILES########
###################################################

###choosing to read in hveto!###
if args.type_dq_flag == 'hveto':
	print 'Data Quality Flag chosen is hveto, stored in the path ' + args.directory_path + '. (Take a Walk on the Board Walk. Advance Token to Board Walk.'
        if args.online_offline == 'offline':
                analysis_segs_45689 = ['4', '5', '6', '8', '9']

                if args.hveto_analysis_seg in analysis_segs_45689:
			pattern_trigs_hveto= os.path.join(args.directory_path, 'analysis' + args.hveto_analysis_seg , 'H1-omicron_BOTH-*-DARM','*VETO_SEGS_ROUND*.txt')
			print pattern_trigs_hveto
		
		else:
                      	print 'Did not choose O1 analysis segment 1,2,3,4,5,6,7,8,9. Please choose.'
                       	exit()
                       	
	else:
                print 'Did not choose online or offline. Please choose.'
               # exit()
'''
                        print 'Data Quality Flag chosen is hveto, stored in the path ' + args.directory_path + '. (Take a Walk on the Board Walk. Advance Token to Board Walk.'

                        #TRIGGER HANDLING: begin for loop that loops over the range of all days/months/years
                        f = open("total_hveto_trigs.txt", "w") #file that will hold collection of all triggers

                        #create pattern paths for the trigger segment files to loop over
                        #NOTE TO SELF: create option to specify which trigger files to loop over. default it to '*VETO_SEGS_ROUND*.txt', and then in the --help, specify how to put in your own list of trigger files.
                        pattern_trigs_hveto = os.path.join(args.directory_path, 'analysis' + args.hveto_analysis_seg , 'H1-omicron_BOTH-*-DARM','*VETO_SEGS_ROUND*.txt')
                        print pattern_trigs_hveto
                        #grabbing the trigger files
                        for filename in glob.glob(pattern_trigs_hveto):
                                #loading the triggers in
                                data = numpy.atleast_2d(numpy.loadtxt(filename))
                                print data

                                #creating and filling arrays to store the data
                                start_time = [data[i,0] for i in range(len(data))]
                                end_time = [data[i,1] for i in range(len(data))]

                                #writing the two arrays to total_hveto_trigs.txt
                                for index in range(len(start_time)):
                                        f.write(str(start_time[index]) + " " + str(end_time[index]) + "\n")

                        f.close()

                        #SEGMENT HANDLING: begin for loop that loops over the range of all days/months/years

                        f = open("total_hveto_segs.txt","w") #file that will hold collection of all segments
                        pattern_segs_hveto = os.path.join(args.directory_path, 'analysis' + args.hveto_analysis_seg , 'H1-omicron_BOTH-*-DARM','segs.txt')
                        print pattern_segs_hveto
                        #grabbing segment files
                        for filename in glob.glob(pattern_segs_hveto):
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
		print pattern_trigs_hveto

                elif args.hveto_analysis_seg == '2':
                        print 'Data Quality Flag chosen is hveto, stored in the path ' + args.directory_path + '. (Take a Walk on the Board Walk. Advance Token to Board Walk.'

                        #TRIGGER HANDLING: begin for loop that loops over the range of all days/months/years
                        f = open("total_hveto_trigs.txt", "w") #file that will hold collection of all triggers

                        #create pattern paths for the trigger segment files to loop over
                        #NOTE TO SELF: create option to specify which trigger files to loop over. default it to '*VETO_SEGS_ROUND*.txt', and then in the --help, specify how to put in your own list of trigger files.
                        pattern_trigs_hveto = os.path.join(args.directory_path,'H1-omicron_BOTH-*-DARM','*VETO_SEGS_ROUND*.txt')
                        print pattern_trigs_hveto
                        #grabbing the trigger files
                        for filename in glob.glob(pattern_trigs_hveto):
                                #loading the triggers in
                                data = numpy.atleast_2d(numpy.loadtxt(filename))
                                print data

                                #creating and filling arrays to store the data
                                start_time = [data[i,0] for i in range(len(data))]
                                end_time = [data[i,1] for i in range(len(data))]

                                #writing the two arrays to total_hveto_trigs.txt
                                for index in range(len(start_time)):
                                        f.write(str(start_time[index]) + " " + str(end_time[index]) + "\n")

                        f.close()


                elif args.hveto_analysis_seg == '3':
                        print args.hveto_analysis_seg

                elif args.hveto_analysis_seg == '7':
                        print args.hveto_analysis_seg		



                
	elif args.online_offline == 'online':
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
						data = numpy.atleast_2d(numpy.loadtxt(filename))

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

	else:
                print 'Did not choose online or offline. Please choose.'
               # exit()
                
###choosing to read in UPVh!###
elif args.type_dq_flag == 'UPVh':
	print 'Data Quality Flag chosen is ' + args.type_dq_flag +', stored in the path ' + args.directory_path + '. (Take a Walk on the Board Walk. Advance Token to Board Walk.'

	#TRIGGER HANDLING: begin for loop that loops over the range of dates
	f = open("total_UPVh_trigs.txt", "w")
	pattern_trigs_UPVh = os.path.join(args.directory_path, 'DARM_LOCK_{}_{}-H', 'H1:*veto.txt')

	for day in range(args.gps_start_time, args.gps_end_time + 1, 86400):
		wildcard_UPVh_trigs = pattern_trigs_UPVh.format(day, day+86400)

		#grabbing segment files
		for filename in glob.glob(wildcard_UPVh_trigs):

			#loading segments in
			data = numpy.loadtxt(filename)

			#storing the segments in these two arrays
			start_time = [data[i,0] for i in range(len(data))]
			end_time = [data[i,1] for i in range(len(data))]

			#writing the two arrays to total_UPVh_trigs.txt
			for index in range(len(start_time)):
				f.write(str(start_time[index]) + " " + str(end_time[index]) + "\n")


	#SEGMENT HANDLING: begin for loop that loops over the range of dates
	f = open("total_UPVh_segs.txt","w")
	pattern_segs_UPVh = os.path.join(args.directory_path, 'DARM_LOCK_{}_{}-H', 'segments.txt')

	for day in range(args.gps_start_time, args.gps_end_time +1, 86400):
		wildcard_UPVh_segs = pattern_segs_UPVh.format(day, day + 86400)

		#grabbing segment files 
		for filename in glob.glob(wildcard_UPVh_segs):
			if os.path.isfile(filename):
				print filename + " exists. Adding to total_UPVh_segs.txt."

				#loading segments in		
				knownsegments = numpy.loadtxt(filename)

				#storing the segments in these two arrays
				known_start = [knownsegments[i,0] for i in range(len(knownsegments))]
				known_end = [knownsegments[i,1] for i in range(len(knownsegments))]

				#writing the two arrays to total_UPVh_segs.txt
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

config.add_section('tab-SNR-5.5')
config.set('tab-SNR-5.5', 'name','SNR 5.5')
config.set('tab-SNR-5.5', 'type', 'veto-flag')
config.set('tab-SNR-5.5', 'shortname', 'SNR 5.5')
config.set('tab-SNR-5.5', 'flags', flag_name )
config.set('tab-SNR-5.5', 'states', "Science")
config.set('tab-SNR-5.5', 'segmentfile', name )

with open(args.type_dq_flag + '_segs.ini','wb') as configfile:
	config.write(configfile)

print "\n Created " + args.type_dq_flag + '_segs.ini. You have everything you need to run VET now! \n(Advance to GO and collect $200.)'
print "To run VET,first go into " + args.type_dq_flag + "_segs.ini, and delete the line that only contains []. Save and exit the .ini file.\n"
print "Now, use the command: gw_summary gps " + str(args.gps_start_time) + " " + str(args.gps_end_time) +  " -f /home/detchar/etc/summary/configurations/defaults.ini -f "+ args.type_dq_flag + "_segs.ini" 
'''
