# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 14:00:05 2018

@author: WilliamCh
"""

from datetime import date, timedelta, datetime
import logging
from auto_query import call_open_rem



#Set up a logger so we can see what the script has been doing for us lately
logger = logging.getLogger('qraday')
logger.setLevel(logging.DEBUG)
#fh = logging.FileHandler('c:/Users/bts-admin/Desktop/qraday.log')
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#fh.setFormatter(formatter)
#logger.addHandler(fh)

################ INPUTS ################

#Set time
#Choose a day equally distant from a fixed point in time as today is

def load_date_list(fn = 'date_query_log.txt'):
    try:
        with open(fn, 'r') as f:
            str_date_list = f.readlines()
        str_date_list = map(str.strip, str_date_list)
        date_list = [datetime.strptime(d, '%Y-%m-%d') for d in str_date_list]
        date_list = [d.date() for d in date_list]
    except:
        print('could not load dates, making new list')
        historical_cutoff = date(2019, 7, 24)
        date_list = [historical_cutoff]
    return date_list

def save_date_list(date_list):
    with open('date_query_log.txt', 'w') as f:
        f.write('\n'.join([str(d) for d in date_list]))

date_query_log = load_date_list()

start_date = min(date_query_log) - timedelta(days=1)
end_date =  min(date_query_log) - timedelta(days=1)
date_query_log.append(end_date)
save_date_list(date_query_log)

#Create a dictionary defining the station names to include
#Note: Currently each list needs to have a junk string at the front and back
#for reasons unknown
include_station_names = ['test1', 'test2', 'test3', 'test4']

exclude_station_names = ['test5']

modalities = ['ct', 'mg', 'dx', 'fl']

study_description_exclude = ['mortem', 'coronial']

################ General string formatting ################
    
if __name__=='__main__':
    
    #Main query
    call_open_rem(sni=include_station_names,
                  sne=exclude_station_names,
                  modalities=modalities,
                  sde=study_description_exclude,
                  start_date=start_date,
                  end_date=end_date)

                  
