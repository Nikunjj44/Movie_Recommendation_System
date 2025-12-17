import streamlit as st
import pandas as pd
import pickle
import os

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

def make_recommendation(movie_title, df, similarity_scores, n = 10):
    
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

    print("Movie Recommendations:")
    print("--"*40)

    # extracting top n+1 values
    # +1 because it will include the movie itself
    scores = scores[:n+1]
    num = 1
    for i in scores:
        if df["title"][i[0]] != movie_title:
            print(f"Recommendation {num}: {df['title'][i[0]]}")
            print(f"Similarity Score : {round(i[1], 2)}")
            num += 1
    

def main():
    st.title("Movie Recommendation System")
    st.subheader("Find your next movie to bingewatch 😁")

    with st.spinner("Loading movies data ..."):
        df, similarity = load_data()
        movie_list = sort_movie_list(df["title"].to_list())

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

    if st.button("Generate Recommendations"):
        print(selected_title)
        print(selected_num_rec)


if __name__ == "__main__":
    main()