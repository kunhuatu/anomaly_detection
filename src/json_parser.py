#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 10:10:55 2017

@author: kunhua
"""

# Insight Data Engineering Coding Challenge

from __future__ import print_function, division

import sys
import json
import re
import time
from collections import OrderedDict
from datetime import datetime


def read_json(s):
    """
    Decode JSON, and add a stream-in timestamp.
    s: a string in JSON format
    return: a dictionary object (event)
    """
    def str2num(d):
        if isinstance(d, OrderedDict):
            timestamp_format = '%Y-%m-%d %H:%M:%S'
            # add timestamp of stream-in time
            d['time_in'] = get_timestamp(datetime.now())
            # reformat values
            if 'event_type' not in d:
                return d
            elif d['event_type'] == 'purchase':
                d['id'] = int(d['id'])
                d['amount'] = float(d['amount'])
            elif d['event_type'] == 'befriend' or d['event_type'] == 'unfriend':
                d['id1'] = int(d['id1'])
                d['id2'] = int(d['id2'])
                
            d['timestamp'] = get_timestamp(datetime.strptime(d['timestamp'], timestamp_format))
            return d

    event = json.loads(s, object_pairs_hook=OrderedDict)
    return str2num(event)
    

def write_json(obj):
    """
    Encode the anomalous event into JSON format
    obj: event dictionary
    return: string (JSON)
    """
    def num2str(d):
        d['id'] = str(d['id'])
        d['timestamp'] = str(datetime.fromtimestamp(d['timestamp']))
        for k in ['amount', 'mean', 'sd']:
            d[k] = truncate(d[k], 2)
        return d
        
    obj = num2str(obj)
    return json.dumps(obj)


def get_timestamp(dt):
    '''Get timestamp of a datetime instances'''
    if sys.version_info.major == 3:
        return dt.timestamp()
    return time.mktime(dt.timetuple()) + dt.microsecond / 1e6


def truncate(num, nb_decimal_point):
    '''truncate number to "nb_decimal_point" decimal points'''
    integer, decimal = str(num).split('.')
    d_formater = '{:0<' + str(nb_decimal_point) + '}'
    decimal = d_formater.format(decimal)
    return '.'.join([integer, decimal[:nb_decimal_point]])
