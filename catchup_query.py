# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 14:00:05 2018

@author: WilliamCh
"""

from datetime import date, timedelta, datetime
import logging
from auto_query import call_open_rem
from auto_query_historical import load_date_list, save_date_list



#Set up a logger so we can see what the script has been doing for us lately
logger = logging.getLogger('qraday')
logger.setLevel(logging.DEBUG)
#fh = logging.FileHandler('c:/Users/bts-admin/Desktop/qraday.log')
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#fh.setFormatter(formatter)
#logger.addHandler(fh)

date_query_log = load_date_list()

################ INPUTS ################




#Create a dictionary defining the station names to include
#Note: Currently each list needs to have a junk string at the front and back
#for reasons unknown
include_station_names = ['test1', 'test2', 'test3']

exclude_station_names = ['test5']

modalities = ['ct'] #, 'mg', 'dx', 'fl'

study_description_exclude = ['mortem', 'coronial']

################ General string formatting ################
    
if __name__=='__main__':
    
    #Main query
    for date in date_query_log:
        start_date = str(date)
        end_date = start_date
    
        call_open_rem(sni=include_station_names,
                      sne=exclude_station_names,
                      modalities=modalities,
                      sde=study_description_exclude,
                      start_date=start_date,
                      end_date=end_date)
        print(date)
        print('query sent')
        failure
                  
