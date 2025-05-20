from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
from scipy.sparse import load_npz

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
except FileNotFoundError:
    raise RuntimeError("movies_list.pkl not found. Please run main.py first.")

# Load the sparse similarity matrix
try:
    similarity = load_npz("similarity.npz")
except FileNotFoundError:
    raise RuntimeError("similarity.npz not found. Please run main.py first.")

@app.get("/")
def home():
    return {"message": "🎬 Movie Recommendation API is running!"}

@app.get("/recommend")
def recommend(video_id: int):
    if video_id not in movies["video_id"].values:
        raise HTTPException(status_code=404, detail="Video ID not found")

    index = movies[movies["video_id"] == video_id].index[0]
    # similarity is sparse matrix, convert row to dense for sorting
    distances = list(enumerate(similarity[index].toarray()[0]))
    distances = sorted(distances, reverse=True, key=lambda x: x[1])

    recommended = []
    for i in distances[1:6]:  # skip self, get top 5
        row = movies.iloc[i[0]]
        recommended.append({
            "video_id": int(row["video_id"]),
            "video_type": row.get("video_type", ""),
            "music_type": row.get("music_type", ""),
            "tag": row.get("tag", "")
        })

    return recommended
