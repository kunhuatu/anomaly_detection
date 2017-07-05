#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 01:29:35 2017

@author: kunhua
"""

# Insight Data Engineering Coding Challenge
from __future__ import print_function, division

import time
import argparse
from json_parser import read_json, write_json
from anomaly_detector import Anomaly_Detector

def process_batch(batch_log, verbose=0):
    '''
    Process historical events from batch log
    batch_log : filepath of historical logs (batch_log.json)
    return : an anomaly_detector instance
    '''
    with open(batch_log, 'r') as log:
        D, T = map(int, map(read_json(log.readline().rstrip('\n')).get, ['D', 'T']))
        assert(D >= 1 and T >= 2) # check for valid D and T
        
        ### create detector ###
        detector = Anomaly_Detector(D, T)
        
        ### start loading data ###
        if verbose: 
            print('Loading historical data...', end='')
            timer_start = time.time()
        line = log.readline().rstrip('\n')
        while line:
            event = read_json(line)
            detector.check_user(event)
            detector.process_history(event)
            line = log.readline().rstrip('\n')
        if verbose: 
            timer_end = time.time()
            print('done!  ' + 'time spent : {:.3f} s'.format(timer_end-timer_start))
        
        ### initialize detector ###
        if verbose: 
            print('Initialize anomaly detector...', end='')
            timer_start = time.time()
        detector.initialize_user_network_stats()
        if verbose: 
            timer_end = time.time()
            print('done!  ' + 'time spent : {:.3f} s'.format(timer_end-timer_start))
        
    return detector


def process_stream(detector, stream_log, flagged_purchase, verbose=0):
    '''
    Process stream-in events from stream log
    detector : an anomaly_detector instance
    stream_log : filepath of stream-in logs (stream_log.json)
    flagged_purchase : filepath to write flagged evnets
    '''
    if verbose > 0: 
        print('Processing stream-in data...')
        timer_start = time.time()
    
    with open(stream_log, 'r') as log:
        with open(flagged_purchase, 'a') as f:
            ### process each line ###
            line = log.readline().rstrip('\n')
            while line:
                t_start = time.time()
                event = read_json(line)
                detector.check_user(event)
                flag_event = detector.process_stream(event)
                t_end = time.time()
                
                if verbose >= 2:
                    print('event type : {} -- {:.3f} s'.format(event['event_type'], 
                                                                           t_end - t_start))
                ### write to file if detected a anomalous event ###
                if flag_event is not None:
                    f.write(write_json(flag_event) + '\n')
    
                line = log.readline().rstrip('\n')
                
    if verbose > 0: 
        timer_end = time.time()
        print('done!  ' + 'time spent : {:.3f} s'.format(timer_end-timer_start))
    

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('batch_log', type=str, help='path of batch log json file')
    arg_parser.add_argument('stream_log', type=str, help='path of stream log json file')
    arg_parser.add_argument('flagged_purchases', type=str, help='path to store flagged purchases')
    arg_parser.add_argument('-v', '--verbose', action="count", default=0, 
                            help='increase processing verbosity')
    args = arg_parser.parse_args()
        
    detector = process_batch(args.batch_log, verbose=args.verbose)
    process_stream(detector, args.stream_log, args.flagged_purchases, verbose=args.verbose)
    
            
            
            
                
            
                    