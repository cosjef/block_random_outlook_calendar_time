# Random Outlook Calendar Time Blocker

A Python script that generates random calendar events and saves them as an .ics file, which can be imported into any calendar application (Apple Calendar, Google Calendar, Outlook, etc.). The script creates realistic-looking calendar blocks with proper distribution of meetings and focus time throughout the work week.

## Features

- Generates 1-4 events per weekday with weighted distribution:
  - 1 event: 10% chance
  - 2 events: 45% chance
  - 3 events: 25% chance
  - 4 events: 20% chance
- Ensures one "Focus Time" block per day
- Automatically avoids scheduling conflicts
- Skips weekends
- Sets 15-minute reminders for all events
- Creates events only during business hours (9 AM - 5 PM)
- Varies meeting durations between 30-90 minutes
- Includes diverse meeting subjects (e.g., "Project Review", "Sprint Retrospective", etc.)
- Saves events in standard .ics format compatible with all major calendar applications

## Prerequisites

- Python 3.6 or higher
- `icalendar` library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cosjef/block_random_outlook_calendar_time
cd block_random_outlook_calendar_time
```

2. Install the required dependency:
```bash
pip install icalendar
```

## Usage

1. Run the script:
```bash
python calendar-generator-mac-random.py
```

2. The script will generate a `random_events.ics` file in your Downloads folder

3. Import the .ics file into your preferred calendar application:
   - Apple Calendar: File -> Import
   - Google Calendar: Settings -> Import & Export -> Import
   - Outlook: File -> Import/Export -> Import an iCalendar file

## Customization

### Meeting Subjects
Edit the `get_random_name()` function to customize the list of possible meeting subjects. The current list includes:
- Project Review
- Client Follow-Up
- Performance Update
- Strategic Planning
- And many more...

### Time Slots
- Morning slots: 9 AM - 11 AM
- Afternoon slots: 1 PM - 4 PM
- Meeting duration: 30-90 minutes

### Event Distribution
Modify the weights in `get_random_events_count()` to adjust the probability distribution of daily events.

## Output

The script generates an .ics file containing:
- Randomly distributed events across workdays
- One Focus Time block per day
- 15-minute reminders for each event
- Busy status for all events
- Unique identifiers for each event

## Error Handling

The script includes:
- Conflict prevention for overlapping events
- Maximum attempts limit to prevent infinite loops
- Basic error reporting for failed operations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- `icalendar` library for Python
- Calendar standardization efforts (iCalendar format)
```
