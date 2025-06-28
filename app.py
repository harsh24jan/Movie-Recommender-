import streamlit as st
import pickle
import pandas as pd
import requests

# Set your TMDB API Key
TMDB_API_KEY = "39ea8c5b4d9fddea496881df4b4071e0"

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))  # Assumes 'original_title' and 'id' columns
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to fetch movie poster using TMDB API
def fetch_poster(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        if "poster_path" in data and data["poster_path"]:
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
        else:
            return "https://via.placeholder.com/500x750.png?text=No+Image"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for TMDB ID {tmdb_id}: {e}")
        return "https://via.placeholder.com/500x750.png?text=No+Image"

# Function to recommend movies
def recommend(movie):
    index = movies[movies['original_title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_data = movies.iloc[i[0]]
        tmdb_id = movie_data.id  # Ensure this column is valid
        recommended_movies.append(movie_data.original_title)
        recommended_posters.append(fetch_poster(tmdb_id))

    return recommended_movies, recommended_posters

# Streamlit App UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Choose a movie", movies['original_title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    st.write("### Top 5 Recommended Movies for You")
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])
