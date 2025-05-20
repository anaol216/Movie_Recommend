from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
import numpy as np
from scipy.sparse import load_npz, issparse
from functools import lru_cache
import os
from typing import List, Dict, Any

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_data(movies_pkl="movies_list.pkl", similarity_npz="similarity.npz"):
    """Loads movies data and similarity matrix."""
    try:
        with open(movies_pkl, "rb") as f:
            movies = pickle.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Error: {movies_pkl} not found. Please run main.py first.")
    except Exception as e:
        raise RuntimeError(f"Error loading movies data: {e}")

    try:
        similarity_mmap = np.load(similarity_npz, mmap_mode='r', allow_pickle=False)  # Memory-mapped file
    except FileNotFoundError:
        raise RuntimeError(f"Error: {similarity_npz} not found. Please run main.py first.")
    except Exception as e:
         raise RuntimeError(f"Error loading similarity matrix: {e}")
    
    return movies, similarity_mmap

movies, similarity_mmap = load_data()


@app.get("/")
def home():
    return {"message": "🎬 Movie Recommendation API is running!"}

@app.get("/columns", response_model=List[str])
def get_columns():
    """
    Returns the column names from the movies DataFrame.
    """
    return movies.columns.tolist()

@app.get("/all_videos", response_model=List[int])
def get_all_video_ids():
    """
    Returns all video IDs from the movies DataFrame
    """
    return movies["video_id"].tolist()


@lru_cache(maxsize=128)
@app.get("/recommend", response_model=List[Dict[str, Any]])
def recommend(video_id: int):
    """
    Provides movie recommendations based on video_id.

    Args:
        video_id (int): The ID of the video to get recommendations for.

    Returns:
        List[Dict[str, Any]]: A list of recommended movies (dictionaries).
    """
    if video_id not in movies["video_id"].values:
        raise HTTPException(status_code=404, detail=f"Video ID {video_id} not found")

    index = movies[movies["video_id"] == video_id].index[0]
    similarity_row = similarity_mmap['data'][index]  # Access with 'data' key
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
    return recommended

