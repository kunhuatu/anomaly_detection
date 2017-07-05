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
    
    def update_network_stats(self, timestamp, time_in, amount):
        '''Update user's network purchase, mean, std with 
           the new purchase made in user's network'''
        if len(self.network_purchase) >= self.T:
            if (timestamp, time_in) > self.network_purchase[0][0]:
                old_record = heapq.heapreplace(self.network_purchase, 
                                               ((timestamp, time_in), amount))
                self._update_mean_std(amount, old_record[1])
        elif len(self.network_purchase) >= 2:
            heapq.heappush(self.network_purchase, ((timestamp, time_in), amount))
            self._update_mean_std(amount)
        else:
            heapq.heappush(self.network_purchase, ((timestamp, time_in), amount))
            self.build_network_stats(self.network_purchase)
    
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
        
    def _update_mean_std(self, new_amount, old_amount=None):
        '''Update network mean and standard deviation with the new amount'''
        n = len(self.network_purchase)
        old_mean, old_std = self.network_mean, self.network_std
        
        if old_amount is not None:
            new_mean = old_mean - (old_amount / n) + (new_amount / n)
            old_mean_xsq = old_std**2 + old_mean**2
            new_mean_xsq = old_mean_xsq - (old_amount**2 / n) + (new_amount**2 / n)
            new_std = (new_mean_xsq - new_mean**2) ** 0.5 
        else:
            new_mean = old_mean * ((n-1) / n) + (new_amount / n)
            old_mean_xsq = old_std**2 + old_mean**2
            new_mean_xsq = old_mean_xsq * ((n-1) / n) + (new_amount**2 / n)
            new_std = (new_mean_xsq - new_mean**2) ** 0.5
                      
        self.network_mean, self.network_std = new_mean, new_std
        
        