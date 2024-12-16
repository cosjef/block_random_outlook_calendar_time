"""
Calendar Event Generator
-----------------------

This script generates random calendar events and saves them as an .ics file that can be imported
into any calendar application (Apple Calendar, Google Calendar, Outlook, etc.).

Dependencies:
    - Python 3.6+
    - icalendar library (install with: pip install icalendar)

To run:
    1. Install dependencies:
       pip install icalendar

    2. Run the script:
       python calendar_generator.py

    3. Find the generated 'random_events.ics' file in your Downloads folder
    
    4. Import the .ics file into your calendar application:
       - Apple Calendar: File -> Import
       - Google Calendar: Settings -> Import & Export -> Import
       - Outlook: File -> Import/Export -> Import an iCalendar file

Features:
    - Generates 1-4 events per weekday (weighted random distribution)
    - Includes one "Focus Time" block per day
    - Avoids scheduling conflicts
    - Skips weekends
    - Sets 15-minute reminders for all events
    - Creates events only during business hours (9 AM - 5 PM)
    - Varies meeting durations between 30-90 minutes
    - Customizable meeting subjects (edit the list in get_random_name() function)

Author: [Your name here]
Date: [Current date]
"""

from datetime import datetime, timedelta
import random
from icalendar import Calendar, Event
import uuid
import os
from pathlib import Path

def create_calendar_event(calendar, subject, start_time, end_time):
    """Create a calendar event and add it to the calendar."""
    event = Event()
    event.add('summary', subject)
    event.add('dtstart', start_time)
    event.add('dtend', end_time)
    
    # Add reminder (15 minutes before)
    from icalendar import Alarm
    alarm = Alarm()
    alarm.add('action', 'DISPLAY')
    alarm.add('trigger', timedelta(minutes=-15))
    alarm.add('description', subject)
    event.add_component(alarm)
    
    # Add unique identifier
    event['uid'] = str(uuid.uuid4())
    
    # Add status and transparency
    event.add('status', 'CONFIRMED')
    event.add('transp', 'OPAQUE')  # Marks as busy
    
    calendar.add_component(event)
    print(f"Event created: {subject} from {start_time} to {end_time}")

def get_random_name():
    """Generate a random meeting subject."""
    subjects = [
        "Project Review", "Client Follow-Up", "Performance Update",
        "Strategic Planning", "Budget Discussion", "Sprint Retrospective",
        "Operational Review", "Focus Time", "Priority Planning",
        "KPI Review", "Status Update", "Market Analysis",
        "Content Review", "Department Check-In", "Stakeholder Meeting",
        "Report Drafting", "Goal Setting", "Next Steps Planning",
        "Annual Planning", "Feedback Session", "Weekly Review",
        "Risk Management", "Results Presentation", "Roadmap Planning"
    ]
    return random.choice(subjects)

def get_random_events_count():
    """Generate a random number of events for a day."""
    # Weights for number of daily events:
    # 1 event:  10% chance
    # 2 events: 45% chance
    # 3 events: 25% chance
    # 4 events: 20% chance
    weights = [10, 45, 25, 20]  # Weights for 1-4 events
    return random.choices(range(1, 5), weights=weights)[0]

def check_for_conflicts(events, start_time, end_time):
    """Check if there are any conflicts with existing events."""
    for event in events:
        event_start = event.get('dtstart').dt
        event_end = event.get('dtend').dt
        if (start_time < event_end and end_time > event_start):
            return True
    return False

def generate_random_events(days=5):
    """Generate random calendar events for the specified number of days."""
    # Create a new calendar
    cal = Calendar()
    cal.add('prodid', '-//Random Calendar Generator//example.com//')
    cal.add('version', '2.0')
    
    # Keep track of all events for conflict checking
    all_events = []
    
    now = datetime.now()
    now = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    for i in range(days):
        day_date = now + timedelta(days=i)
        
        # Skip weekends
        if day_date.strftime('%A') in ['Saturday', 'Sunday']:
            continue
            
        # Randomly determine number of events for this day
        events_for_today = get_random_events_count()
        print(f"\nGenerating {events_for_today} events for {day_date.strftime('%A, %B %d')}")
        
        generated_events = 0
        focus_time_created = False
        attempts = 0  # Add a maximum attempts counter to prevent infinite loops
        
        while generated_events < events_for_today and attempts < 50:  # Limit attempts
            attempts += 1
            
            # Randomly choose morning or afternoon
            if random.choice(['Morning', 'Afternoon']) == 'Morning':
                start_hour = random.randint(9, 11)  # Extended morning hours
            else:
                start_hour = random.randint(13, 16)  # Extended afternoon hours
                
            start_minute = random.choice([0, 15, 30, 45])
            duration = random.randint(30, 90)  # More flexible duration
            
            # Create datetime objects for start and end times
            start_time = day_date.replace(hour=start_hour, minute=start_minute)
            end_time = start_time + timedelta(minutes=duration)
            
            # Check if the meeting would end after 5 PM
            if end_time.hour >= 17:
                continue
            
            if not check_for_conflicts(all_events, start_time, end_time):
                # Determine subject (ensure one Focus Time per day)
                if not focus_time_created:
                    subject = "Focus Time"
                    focus_time_created = True
                else:
                    subject = get_random_name()
                
                # Create the event
                event = Event()
                event.add('summary', subject)
                event.add('dtstart', start_time)
                event.add('dtend', end_time)
                event['uid'] = str(uuid.uuid4())
                
                all_events.append(event)
                create_calendar_event(cal, subject, start_time, end_time)
                generated_events += 1
    
    # Save to file
    output_dir = Path.home() / "Downloads"
    output_file = output_dir / "random_events.ics"
    
    with open(output_file, 'wb') as f:
        f.write(cal.to_ical())
    
    print(f"\nCalendar file has been created at: {output_file}")
    print("You can import this file into Apple Calendar or any other calendar application.")

if __name__ == "__main__":
    try:
        generate_random_events()
        print("Calendar events generation completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
