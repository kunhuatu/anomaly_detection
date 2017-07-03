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
            for k, v in d.items():
                if re.match('id*', k): d[k] = int(v)
                if k == 'amount': d[k] = float(v)
                if k == 'T' or k == 'D': d[k] = int(v)
                if k == 'timestamp':
                    d[k] = get_timestamp(datetime.strptime(d[k], timestamp_format))
            d['time_in'] = get_timestamp(datetime.now())
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
        for k, v in d.items():
            if re.match('id*', k): d[k] = str(v)
            if k == 'amount' or k == 'mean' or k == 'sd': 
                d[k] = '{:.3f}'.format(v)[:-1]
            if k == 'timestamp': 
                d[k] = str(datetime.fromtimestamp(v))
        return d
        
    obj = num2str(obj)
    return json.dumps(obj)


def get_timestamp(dt):
    '''Get timestamp of a datetime instances'''
    if sys.version_info.major == 3:
        return dt.timestamp()
    return time.mktime(dt.timetuple()) + dt.microsecond / 1e6
