# app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the recommendations.json on startup
try:
    with open("recommendations.json", "r") as f:
        recommendations = json.load(f)
except Exception as e:
    print("❌ Error loading recommendations.json:", e)
    recommendations = {}

@app.get("/")
def read_root():
    return {"message": "Video Recommendation API is running 🚀"}

@app.get("/recommend/{video_id}")
def get_recommendations(video_id: str):
    if video_id not in recommendations:
        raise HTTPException(status_code=404, detail=f"No recommendations found for video_id {video_id}")
    return {"video_id": video_id, "recommendations": recommendations[video_id]}
