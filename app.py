from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
import numpy as np
from scipy.sparse import load_npz, issparse
from functools import lru_cache
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the movies DataFrame
try:
    with open("movies_list.pkl", "rb") as f:
        movies = pickle.load(f)
    print("Loaded movies_list.pkl:")  # Debugging
    print(movies.head())
except FileNotFoundError:
    raise RuntimeError("movies_list.pkl not found. Please run main.py first.")

# Load the sparse similarity matrix using memory mapping
try:
    similarity_npz_path = "similarity.npz"
    similarity_mmap = np.load(similarity_npz_path, mmap_mode='r')  # Memory-mapped file
    print("Loaded similarity.npz with shape:", similarity_mmap['arr_0'].shape) # Debug
except FileNotFoundError:
    raise RuntimeError("similarity.npz not found. Please run main.py first.")


@app.get("/")
def home():
    return {"message": "🎬 Movie Recommendation API is running!"}

@app.get("/columns")  # New endpoint to get column names
def get_columns():
    """
    Returns the column names from the movies DataFrame.
    """
    return {"columns": movies.columns.tolist()}

@app.get("/all_videos")
def get_all_video_ids():
    """
    Returns all video IDs from the movies DataFrame
    """
    return {"video_ids": movies["video_id"].tolist()}


@lru_cache(maxsize=128)
@app.get("/recommend")
def recommend(video_id: int):
    print(f"Finding recommendations for video_id: {video_id}")  # Debugging
    print(f"Video IDs in movies: {movies['video_id'].unique()}")
    if video_id not in movies["video_id"].values:
        raise HTTPException(status_code=404, detail="Video ID not found")

    index = movies[movies["video_id"] == video_id].index[0]
    print(f"Found index: {index} for video_id: {video_id}") # Debug
    similarity_row = similarity_mmap['arr_0'][index]
    distances = list(enumerate(similarity_row))
    distances = sorted(distances, reverse=True, key=lambda x: x[1])
    recommended = []
    for i in distances[1:6]:
        row = movies.iloc[i[0]]
        recommended.append({
            "video_id": int(row["video_id"]),
            "video_type": row.get("video_type", ""),
            "music_type": row.get("music_type", ""),
            "tag": row.get("tag", "")
        })
    print("Recommendations:", recommended)
    return recommended

