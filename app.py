import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=09200b14fb134d63aa5cf9f27af15124&language=en-US'
    response = requests.get(url)
    data = response.json()

    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"



def recommend(movie):
    if movie not in movies['title'].values:
        return [], [], None  # Return empty lists and None for the poster

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Ensure 'movie_id' column exists
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    searched_movie_id = movies.iloc[movie_index].movie_id
    searched_movie_poster = fetch_poster(searched_movie_id)

    return recommended_movies, recommended_movies_posters, searched_movie_poster



movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


similarity = pickle.load(open('similarity.pkl', 'rb'))


st.title(' 🎥Movie Recommendation System🎬')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters, searched_poster = recommend(selected_movie_name)

    if searched_poster:

        st.image(searched_poster, caption=selected_movie_name, use_column_width=True)

    if names:
        st.subheader("Recommended Movies")
        cols = st.columns(5)
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.text(name)
                st.image(poster)
    else:
        st.error("No recommendations found. Try another movie.")
