# Anomaly Detection
Designed for insight data engineering coding challenge. 
Please find out the situation setting in 
https://github.com/InsightDataScience/anomaly_detection

## Used packages
argparse, time, datetime, heapq (all of these are already in python standard library)

## Usage
#### option 1:
Use the following in command-line:

    anomaly_detection~$ python ./src/process_log.py batch_log.json./log_input/ ./log_input/stream_log.json ./log_output/flagged_purchases.json [-v][-vv]

`batch_log` : file of historical event logs

`stream_log` : file of stream-in logs

`flagged_purchases` : file to output flagged purchases (Flagged purchases would be write-in as a newline, and would not overwrite the original content.)

`-v` and `-vv` : increase verbosity

#### option 2:
Directlt execute `run.sh` in command-line (with structured folder and filename):

    anomaly_detection~$ ./run.sh

## Approach summary
