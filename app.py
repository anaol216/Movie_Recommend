from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
import numpy as np
import os

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
try:
    with open("movies_list.pkl", "rb") as f:
        movies = pickle.load(f)

    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)

except FileNotFoundError:
    raise RuntimeError("Model files not found. Please run main.py first.")

@app.get("/")
def home():
    return {"message": "🎬 Movie Recommendation API is running!"}

@app.get("/recommend")
def recommend(video_id: int):
    if video_id not in movies["video_id"].values:
        raise HTTPException(status_code=404, detail="Video ID not found")

    index = movies[movies["video_id"] == video_id].index[0]
    distances = list(enumerate(similarity[index].toarray()[0]))
    distances = sorted(distances, reverse=True, key=lambda x: x[1])

    # Get top 5 recommendations (skip the first one which is the input video itself)
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
