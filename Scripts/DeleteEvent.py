import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Authenticate and authorize
SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES,
    redirect_uri="http://localhost:9090/"
)
creds = flow.run_local_server(port=9090)

# Build the service
service = build('calendar', 'v3', credentials=creds)

calendar_id = 'primary'  # Your main calendar
timezone = 'Europe/Warsaw'  # Change to your timezone

# Get today's date
today = datetime.datetime.utcnow().date()

# Get events for today
events_result = service.events().list(
    calendarId=calendar_id,
    timeMin=f"{today}T00:00:00Z",
    timeMax=f"{today}T23:59:59Z",
    singleEvents=True,
    orderBy="startTime"
).execute()

events = events_result.get("items", [])

# Find duplicate events
event_map = {}
duplicate_events = []

for event in events:
    key = (event["summary"], event["start"]["dateTime"], event["end"]["dateTime"])
    if key in event_map:
        duplicate_events.append(event["id"])  # Store duplicate event IDs
    else:
        event_map[key] = event["id"]  # Store first occurrence

# Delete duplicate events
for event_id in duplicate_events:
    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
    print(f"Deleted duplicate event: {event_id}")

print("Duplicate cleanup complete!")
