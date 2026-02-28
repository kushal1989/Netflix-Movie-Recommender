import streamlit as st
import pandas as pd
import joblib

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Netflix Recommender",
    page_icon="🎬",
    layout="wide"
)

# ---------- LOAD DATA ----------
similarity = joblib.load('model.pkl')
df = pd.read_csv('tmdbdf.csv').head(5000)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {
    background-color: #0E1117;
}

/* Title */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #E50914;
    margin-bottom: 5px;
}

/* Subtitle */
.sub-text {
    text-align: center;
    color: #b3b3b3;
    margin-bottom: 30px;
}

/* Movie Card */
.movie-card {
    padding: 10px;
    border-radius: 15px;
    background-color: #1c1f26;
    text-align: center;
    transition: transform 0.3s, box-shadow 0.3s;
}

.movie-card:hover {
    transform: scale(1.05);
    box-shadow: 0px 4px 20px rgba(255,255,255,0.2);
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="main-title">🎬 Netflix Movie Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Find movies similar to your favorites 🍿</div>', unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.header("🎯 Choose Movie")
movie_name = st.sidebar.selectbox("Select a movie", df['title'].values)

# ---------- RECOMMEND FUNCTION ----------
def recommend(movie):
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names = []
    posters = []

    for i in movie_list:
        names.append(df.iloc[i[0]].title)

        poster = df.iloc[i[0]]['poster_path']
        if pd.notnull(poster):
            posters.append("https://image.tmdb.org/t/p/w500/" + poster)
        else:
            posters.append("https://via.placeholder.com/500x750?text=No+Poster")

    return names, posters

# ---------- BUTTON ----------
if st.sidebar.button("🎥 Recommend"):
    names, posters = recommend(movie_name)

    st.subheader("✨ Recommended Movies")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            st.image(posters[i], use_container_width=True)  # ✅ FIXED
            st.markdown(
                f"<h5 style='text-align:center; color:white'>{names[i]}</h5>",
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)