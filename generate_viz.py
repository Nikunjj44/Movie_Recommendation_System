import requests
import base64
import json
import streamlit as st
from config import REQ_URL, CONFIG_KEY, IMAGE_URL, MOVIE_DATA_PATH, BASE_URL

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


def get_base64_image(image_path):
    # converting image into base64 form
    
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

@st.cache_data(show_spinner=False)
def get_cast_data_w_img(movie_title):
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
            movie_id = data["results"][0]["id"]
            url = f"{BASE_URL}/movie/{movie_id}/credits"

            params = {"api_key":CONFIG_KEY}
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                config_data = response.json()["cast"]
                n = len(config_data)
                if n > 10:
                    n = 10
                actor_name = []
                char_name = []
                cast_img = []
                for i in range(n):
                    # only keeping cast which have movie alias
                    if config_data[i]["character"] and config_data[i]["name"]:
                        actor_name.append(config_data[i]["name"])
                        char_name.append(config_data[i]["character"])

                        if config_data[i]["profile_path"]:
                            profile_path = config_data[i]["profile_path"]
                            cast_img.append(f"{IMAGE_URL}{profile_path}")
                        else:
                            # if no profile pic found - assign default image based on gender
                            if config_data[i]["gender"] == 2:
                                PLACEHOLDER_IMAGE = get_base64_image("data/no_profile_man.png")
                            else:
                                PLACEHOLDER_IMAGE = get_base64_image("data/no_profile_female.png")
                            cast_img.append(f"data:image/png;base64,{PLACEHOLDER_IMAGE}")

                    else:
                        pass
                
                cast_info = {
                    "actors" : actor_name,
                    "characters" : char_name,
                    "cast_img_links" : cast_img,
                    "total_cast_members" : n
                }

                return cast_info
                            
            else:
                print("Error extracting cast details from api")
                return None
    else:
        print("Error extracting cast details from api")
        return None