import streamlit as st
import pandas as pd
import pickle
import warnings
from config import *
from generate_viz import get_poster_url, get_movie_summary, get_genre_list, get_cast_data_w_img

warnings.filterwarnings("ignore")

st.set_page_config(page_title = "Movie Recommendation System")

# custom content width - default in page config para is "centered" = 730px
st.markdown("""
    <style>
    .block-container {
        max-width: 1000px;
        padding: 3rem 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# functions to load req. data + perform req. pre-processing
@st.cache_data
def load_data():
    try:
        with open("data/movies_data.pkl", "rb") as file:
            df = pickle.load(file)

        with open("data/similarity_matrix.pkl", "rb") as file:
            similarity = pickle.load(file)

        return df, similarity
    except Exception as e:
        st.error("Unable to load required data files!!")
        st.stop()

def sort_movie_list(movie_list):
    result = []
    num_movie = []
    for i in sorted(movie_list):
        if i[0].isalpha():
            result.append(i)
        else:
            num_movie.append(i)
    
    return result + num_movie

# Func. to get recommendations and respective scores
def make_recommendation(movie_title, df, similarity_scores, n = 10):
    
    try:
        # making sure we have ordered index
        df = df.reset_index()
        
        # finding the index of the movie
        try:
            index = df[df["title"] == movie_title].index[0]
        except Exception as e:
            print(f"Incorrect movie name! Movie {movie_title} not present in dataset.")
            return None

        # extracting the similarity score with the above extracted index (for the ip movie)
        # creating a sorted list of scores
        
        scores = list(enumerate(similarity_scores[index]))

        # here key argument referes to which value of the enumerated key do you want to sort on
        scores = sorted(scores, reverse = True, key = lambda x: x[1])

        # extracting top n+1 values
        # +1 because it will include the movie itself
        scores = scores[:n+1]

        titles = []
        rec_score = []
        for i in scores:
            if df["title"][i[0]] != movie_title:
                titles.append(df['title'][i[0]])
                rec_score.append(i[1])
        
        return {"movies" : titles, "scores" : rec_score}

    except:
        st.error("Failed to make recommendatios")

st.markdown("""
    <style>
    .pill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .pill-button {
        display: inline-block;
        padding: 4px 12px;
        border: 1px solid #ccc;
        border-radius: 25px;
        background-color: white;
        color: #333;
        text-decoration: none;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .pill-button:hover {
        background-color: #f0f0f0;
        border-color: #999;
    }
    </style>
    """, unsafe_allow_html=True
)

# st.markdown("""
#     <style>
#     .stTextArea {
#         margin-top: -10px;
#     }
#     </style>
#     """, unsafe_allow_html=True)
def get_display_data(df):
    poster = []
    summary = []
    genres = []
    cast_data = []
    movies = []

    for i in st.session_state["rec_movies"]:
        poster.append(get_poster_url(i))
        summary.append(get_movie_summary(i, df))
        genres.append(get_genre_list(i, df))
        cast_data.append(get_cast_data_w_img(i))
        movies.append(i)
    
    return {
        "posters" : poster,
        "overview" : summary,
        "genres" : genres,
        "casts" : cast_data,
        "movie_name" : movies
    }

def display_cast(cast_data):

    st.markdown("""
        <style>
        /* Your existing CSS... */
        
        /* Scrollable cast container */
        .cast-scroll-container {
            display: flex;
            overflow-x: auto;
            gap: 1rem;
            padding: 1rem;
            scroll-behavior: smooth;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
        }
        
        .cast-scroll-container::-webkit-scrollbar {
            height: 8px;
        }
        
        .cast-scroll-container::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.3);
            border-radius: 10px;
        }
        
        .cast-card {
            min-width: 120px;
            text-align: center;
            flex-shrink: 0;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .cast-card:hover {
            transform: scale(1.05);
        }
        
        .cast-image {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid rgba(255,255,255,0.3);
        }
        
        .cast-name {
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 0.5rem;
            color: white;
        }
        
        .cast-character {
            font-size: 0.75rem;
            color: rgba(255,255,255,0.7);
            font-style: italic;
        }
        </style>
    """, unsafe_allow_html=True)
    
    cast_html = '<div class="cast-scroll-container">'

    for i in range(len(cast_data["actors"])):
        name = cast_data["actors"][i]
        character = cast_data["characters"][i]
        img_url = cast_data["cast_img_links"][i]
        
        if img_url == "NA":
            img_url = "https://via.placeholder.com/100x100/667eea/ffffff?text=No+Image"

        cast_html += f'<div class="cast-card"><img src="{img_url}" class="cast-image" alt="{name}"><div class="cast-name">{name}</div><div class="cast-character">{character}</div></div>'
    
    cast_html += '</div>'
    st.markdown(cast_html, unsafe_allow_html=True)


def display_recommendations(disp_data):
    try:
        st.subheader("You may like these movies 🤔")

        for i in range(len(disp_data["movie_name"])):
            poster, details = st.columns([2, 4])
            
            img_url = disp_data["posters"][i]
            overview = disp_data["overview"][i]
            genres = disp_data["genres"][i]
            movie_name = disp_data["movie_name"][i]
            cast = disp_data["casts"][i]

            with poster:
                st.image(img_url, width = 300)
            
            with details:
                st.markdown(f"#### {movie_name}")
                st.text_area(value = overview, label = "Overview", height = 100, label_visibility="collapsed")

                # displaying genres
                pills_html = '<div class="pill-container">'
                for category in sorted(genres):
                    pills_html += f'<span class="pill-button">{category}</span>'
                pills_html += '</div>'

                st.markdown(pills_html, unsafe_allow_html=True)

                display_cast(cast)

    except Exception as e:
        print(e)

def main():
    
    # UI for inputs
    st.title("Movie Recommendation System")
    st.subheader("Find your next movie to bingewatch 😁")

    # Loading req. data
    with st.spinner("Loading movies data ..."):
        df, similarity = load_data()
        df_movies = pd.read_csv(MOVIE_DATA_PATH)
        movie_list = sort_movie_list(df["title"].to_list())

    # Inputs 
    ddn, slider = st.columns([4, 2])
    
    with ddn:
        selected_title = st.selectbox(
            label = "Select a movie you like: ",
            options = movie_list,
            placeholder = None,
            accept_new_options = False
        )
    
    with slider:
        selected_num_rec = st.slider(
            label = "How many recommendations would you like ?",
            min_value = 5,
            max_value = 15,
            value = 10
        )
    # Generating outputs
    if st.button("Generate Recommendations"):
        try:
            recommendations = make_recommendation(
                movie_title = selected_title,
                df = df,
                similarity_scores = similarity,
                n = selected_num_rec
            )
            
            st.session_state["rec_movies"] = recommendations["movies"]
            st.session_state["rec_Scores"] = recommendations["scores"]
            
            with st.spinner("Loading Recommendations ..."):
                display_data = get_display_data(df_movies)
                st.session_state["display_data"] = display_data

        except Exception as e:
            st.error(e)

    if st.session_state["display_data"] is not None:
        display_recommendations(st.session_state["display_data"])


if __name__ == "__main__":
    # Initialize
    # st.session_state["display_data"] = None
    if "display_data" not in st.session_state:
        st.session_state.display_data = None

    main()