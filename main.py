import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import save_npz

# Load raw dataset (update path if needed)
df = pd.read_csv("data/KuaiRand-Pure/KuaiRand-Pure/data/video_features_statistic_pure.csv")

# Select necessary columns (update based on your real columns)
movies = df[["video_id", "video_type", "music_type", "tag"]].drop_duplicates()

# Create combined feature string column for similarity
movies["features"] = movies["video_type"].fillna('') + " " + movies["music_type"].fillna('') + " " + movies["tag"].fillna('')

# Vectorize features using TF-IDF (creates sparse matrix)
tfidf = TfidfVectorizer(stop_words="english")
feature_matrix = tfidf.fit_transform(movies["features"])

# Compute cosine similarity matrix (dense is large; we save sparse dot product)
# similarity = cosine_similarity(feature_matrix)  # Dense matrix

# Instead of dense, save the sparse matrix directly as feature_matrix (we can use dot product later)
# But since your API expects similarity, let's precompute similarity matrix sparse:

from sklearn.metrics.pairwise import linear_kernel
similarity = linear_kernel(feature_matrix, feature_matrix)  # returns dense matrix

# To optimize memory: convert to sparse matrix and save
from scipy.sparse import csr_matrix
similarity_sparse = csr_matrix(similarity)

# Save movies DataFrame as pickle (drop features to save space)
movies.drop(columns=["features"], inplace=True)
with open("movies_list.pkl", "wb") as f:
    pickle.dump(movies, f)

# Save similarity sparse matrix as .npz (more efficient)
save_npz("similarity.npz", similarity_sparse)

print("Pickle and similarity matrix saved!")
