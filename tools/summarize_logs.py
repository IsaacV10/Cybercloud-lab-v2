"""Summarize honeypot logs: total events, events per type, events per day."""
import json
import sys
from collections import Counter
from pathlib import Path


def read_events(folder):
    """Yield one event (a dict) per line, from every log file in the folder."""
    for path in sorted(Path(folder).glob("*.log*")):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield json.loads(line)


def main():
    folder = sys.argv[1]
    by_type = Counter()
    by_day = Counter()
    total = 0

    for event in read_events(folder):
        total += 1

        # count this event's event_type in by_type
        event_type = event["event_type"] 
        by_type [event_type] = by_type.get(event_type,0) + 1
        
        # get the day from the timestamp and count it in by_day
        day = event["timestamp"][:10]
        by_day[day] = by_day.get(day,0) + 1
    
    print("Total events:", total)
    # print each event type and its count, most common first
    print("\nEvents by type:")
    for event_type, count in by_type.most_common():
        print(f"  {event_type:<20} {count:>8,}")
    # print each day and its count, in date order
    print("\nEvents by day:")
    for day, count in sorted(by_day.items()):
        print(f"  {day}  {count:>8,}")

if __name__ == "__main__":
    main()