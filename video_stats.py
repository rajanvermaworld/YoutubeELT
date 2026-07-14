import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
API_key = os.getenv("API_key") # important to keep it secret, so I will use .env file to store it
Channel_ID = "ApnaCollegeOfficial"
maxResults = 50

def get_playlist_id():
    try:

        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={Channel_ID}&key={API_key}"

        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        # print(response)
        # print(data)
        # print(json.dumps(data, indent=4))

        channel_items = data["items"][0]
        channel_playlist_id = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlist_id)
        return channel_playlist_id

    except Exception as e:
        print(f"Error occurred: {e}")

def get_video_ids(playlistId):
    
    video_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_key}"

    try: 

        while True:

            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
                
            response = requests.get(url)
            response.raise_for_status()  
            data = response.json()
            for item in data.get("items", []):     
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)

            pageToken = data.get("nextPageToken")
            if not pageToken:
                break
        return video_ids
    
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    playlistId = get_playlist_id()
    print(get_video_ids(playlistId)) 