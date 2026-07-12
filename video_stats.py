import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
API_key = os.getenv("API_key") # API_key = "AIzaSyDVje6xM_1vOlUXl5sE-MHioAyBa4p1kIE" important to keep it secret, so I will use .env file to store it
Channel_ID = "tseries"

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

    except Exception as e:
        print(f"Error occurred: {e}")
if __name__ == "__main__":
    get_playlist_id()
