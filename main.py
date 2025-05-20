from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd

app = FastAPI()

# CORS setup (IMPORTANT for frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
movies = pickle.load(open("models/movies_list.pkl", "rb"))
similarity = pickle.load(open("models/similarity.pkl", "rb"))

@app.get("/")
def root():
    return {"message": "🎬 Video Recommendation API is running"}

@app.get("/recommend")
def recommend(video_id: int):
    if video_id not in movies["video_id"].values:
        raise HTTPException(status_code=404, detail="Video ID not found")
    
    index = movies[movies["video_id"] == video_id].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended = []
    for i in distances[1:6]:  # Top 5 excluding self
        row = movies.iloc[i[0]]
        recommended.append({
            "video_id": int(row["video_id"]),
            "video_type": str(row.get("video_type", "")),
            "music_type": str(row.get("music_type", "")),
            "tag": str(row.get("tag", ""))
        })
    
    return recommended
