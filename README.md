# Anomaly Detection
Designed for insight data engineering coding challenge. 
Please find out the situation setting in 
https://github.com/InsightDataScience/anomaly_detection

## Used packages
argparse, time, datetime, heapq (all of these are already in python standard library)

## Usage
#### option 1:
Use the following in command-line:

    anomaly_detection~$ python ./src/process_log.py ./log_input/batch_log.json ./log_input/stream_log.json ./log_output/flagged_purchases.json [-v][-vv]
`-v` and `-vv` : increase verbosity

#### option 2:
Directlt execute `run.sh` in command-line:

    anomaly_detection~$ ./run.sh

## Approach summary
