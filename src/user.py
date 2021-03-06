#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 11:03:50 2017

@author: kunhua
"""

# Insight Data Engineering Coding Challenge

from __future__ import print_function, division

import heapq
import math


class User(object):
    '''An user object that keeps user's information'''
    def __init__(self, user_id, T):
        self.id = user_id
        self.T = T
        self.friends = set()
        self.last_T_purchase = []
        self.network_purchase = []
        self.network_mean = -1
        self.network_std = -1
        self.purchase_history = []  #To be used if there is a desire to change T in the middle of processing
                                    #Related functions have not been implemented
        
    def befriend(self, user_id):
        '''Add someone to friends'''
        self.friends.add(user_id)
        
    def unfriend(self, user_id):
        '''Remove someone from friends'''
        self.friends.remove(user_id)
        
    def update_self_purchase(self, timestamp, time_in, amount):
        '''Update queue of user's last T purchase'''
        if len(self.last_T_purchase) >= self.T:
            if (timestamp, time_in) > self.last_T_purchase[0][0]:
                heapq.heapreplace(self.last_T_purchase, ((timestamp, time_in), amount))
        else:
            heapq.heappush(self.last_T_purchase, ((timestamp, time_in), amount))
    
    def build_network_stats(self, purchases):
        '''(re)Build a purchase list made by user's network and 
           calculate the mean and standard deviation'''
        self.network_purchase = purchases
        if len(purchases) < 2 :
            self.network_mean, self.network_std = -1, -1
        else:
            amounts = [prch[1] for prch in purchases]
            mean = math.fsum(amounts) / len(amounts)
            variance = math.fsum((val - mean)**2 for val in amounts) / len(amounts)
            self.network_mean = mean
            self.network_std = math.sqrt(variance)
            
    def get_last_T_purchase(self):
        '''Return user's last T purchases'''
        return self.last_T_purchase[:]
        
        