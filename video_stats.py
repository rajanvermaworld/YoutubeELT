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



def get_video_data(video_ids):
    get_data = []

    def batch_list(video_id_list, batch_size):
        for video_id in range (0, len(video_id_list), batch_size):
            yield video_id_list[video_id : video_id + batch_size]

    try:
        for batch in batch_list(video_ids, maxResults):
            videos_ids_str = ",".join(batch)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={videos_ids_str}&key={API_key}"
            response = requests.get(url)
            response.raise_for_status()  
            data = response.json()

            for items in data.get("items", []):
                video_id =items['id']
                snippet = items['snippet']
                contentDetails = items['contentDetails']
                statistics = items['statistics']

                video_data = {
                    "video_id":video_id,
                    "title":snippet['title'],
                    "publishedAt":snippet['publishedAt'],
                    "duration":contentDetails['duration'],
                    "viewCount":statistics.get('viewCount',None),
                    "likeCount":statistics.get('likeCount', None),
                    "commentCount":statistics.get('commentCount', None),
                }               
                get_data.append(video_data)
        return get_data
    
    except Exception as e:
        print(f"Error occurred: {e}")



if __name__ == "__main__":
    playlistId = get_playlist_id()
    video_ids = (get_video_ids(playlistId)) 
    print(get_video_data(video_ids))