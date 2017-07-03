#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 01:29:35 2017

@author: kunhua
"""

# Insight Data Engineering Coding Challenge
from __future__ import print_function, division

import os
import sys
import time
from json_parser import read_json, write_json
from anomaly_detector import Anomaly_Detector

def process_batch(batch_log, verbose=0):
    '''Process history events from batch log'''
    with open(batch_log, 'r') as log:
        D, T = map(int, map(read_json(log.readline().rstrip('\n')).get, ['D', 'T']))
        assert(D >= 1 and T >= 2) # check for valid D and T
        
        ### create detector ###
        detector = Anomaly_Detector(D, T)
        
        ### start loading data ###
        if verbose: print('Loading historical data...', end='')
        line = log.readline().rstrip('\n')
        while line:
            event = read_json(line)
            detector.check_user(event)
            detector.process_history(event)
            line = log.readline().rstrip('\n')
        if verbose: print('done!')
        
        ### initialize detector ###
        if verbose: print('Initialize anomaly detector...', end='')
        detector.initialize_user_network_stats()
        if verbose: print('done!')
        
    return detector


def process_stream(detector, stream_log, flagged_purchase, verbose=0):
    '''Process stream-in events from stream log'''
    if verbose > 0: print('Processing stream-in data...', end='')
    
    with open(stream_log, 'r') as log:
        with open(flagged_purchase, 'a') as f:
            ### process each line ###
            line = log.readline().rstrip('\n')
            while line:
                timer_start = time.time()
                event = read_json(line)
                detector.check_user(event)
                flag_event = detector.process_stream(event)
                timer_end = time.time()
                
                if verbose==2:
                    print('event type:{}, time_spent:{:.3f}s'.format(event['event_type'], 
                                                                     timer_end - timer_start))
                ### write to file if detected a anomalous event ###
                if flag_event is not None:
                    f.write(write_json(flag_event) + '\n')
    
                line = log.readline().rstrip('\n')
                
    if verbose > 0: print('done!')

if __name__ == "__main__":
    process_log, batch_log, stream_log, flagged_purchase = sys.argv
        
    detector = process_batch(batch_log, verbose=1)
    process_stream(detector, stream_log, flagged_purchase, verbose=1)
    
            
            
            
                
            
                    