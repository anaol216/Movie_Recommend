from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

# ✅ Load recommendations.json
recommendations_file = "recommendations.json"
if not os.path.exists(recommendations_file):
    raise FileNotFoundError(f"{recommendations_file} not found. Please run the script to generate it.")

with open(recommendations_file, "r") as f:
    recommendations = json.load(f)

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Allow CORS for your deployed frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://movierecommend-git-main-anaol-atinafus-projects.vercel.app"],  # Update if you deploy elsewhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ API endpoint
@app.get("/recommend/{video_id}")
async def get_recommendations(video_id: str):
    recs = recommendations.get(video_id, [])
    return {
        "video_id": video_id,
        "recommendations": recs  # This will be a list like ["2", "3", "6", "8", "10"]
    }
