import datetime
import pytz
import subprocess
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Define your schedule
schedule = [
    {"name": "AWS Course", "start": "06:00", "end": "08:00", "color": "blue"},
    {"name": "Java Practice", "start": "08:00", "end": "10:00", "color": "green"},
    {"name": "Content Automation", "start": "10:00", "end": "11:00", "color": "purple"},
    {"name": "Management", "start": "11:00", "end": "12:30", "color": "red"},
    {"name": "Break", "start": "12:30", "end": "13:30", "color": None},
    {"name": "AWS Course", "start": "13:30", "end": "15:30", "color": "blue"},
    {"name": "Java Practice", "start": "15:30", "end": "16:30", "color": "green"},
    {"name": "Break", "start": "16:30", "end": "18:00", "color": "orange"},
    {"name": "Relax/Unwind", "start": "18:00", "end": "19:00", "color": None},
]

# Authenticate and authorize
SCOPES = ['https://www.googleapis.com/auth/calendar']
#flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES,
    redirect_uri="http://localhost:9090/"
)


print("Redirect URI:", flow.redirect_uri)

creds = flow.run_local_server(port=9090)

# Build the service
service = build('calendar', 'v3', credentials=creds)

# Add events to Google Calendar
calendar_id = 'primary'  # Use 'primary' for your main calendar
timezone = 'Europe/Warsaw'  # Change to your timezone

color_mapping = {
    "blue": "1",
    "green": "2",
    "purple": "6",
    "red": "4",
    "orange": "5",
}

for task in schedule:
    start_time = datetime.datetime.strptime(task["start"], "%H:%M").time()
    end_time = datetime.datetime.strptime(task["end"], "%H:%M").time()

    event = {
        'summary': task["name"],
        'start': {
            'dateTime': datetime.datetime.combine(datetime.date.today(), start_time).isoformat(),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': datetime.datetime.combine(datetime.date.today(), end_time).isoformat(),
            'timeZone': timezone,
        },
        'recurrence': [
            'RRULE:FREQ=DAILY'  # Repeat daily
        ],
    }

    # Set colorId only if a valid color is provided
    if task["color"]:
        event["colorId"] = color_mapping.get(task["color"], "1")  # Default to blue

    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')
