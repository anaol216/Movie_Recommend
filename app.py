# app.py
import pickle
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scipy.sparse import load_npz

app = FastAPI()

# Allow CORS for your frontend or development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set your frontend domain here in production
    allow_credentials=True,
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
        similarity_mmap = load_npz(similarity_npz)  # FIXED: Removed allow_pickle=False
    except FileNotFoundError:
        raise RuntimeError(f"Error: {similarity_npz} not found. Please run main.py first.")
    except Exception as e:
        raise RuntimeError(f"Error loading similarity matrix: {e}")
    
    return movies, similarity_mmap


def recommend(movie_title: str, movies, similarity_mmap):
    if movie_title not in movies["title"].values:
        raise ValueError(f"Movie '{movie_title}' not found in dataset.")
    
    idx = movies[movies["title"] == movie_title].index[0]
    sim_scores = list(enumerate(similarity_mmap[idx].toarray()[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]  # Top 5 excluding itself

    recommended = []
    for i in sim_scores:
        movie = movies.iloc[i[0]]
        recommended.append({
            "title": movie["title"],
            "id": movie["movie_id"]
        })
    
    return recommended


# Load data on startup
try:
    movies, similarity_mmap = load_data()
except Exception as e:
    print(e)
    raise


@app.get("/")
def read_root():
    return {"message": "Movie Recommendation API is running 🚀"}


@app.get("/recommend/{movie_title}")
def get_recommendations(movie_title: str):
    try:
        recommendations = recommend(movie_title, movies, similarity_mmap)
        return {"recommendations": recommendations}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
