# Movie Recommendation System
This project implements a movie recommendation system that analyzes movie metadata to provide personalized recommendations. Using content-based filtering techniques, the system suggests movies that are similar to a given movie based on various features such as genres, keywords, cast, crew, and plot summaries.

## Methodology
1. Dataset Used -- TMDB 5000 Movies Dataset -- https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
2. Data pre-processing:  
     a) Exploring Movies and Credits data to identify key features for recommendation system.  
     b) Merging and removing duplicates from identified features.  
     c) Transforming -- genres, keywords, cast and crew columns -- such that each row gets a list of processed values. For eg: After processing genre column, each movie gets a list of genres associated with it in the genre column like ["Action", "SciFi"].  
     d) Genrating a single tags column from the above mentioned columns.  
     e) Applying Porter Stemmer - to reduce similar words and provide consistency.  
3. Creating recommendation system using **TV-IVF Vectorizer and Cosine Similarity**  
     a) The vectorizer consists of two components:  
          - **Term Frequency (TF):** Measures how often a word appears in a specific document.  
          - **Inverse Document Frequency (IDF):** Measures how rare the word is across all documents in the corpus. The rarer the word, the higher its score.  
     b) **Cosine Similarity** is used to get similarity scores which are calculated based on the angles of the above represented vectors.  
4. Saving required files
   **Note: the above mentioned 4 steps are presented in file -- "Movie Rec.ipynb"**  
5. Building Streamlit App

## Streamlit Application
### Landing Page

<img width="972" height="281" alt="landing_page" src="https://github.com/user-attachments/assets/be517d9f-7fc4-4548-9dbc-d2f271848ef8" />

### Generated Recommendations 

<img width="780" height="880" alt="sample_recs" src="https://github.com/user-attachments/assets/df60b126-967e-4120-bae1-1de29f065d8a" />

### Apllication Link -- Try it out 😄
https://movie-recommendation-system-nm.streamlit.app
