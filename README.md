# Anomaly Detection
Designed for insight data engineering coding challenge. 
Please find out the situation setting in 
https://github.com/InsightDataScience/anomaly_detection

## Used packages
argparse, time, datetime, heapq (all of these are already in python standard library)

## Usage
#### option 1:
Use the following in command-line:

    anomaly_detection~$ python ./src/process_log.py batch_log stream_log flagged_purchases [-v][-vv]

`batch_log` : file of historical event logs

`stream_log` : file of stream-in event logs

`flagged_purchases` : file to output flagged purchases (Flagged purchases would be write-in as a newline, and would not overwrite the original content.)

`-v` and `-vv` : increase verbosity

#### option 2:
Directlt execute `run.sh` in command-line (with structured default folder and filename):

    anomaly_detection~$ ./run.sh

## Approach summary

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
1. Keep track of the user's friends (`D`=1)
2. Keep track (using heap) of his/her last `T` purchases (`last_T_purchase`), and the last `T` purchases in his/her `D` degree network (`network purchase`) (not including the user's own purchases). 
3. Keep track of the mean (`mean`) and standard deviation (`std`) of the purchases made in user's network.

To speed up, each information of an user are updated in a rolling style. But if friendships have changed ('befriend' or 'unfriend' events), the network related attributes will be rebuild using `build_network_stats`.

### Auxiliary (json_parser.py):
Read: parse a json string into `OrderedDict`, and add an additional timestamp to represent the stream-in time.   
Write: translate `OrderedDict` into a json string.


