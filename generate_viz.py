import requests
import pandas as pd
import json
from config import REQ_URL, CONFIG_KEY, IMAGE_URL, MOVIE_DATA_PATH

def get_poster_url(movie_title):

    params = {
        "api_key": CONFIG_KEY,
        "query": movie_title,
        "language": "en-US"
    }

    response = requests.get(REQ_URL, params=params, timeout=5)

    # progress only if successful api req
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            sub_url = data["results"][0]["poster_path"]
            poster_url = IMAGE_URL + sub_url

            return poster_url
    else:
        print("Error creating movie poster url")
        return None
    
def get_movie_summary(movie_title, df):
    
    summary = df[df["title"] == movie_title].reset_index()["overview"][0]

    return summary

def get_genre_list(movie_title, df):
    
    genre_val = df[df["title"] == movie_title].reset_index()["genres"][0]

    result = []
    list = json.loads(genre_val)
    for i in list:
        result.append(i["name"])

    return result