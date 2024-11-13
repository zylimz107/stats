Event Modeler and Intrusion Detection System

This Python project simulates an event modeler and intrusion detection system, processing event logs and detecting anomalies based on defined thresholds. It uses JSON to store activity logs and calculates daily totals, mean, and standard deviation for event statistics.

Prerequisites
Python 3.x: Ensure Python 3.x is installed on your machine.
Packages: This script relies on built-in Python libraries (e.g., json, random, re, statistics), so no additional package installations are required.
Files Required:

Events.txt
Stats.txt

Usage Instructions

1. Setting Up the Environment
Place Events.txt and Stats.txt in the same directory as this script, or provide the file paths during runtime.

2. Running the Script
Run the script in a terminal or command prompt:

python alert.py

The script will prompt for:

The path to a new statistics file.
The number of days to simulate event activity.

3. Functionality Overview
The script performs the following main tasks:

Activity Generation:

Uses Events.txt and the provided statistics file to generate random activity data based on event types (discrete or continuous).
Saves generated activity logs to activity_log.json.

Analysis Engine:

Calculates mean and standard deviation for each event across the simulated days.
Stores baseline statistics in baseline_stats.json.
Computes daily totals for each day and saves them in DailyTotals.json.

Alert Engine:

Compares daily event values to baseline statistics to detect anomalies.
Flags days with anomalies exceeding a threshold, calculated from event weights.
Prints an alert for each day, indicating whether it's flagged or okay.

4. Additional Notes
Threshold Adjustment: The threshold for anomaly detection can be configured within the code for higher sensitivity or robustness.
Restart Option: At the end of each run, the program will prompt whether to analyze another file, allowing multiple analyses within one session.
