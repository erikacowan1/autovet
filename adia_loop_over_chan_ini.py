import argparse


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

#code that can loop over channels while generating the .ini file, not necessary for now
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
