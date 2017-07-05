# Anomaly Detection
Designed for insight data engineering coding challenge. 
Please find out the situation setting in 
https://github.com/InsightDataScience/anomaly_detection

## Environment
Python 2, 3 (tested on python 2.7 and 3.5)
#### Used packages
`argparse`, `time`, `datetime`, `heapq`, `math`, `collections` (all of these are already in python standard library)

## Usage
#### option 1:
Use the following in command-line:

    anomaly_detection~$ python ./src/process_log.py batch_log stream_log flagged_purchases [-v][-vv]

`batch_log` : file of historical event logs

`stream_log` : file of stream-in event logs

`flagged_purchases` : file to output flagged purchases (Flagged purchases would be write-in as a newline, and would not overwrite the original content.)

`-v` and `-vv` : increase verbosity

#### option 2:
Directly execute `run.sh` in command-line (with structured default folder and filename):

    anomaly_detection~$ ./run.sh

## Approach Summary

The task has been divided into three different levels: processing level, detector level, user level. An auxiliary `json_parser` is used to read and write json format. 

### Processing level (process_log.py):
1. Get the value of

    `D` : the number of degrees that defines a user's social network.   
    `T` : the number of consecutive purchases made by a user's social network (not including the user's own purchases)
    
2. Create a detector and initialize the detector with the historical events in batch log file
3. For each event in stream-in log file, use detector to determine whether it is a anomalous purchase, and then update the detector with the new event.

### Detector level (anomaly_detector.py):
Keep track of all users appeared in events. When a new event coming in, create a new user if he/she does not exist, and then update the information in related users (using BFS to search in `D` degree network).

### User level (user.py):
In each user,
1. keep track of the user's friends (`D`=1)
2. keep track (using heap) of his/her last `T` purchases (`last_T_purchase`), and the last `T` purchases in his/her `D` degree network (`network purchase`) (not including the user's own purchases) 
3. keep track of the mean (`mean`) and standard deviation (`std`) of the purchases made in user's network

To speed up, each information of an user are updated in a rolling style. But if friendships have changed ('befriend' or 'unfriend' events), the network related attributes will be rebuild using `build_network_stats`.

### Auxiliary (json_parser.py):
Read: parse a json string into `OrderedDict`, and add an additional timestamp to represent the stream-in time.   
Write: translate `OrderedDict` into a json string.

## Further Discussion
#### 1. Whether it is good or not to keep track of the network purchases for each user? (use heap implementation)    
Assuming users have an average of `N` friends in their D degree network, when a 'purchase' event comes in, the processing time complexity is O(N logT) if we keep track the network purchases, and if we do not, the time complexity would be O(NT logT). On the other hand, if the event is 'befriend' or 'unfriend', the processing time complexity would be O(N^2T logT) for keeping track of network purchases and O(1) for not doing it. So if most of the event are purchases, keeping track of the network purchase for each user would save us some time; however, if there are lots of (be/un)friend events, it may turn out to be slow. Here I chose to implementation with keeping track of it because I would think 'purchase' should happen more often than '(be/un)friend'.
 
#### 2. What's data structure to use for personal purchase history (last T purchases)? Heap or Deque?
In my opinion, it depends on whether the stream-in data is ordered in time. If it is, then a fixed-size FIFO deque should be good to use, and updating the history only cost O(1) time complexity. But if it isn't, a heap is required and the time complexity for updating would be O(logT). I would think using heap here is more safe and flexible, since there may be multiple stream-in sources at the same time and the event log can be non-ordered when combining the sources.
