#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 10:10:55 2017

@author: kunhua
"""

# Insight Data Engineering Coding Challenge

from datetime import datetime

def parse_json(s):
    '''
    Decode JSON, and add a stream-in timestamp
    s: a string in JSON format
    return: a dictionary object (event)
    '''
    raise NotImplementedError('To be implemented')
    

def build_user(event):
    '''
    Build a new User object if the user id in the event does not exist.
    event: a dictionary
    return: an user object
    '''
    raise NotImplementedError('To be implemented')
