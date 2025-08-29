import pickle
import streamlit as st
import requests

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a57abea40dd1c2f148ad32e43b10e3fc&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    full_poster = "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
    
    details = {
        "title": data.get("title", "Unknown"),
        "overview": data.get("overview", "No overview available."),
        "release_date": data.get("release_date", "Unknown"),
        "rating": data.get("vote_average", "N/A"),
        "poster": full_poster,
        "runtime": data.get("runtime", "N/A"),
        "genres": ", ".join([g['name'] for g in data.get('genres', [])])
    }
    return details

def recommend(movie, top_n=50):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    
    for i in distances[1:top_n+1]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(fetch_movie_details(movie_id))
    
    return recommended_movies

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header('🎬 Movie Recommender System')

movies = pickle.load(open('model/movie-list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity_list.pkl', 'rb'))
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movies = recommend(selected_movie, top_n=50) 
    num_cols = 5
    for i in range(0, len(recommended_movies), num_cols):
        cols = st.columns(num_cols)
        for j, movie in enumerate(recommended_movies[i:i+num_cols]):
            with cols[j]:
                with st.expander(movie['title']):
                    st.image(movie['poster'], use_container_width=True)
                    st.write(f"**Release Date:** {movie['release_date']}")
                    st.write(f"**Rating:** {movie['rating']}")
                    st.write(f"**Runtime:** {movie['runtime']} minutes")
                    st.write(f"**Genres:** {movie['genres']}")
                    st.write(f"**Overview:** {movie['overview']}")
