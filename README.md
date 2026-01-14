# Movie Recommendation System
This project implements a movie recommendation system that analyzes movie metadata to provide personalized recommendations. Using content-based filtering techniques, the system suggests movies that are similar to a given movie based on various features such as genres, keywords, cast, crew, and plot summaries.

## TechStack Used

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-4B8BBE?style=for-the-badge&logo=text&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

## Methodology
1. Dataset Used -- TMDB 5000 Movies Dataset -- https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
2. Data pre-processing:  
     a) Exploring Movies and Credits data to identify key features for recommendation system.  
     b) Merging and removing duplicates from identified features.  
     c) Transforming -- genres, keywords, cast and crew columns -- such that each row gets a list of processed values. For eg: After processing genre column, each movie gets a list of genres associated with it in the genre column like ["Action", "SciFi"].  
     d) Genrating a single tags column from the above mentioned columns.  
     e) Applying Porter Stemmer - to reduce similar words and provide consistency.  
3. Creating recommendation system using **TV-IVF Vectorizer and Cosine Similarity**  
     a) The vectorizer consists of two components and TF-IDF is a product of these two components:  
          - **Term Frequency (TF):** Measures how often a word appears in a specific document.  
          - **Inverse Document Frequency (IDF):** Measures how rare the word is across all documents in the corpus. The rarer the word, the higher its score.  
        Therefore, TF-IDF is a product of the above two components.  
     b) **Cosine Similarity** is used to get similarity scores which are calculated based on the angles of the above represented vectors.  
5. Saving required files  
   **Note: the above mentioned 4 steps are presented in file -- "Movie Rec.ipynb"**  
6. Building Streamlit App

## Streamlit Application
### Landing Page

<img width="972" height="281" alt="landing_page" src="https://github.com/user-attachments/assets/be517d9f-7fc4-4548-9dbc-d2f271848ef8" />

### Some Generated Recommendations (a total of 10 recommendations will be dispayed as per the slider)

<img width="780" height="880" alt="sample_recs" src="https://github.com/user-attachments/assets/df60b126-967e-4120-bae1-1de29f065d8a" />

### Application Link -- Try it out 😄
https://movie-recommendation-system-nm.streamlit.app

## Future Scope

Currenly the application is based on the TMDB 5000 dataset thus having a limited number of movies. This can further be improved by either using a larger dataset or incorporating an API to get data. The API method would be more relevant as it would also include recently released movies thereby keeping the application upto date. Another improvement that can be made is in the way recommendation is made. Currently, we use TF-IDF which treats all terms equally. So we can incorporate a special weighted mechanism that would give a set of terms more weight than others. These terms with higher weight than others would include cast, directors and genres.  

Furthermore, we can have some additional enhancements while displaying the final recommendations like:  
1. Including list of directors in a similar way the cast is presented.
2. Incorporating movie ratings and reviews in order to help the end user make a decision on what movie they want to watch next.

