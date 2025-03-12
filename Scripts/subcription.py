from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

# Authenticate and get credentials
flow = InstalledAppFlow.from_client_secrets_file("youtubecred.json", SCOPES)
creds = flow.run_local_server(port=9091)

# Build the YouTube API service
youtube = build("youtube", "v3", credentials=creds)

# Fetch the list of subscribers (You cannot get members this way)
subscribers = []
next_page_token = None

while True:
    request = youtube.subscriptions().list(
        part="snippet",
        mine=True,  # 'mine' means the authenticated user's channel
        maxResults=50,  # Max number of results per request
        pageToken=next_page_token
    )
    response = request.execute()

    subscribers.extend(response.get("items", []))
    next_page_token = response.get("nextPageToken")
    if not next_page_token:
        break  # Exit the loop if there are no more pages

# Print the subscriber's name or other details
print(f"Total Subscribers: {len(subscribers)}")
for subscriber in subscribers:
    print(subscriber["snippet"]["title"])  # Subscriber name

# import os





# import google.auth
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
#
# # YouTube API scopes
# SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
#
# # Authentication flow to get user credentials
# def authenticate():
#     """Authenticate and return the service object"""
#     flow = InstalledAppFlow.from_client_secrets_file(
#         'youtubecred.json', SCOPES)
# #    creds = flow.run_local_server(port=0)
#     creds = flow.run_local_server(port=9091)
#     service = build('youtube', 'v3', credentials=creds)
#     return service
#
# # Get a list of subscribers
# def get_subscribers(service, channel_id):
#     """Fetch and print the list of subscribers for a given channel"""
#     request = service.subscriptions().list(
#         part="snippet",
#         channelId=channel_id,
#         maxResults=50  # You can adjust this number for pagination
#     )
#     response = request.execute()
#
#     subscribers = []
#     while request is not None:
#         # Append subscribers from the current page
#         for item in response['items']:
#             subscribers.append(item['snippet']['title'])
#
#         # If there are more pages, get the next page of results
#         request = service.subscriptions().list_next(request, response)
#         if request is not None:
#             response = request.execute()
#
#     return subscribers
#
# def main():
#     # Authenticate and get the YouTube service
#     service = authenticate()
#
#     # Replace this with your YouTube channel ID
#     channel_id = 'UCd7VirXIqZJxpYlsLozQiWg'  # Example channel ID for Google Developers
#
#     # Get the list of subscribers
#     subscribers = get_subscribers(service, channel_id)
#
#     # Print out the subscriber list
#     if subscribers:
#         print(f"Subscribers to channel {channel_id}:")
#         for subscriber in subscribers:
#             print(subscriber)
#     else:
#         print(f"No subscribers found or the channel has no public subscribers.")
#
# if __name__ == "__main__":
#     main()
