# FastAPI endpoint to replace Streamlit's button logic
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

@app.get("/recommend")
def recommend(video_id: int):
    index = movies[movies['video_id'] == video_id].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended = []
    for i in distances[1:6]:
        row = movies.iloc[i[0]]
        recommended.append({
            "video_id": int(row["video_id"]),
            "video_type": row.get("video_type", ""),
            "music_type": row.get("music_type", ""),
            "tag": row.get("tag", "")
        })
    
    return recommended
