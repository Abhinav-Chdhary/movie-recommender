import streamlit as st
import joblib
import pandas as pd
import json
import requests

with open("config.json") as config_file:
    config = json.load(config_file)
API_KEY = config["api-key"]


# get movie poster
def fetch_poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key={}".format(movie_id, API_KEY)
    )
    data = response.json()
    # print(data)
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]


# get recommendation
def recommend(movie):
    movie_index = movies_df[movies_df["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:6
    ]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        recommended_movies.append(movies_df.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movies_df.iloc[i[0]].id))

    return recommended_movies, recommended_movies_poster


movies_df = joblib.load("movies.joblib")

movies_list = movies_df["title"].tolist()

similarity = joblib.load("similarity.joblib")

st.title("Movie Recommender System")

selected_movie_name = st.selectbox("Enter a movie you have watched:", (movies_list))
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    col = st.columns(5)
    for i in range(0, 5):
        with col[i]:
            st.write(names[i])
            st.image(posters[i])
