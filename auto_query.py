# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 14:00:05 2018

@author: WilliamCh
"""

from datetime import date, timedelta
import os
import subprocess
import time
import logging

#Set up a logger so we can see what the script has been doing for us lately
logger = logging.getLogger('qraday')
logger.setLevel(logging.DEBUG)
#fh = logging.FileHandler('c:/Users/bts-admin/Desktop/qraday.log')
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#fh.setFormatter(formatter)
#logger.addHandler(fh)

################ INPUTS ################

start_date = date.today() - timedelta(days=2)
end_date = date.today() - timedelta(days=1)

#Create a dictionary defining the station names to include
#Note: Currently each list needs to have a junk string at the front and back
#for reasons unknown
include_station_names = ['test1', 'test2', 'test3', 'test4', 'test5']

exclude_station_names = ['MOR0']

modalities = ['ct', 'mg', 'dx', 'fl']

study_description_exclude = ['mortem', 'coronial']

################ General string formatting ################

#Time arguments
def format_time(datetime):
    return datetime.strftime('%Y-%m-%d')

#script location
scriptstr = "/app/openrem/scripts/openrem_qr.py"

logger.debug('Beginning queries')

################ Call OpenREM ################

def call_open_rem(modalities=['ct','fl','mg','dx'],
                  start_date=date.today(), end_date=None,
                  remote_id='1', store_id='1',
                  sni=None, sne=None, 
                  sde=None, sdi=None):
    if len(modalities)==1:
        modalities = [modalities]
    #Modality by modality query
    for modality in modalities:
        args = ['python', scriptstr, remote_id, store_id]
        args.append('-' + modality)
        args.append('-f')
        args.append(str(start_date))
        if end_date:
            args.append('-t')
            args.append(str(end_date))
        if sni:
            args.append('-sni')
            args.append(','.join(sni))
        if sne:
            args.append('-sne')
            args.append(','.join(sne))
        if sdi:
            args.append('-i')
            args.append(','.join(sdi))
        if sde:
            args.append('-e')
            args.append(','.join(sde))
        
        logger.info('Submitting query for ' + modality )
        #Call the script with the arguments we've collated
        print(args)
        p = subprocess.Popen(args, cwd = '/app/openrem/remapp/netdicom', shell = False)
        x = p.communicate() #This actually does nothing, because the subprocess starts a sub-sub process rather than doing anything itself
        time.sleep(120) # Wait 2 minutes before starting the next modality
    logger.info('End query submissions')
if __name__=='__main__':

    #Main query
    call_open_rem(sni=include_station_names,
                  sne=exclude_station_names,
                  sde=study_description_exclude,
                  start_date=start_date,
                  end_date=end_date)
                  
    #Historical query
    #call_open_rem(sni=include_station_names,
    #              sne=exclude_station_names,
    #              sde=study_description_exclude,
    #              start_date=start_date,
    #              end_date=end_date)
                  
