import streamlit as st
import pickle

# Load data
movies = pickle.load(open("movies_list.pkl", "rb"))  # Must include 'video_id', 'video_type', 'music_type', 'tag'
similarity = pickle.load(open("similarity.pkl", "rb"))

# Convert video_id to string for dropdown display
movies_list = movies['video_id'].astype(str).values

# App title
st.header("🎵 Movie Recommender System (Text Info Only)")

# Dropdown for selecting a movie by video_id
selected_video_id = st.selectbox("🔽 Select a video ID", movies_list)

# Recommendation function based on video_id
def recommend(video_id):
    index = movies[movies['video_id'] == int(video_id)].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended = []
    for i in distances[1:6]:
        row = movies.iloc[i[0]]
        info = {
            "video_id": row["video_id"],
            "video_type": row.get("video_type", ""),
            "music_type": row.get("music_type", ""),
            "tag": row.get("tag", "")
        }
        recommended.append(info)
    
    return recommended

# Display recommendations
if st.button("🔍 Show Recommendations"):
    recommendations = recommend(selected_video_id)
    
    for i, rec in enumerate(recommendations):
        st.markdown(f"### 🎬 Recommendation {i+1}")
        st.write(f"**Video ID:** {rec['video_id']}")
        
        st.write(f"**Video Type:** {rec['video_type']}")
        st.write(f"**Music Type:** {rec['music_type']}")
        st.write(f"**Tag:** {rec['tag']}")
        st.markdown("---")
