
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from scipy.sparse import save_npz, csr_matrix

def create_recommendation_data(csv_file="data/KuaiRand-Pure/KuaiRand-Pure/data/video_features_basic_pure.csv",
                             max_features=2000,
                             output_movies_pkl="movies_list.pkl",
                             output_similarity_npz="similarity.npz"):
    """
    Processes video data, calculates similarity, and saves results.

    Args:
        csv_file (str): Path to the CSV file.
        max_features (int): Maximum features for CountVectorizer.
        output_movies_pkl (str): Path to save movies DataFrame.
        output_similarity_npz (str): Path to save similarity matrix.
    """
    try:
        # Load dataset
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: CSV file not found at {csv_file}")

    # Print the columns to debug
    print("Columns in the CSV file:", df.columns)

    # Correct the column names based on the actual CSV file
    features_cols = ['video_type', 'music_type', 'tag']

    # Check if the columns exist before proceeding.
    for col in ['video_id'] + features_cols:
        if col not in df.columns:
            raise KeyError(f"Error: Column '{col}' not found in DataFrame.")

    movies = df[["video_id"] + features_cols].drop_duplicates()

    # Downcast video_id to the smallest possible integer type
    if movies['video_id'].max() <= np.iinfo(np.int32).max:
        movies['video_id'] = movies['video_id'].astype(np.int32)
    elif movies['video_id'].max() <= np.iinfo(np.int64).max:
        movies['video_id'] = movies['video_id'].astype(np.int64)

    # Fill only object (string) columns with ""
    for col in ["video_type", "music_type", "tag"]:
        if col in movies.columns:  # check if the column exists
            if movies[col].dtype == "float64":
                movies[col] = movies[col].fillna(0).astype(np.float32).astype(str)  # Convert to string
            else:
                movies[col] = movies[col].fillna("").astype(str)

    # Combine selected features into a single text field
    movies["tags"] = (
        movies["video_type"].astype(str) + " " +
        movies["music_type"].astype(str) + " " +
        movies["tag"].astype(str)
    )

    # Vectorize
    cv = CountVectorizer(max_features=max_features, stop_words='english')  # Reduced max_features
    vector = cv.fit_transform(movies["tags"].values.astype("U"))  # vector is now a sparse matrix

    # Similarity matrix (calculate on sparse matrix)
    similarity = cosine_similarity(vector)  # similarity will be dense matrix
    similarity = similarity.astype(np.float32)

    # Save files
    try:
        with open(output_movies_pkl, "wb") as f:
            pickle.dump(movies, f)
    except Exception as e:
        raise RuntimeError(f"Error saving movies data: {e}")

    try:
        save_npz(output_similarity_npz, csr_matrix(similarity))  # <-- FIXED HERE
    except Exception as e:
        raise RuntimeError(f"Error saving similarity matrix: {e}")
    
    print(f"Saved movies data to {output_movies_pkl}")
    print(f"Saved similarity matrix to {output_similarity_npz}")


if __name__ == "__main__":
    create_recommendation_data()
