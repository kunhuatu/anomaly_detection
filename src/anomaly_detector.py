#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 17:09:28 2017

@author: kunhua
"""

# Insight Data Engineering Coding Challenge
from __future__ import print_function, division

import re
import heapq
from user import User

class Anomaly_Detector(object):
    def __init__(self, D, T):
        self.users = dict()
        self.D = D
        self.T = T
        
    def is_anomalous(self, event):
        '''Check if an event is anomalous'''
        user = self.users[event['id']]
        if len(user.network_purchase) < 2:
            return False
        elif event['amount'] <= user.network_mean + (3 * user.network_std):
            return False
        return True
    
    def check_user(self, event):
        '''Check whether the user(s) involved in the event exists, 
           if not, create a new User instance'''
        for k in event:
            if re.match('id*', k) and event[k] not in self.users:
                self.users[event[k]] = User(event[k], self.T)
                
    def process_history(self, event):
        '''Process history event'''
        if event['event_type'] == 'befriend' or event['event_type'] == 'unfriend':
            uid_1, uid_2 = event['id1'], event['id2']
            getattr(self.users[uid_1], event['event_type'])(uid_2)
            getattr(self.users[uid_2], event['event_type'])(uid_1)
        elif event['event_type'] == 'purchase':
            user = self.users[event['id']]
            user.update_self_purchase(event['timestamp'], event['time_in'], event['amount'])
        else:
            raise ValueError('Unknown event type')
    
    def initialize_user_network_stats(self):
        '''Initialize the network stats of each user'''
        for uid in self.users:
            self.users[uid].build_network_stats(self.get_network_purchase(uid, self.D, self.T))
        
    def process_stream(self, event):
        '''Process stream-in event'''
        to_return = None
        if event['event_type'] == 'befriend' or event['event_type'] == 'unfriend':
            uid_1, uid_2 = event['id1'], event['id2']
            getattr(self.users[uid_1], event['event_type'])(uid_2)
            getattr(self.users[uid_2], event['event_type'])(uid_1)
            friends_affected = self.find_friends(uid_1, self.D-1) | self.find_friends(uid_2, self.D-1) | {uid_1, uid_2}
            for fid in friends_affected:
                self.users[fid].build_network_stats(self.get_network_purchase(fid, self.D, self.T))
        elif event['event_type'] == 'purchase':
            uid = event['id']
            if self.is_anomalous(event):
                to_return = event.copy()
                to_return['mean'] = self.users[uid].network_mean
                to_return['sd'] = self.users[uid].network_std
                del to_return['time_in']
            self.users[uid].update_self_purchase(event['timestamp'], event['time_in'], event['amount'])
            friends_affected = self.find_friends(uid, self.D)
            for fid in friends_affected:
                self.users[fid].update_network_stats(event['timestamp'], event['time_in'], event['amount'])
        else:
            raise ValueError('Unknown event type')
        return to_return
        
    def find_friends(self, user_id, D):
        '''Find friends in user's D-degree network'''
        friend_ids = set()
        deg = 0
        curr_level = {user_id}
        while deg < D and len(curr_level) != 0:
            nxt_level = set()
            for uid in curr_level:
                nxt_level.update(self.users[uid].friends)
            curr_level = nxt_level - friend_ids
            friend_ids.update(curr_level)
            deg += 1
        friend_ids -= {user_id}
        return friend_ids
    
    def get_network_purchase(self, user_id, D, T):
        '''Get last T purchase in user's D-degree network'''
        friend_ids = self.find_friends(user_id, D)
        purchases = []
        for uid in friend_ids:
            friend = self.users[uid]
            for prch in friend.get_last_T_purchase():
                if len(purchases) < T:
                    heapq.heappush(purchases, prch)
                elif prch[0] > purchases[0][0]:
                    heapq.heapreplace(purchases, prch)
        return purchases
