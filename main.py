import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import save_npz

# Load dataset
df = pd.read_csv("archive/KuaiRand-Pure/KuaiRand-Pure/data/video_features_statistic_pure.csv")

# Columns to use as features (adjust if you find more relevant ones)
features_cols = ["video_type", "upload_dt", "upload_type"]

# Drop duplicates based on video_id + feature columns
movies = df[["video_id"] + features_cols].drop_duplicates()

# Combine feature columns into one string, fill missing values with empty string
movies["features"] = movies[features_cols].fillna('').agg(' '.join, axis=1)

# Vectorize combined text features using TF-IDF (sparse matrix)
tfidf = TfidfVectorizer(stop_words="english")
feature_matrix = tfidf.fit_transform(movies["features"])

# Compute sparse cosine similarity matrix by multiplying sparse TF-IDF matrix with its transpose
similarity_sparse = feature_matrix * feature_matrix.T

# Remove the temporary 'features' column before saving
movies.drop(columns=["features"], inplace=True)

# Save movies DataFrame (pickle)
with open("movies_list.pkl", "wb") as f:
    pickle.dump(movies, f)

# Save sparse similarity matrix (.npz)
save_npz("similarity.npz", similarity_sparse)

print("Memory-optimized movies list and similarity matrix saved!")
