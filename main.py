import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from scipy.sparse import save_npz, csr_matrix

# Load dataset
df = pd.read_csv("data/KuaiRand-Pure/KuaiRand-Pure/data/video_features_basic_pure.csv")

# Print the columns to debug
print("Columns in the CSV file:", df.columns)

# Correct the column names based on the actual CSV file
features_cols = ['video_type', 'music_type', 'tag']

# Check if the columns exist before proceeding.
for col in ['video_id'] + features_cols:
    if col not in df.columns:
        print(f"Error: Column '{col}' not found in DataFrame.")
        exit(1)  # Stop execution if a required column is missing.
        
# Downcast video_id to the smallest possible integer type
if df['video_id'].max() <= np.iinfo(np.int32).max:
    df['video_id'] = df['video_id'].astype(np.int32)
elif df['video_id'].max() <= np.iinfo(np.int64).max:
    df['video_id'] = df['video_id'].astype(np.int64)

movies = df[["video_id"] + features_cols].drop_duplicates()

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
cv = CountVectorizer(max_features=2000, stop_words='english')  # Reduced max_features
vector = cv.fit_transform(movies["tags"].values.astype("U"))  # vector is now a sparse matrix

# Similarity matrix (calculate on sparse matrix)
similarity = cosine_similarity(vector)  # similarity will be sparse if vector is sparse
similarity = similarity.astype(np.float32)

# Save files
pickle.dump(movies, open("movies_list.pkl", "wb"))
save_npz("similarity.npz", csr_matrix(similarity))  # Save similarity as sparse .npz

