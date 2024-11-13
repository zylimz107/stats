import json
import random
import re
import statistics
from datetime import datetime, timedelta

# --- Helper Functions ---
def get_user_input():
    """Prompt user for statistics file and number of days."""
    stats_file = input("Enter the path to the new statistics file: ")
    num_days = int(input("Enter the number of days to generate activity data: "))
    return stats_file, num_days

# --- Parsing Functions ---
def parse_events(file_path):
    """Parse Events.txt to extract event details."""
    events = []
    with open(file_path, 'r') as file:
        num_events = int(file.readline().strip())  # First line: number of events
        for _ in range(num_events):
            line = file.readline().strip()
            event_data = re.split(r'[:]', line)
            event_name = event_data[0]
            event_type = event_data[1]
            min_value = float(event_data[2]) if event_data[2] else 0
            max_value = float(event_data[3]) if event_data[3] else None
            weight = int(event_data[4])
            events.append({
                'name': event_name,
                'type': event_type,
                'min': min_value,
                'max': max_value,
                'weight': weight
            })
    return events

def parse_stats(file_path):
    """Parse Stats.txt to extract mean and standard deviation for each event."""
    stats = {}
    with open(file_path, 'r') as file:
        num_events = int(file.readline().strip())  # First line: number of events
        for _ in range(num_events):
            line = file.readline().strip()
            event_data = re.split(r'[:]', line)
            event_name = event_data[0]
            mean = float(event_data[1])
            std_dev = float(event_data[2])
            stats[event_name] = {'mean': mean, 'std_dev': std_dev}
    return stats

def check_consistency(events, stats):
    """Check for consistency between Events.txt and Stats.txt."""
    inconsistencies = []
    for event in events:
        if event['name'] not in stats:
            inconsistencies.append(event['name'])
    if inconsistencies:
        print("Inconsistencies found in the following events:", inconsistencies)
    else:
        print("All events have corresponding statistics.")

# --- Activity Engine ---
def generate_event_value(event, stats):
    """Generate a value for an event based on its type and statistics."""
    mean = stats[event['name']]['mean']
    std_dev = stats[event['name']]['std_dev']
    if event['type'] == 'D':  # Discrete event
        return round(random.gauss(mean, std_dev))
    elif event['type'] == 'C':  # Continuous event
        return round(random.gauss(mean, std_dev), 2)

def generate_daily_log(events, stats):
    """Generate a log entry for one day of events."""
    daily_log = {}
    for event in events:
        daily_log[event['name']] = generate_event_value(event, stats)
    return daily_log

def run_activity_engine(events, stats, num_days, log_file='activity_log.json'):
    """Run the activity engine to generate event logs over multiple days."""
    logs = []
    current_date = datetime.now()
    for day in range(num_days):
        daily_log = generate_daily_log(events, stats)
        daily_log['date'] = (current_date + timedelta(days=day)).strftime('%Y-%m-%d')
        logs.append(daily_log)
    with open(log_file, 'w') as file:
        json.dump(logs, file, indent=2)
    print("Event generation complete.")

# --- Analysis Engine ---
def calculate_baseline_stats(logs):
    """Calculate the baseline statistics (mean, std deviation) for each event."""
    print("Starting Analysis engine...")
    event_data = {}
    
    # Collect event data
    for log in logs:
        for event, value in log.items():
            if event != 'date':  # Skip the date field
                if event not in event_data:
                    event_data[event] = []
                event_data[event].append(value)
    
    baseline_stats = {}
    
    # Calculate baseline statistics (mean, std dev)
    for event, values in event_data.items():
        mean = sum(values) / len(values)  # Calculate mean manually to avoid rounding errors
        std_dev = statistics.pstdev(values) if len(values) > 1 else 0  # Population std dev
        
        baseline_stats[event] = {
            'mean': round(mean, 2),
            'std_dev': round(std_dev, 2)
        }
    
    print("Analysis complete.")
    return baseline_stats

def calculate_and_save_daily_totals(logs, output_file='DailyTotals.json'):
    """Calculate daily totals for each log and save them to a JSON file."""
    daily_totals = []
    for log in logs:
        daily_total = sum(value for key, value in log.items() if key != 'date')
        daily_totals.append({'date': log['date'], 'daily_total': round(daily_total, 2)})
    
    with open(output_file, 'w') as file:
        json.dump(daily_totals, file, indent=2)
    print(f"Daily totals saved to {output_file}")

def save_baseline_stats(baseline_stats, filename='baseline_stats.json'):
    """Save the baseline statistics to a file."""
    with open(filename, 'w') as file:
        json.dump(baseline_stats, file, indent=2)
    print(f"Baseline statistics saved to {filename}")

def load_activity_logs(log_file='activity_log.json'):
    """Load activity logs from a JSON file."""
    with open(log_file, 'r') as file:
        logs = json.load(file)
    return logs

# --- Alert Engine ---
def calculate_anomaly_counter(daily_log, baseline_stats, events):
    """Calculate the anomaly counter for a given day based on event deviations."""
    anomaly_counter = 0
    for event in events:
        event_name = event['name']
        if event_name in daily_log:
            observed_value = daily_log[event_name]
            baseline_mean = baseline_stats[event_name]['mean']
            baseline_std_dev = baseline_stats[event_name]['std_dev']
            weight = event['weight']
            
            if baseline_std_dev > 0:  # Avoid division by zero
                deviation = abs(baseline_mean - observed_value) / baseline_std_dev
                weighted_deviation = deviation * weight
                anomaly_counter += weighted_deviation
    return anomaly_counter

def detect_anomalies(logs, baseline_stats, events):
    """Detect anomalies based on the calculated anomaly counter and threshold."""
    threshold = 2 * sum(event['weight'] for event in events)
    
    alerts = []
    for log in logs:
        anomaly_counter = calculate_anomaly_counter(log, baseline_stats, events)
        date = log['date']
        alert_status = 'Flagged' if anomaly_counter >= threshold else 'Okay'
        alerts.append({
            'date': date,
            'anomaly_counter': round(anomaly_counter, 2),
            'threshold': threshold,
            'status': alert_status
        })
    return alerts

# --- Main Function ---
def main():
    while True:
        stats_file, num_days = get_user_input()
        events = parse_events('Events.txt')
        baseline = parse_stats('Stats.txt')
        stats = parse_stats(stats_file)
        
        check_consistency(events, stats)
        
        run_activity_engine(events, stats, num_days)
        
        logs = load_activity_logs()
        baseline_stats = calculate_baseline_stats(logs)
        save_baseline_stats(baseline_stats)
        
        # Calculate and save daily totals for later use in the alert phase
        calculate_and_save_daily_totals(logs)
        
        # Detect anomalies
        alerts = detect_anomalies(logs, baseline, events)
        for alert in alerts:
            print(alert)
        
        repeat = input("Would you like to analyze another file? (yes/no): ")
        if repeat.lower() != 'yes':
            break

if __name__ == "__main__":
    main()