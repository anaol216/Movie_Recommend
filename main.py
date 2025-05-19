import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import numpy as np
import os

# Load dataset
csv_path = "data/KuaiRand-Pure/KuaiRand-Pure/data/video_features_basic_pure.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Dataset not found at: {csv_path}")

movies = pd.read_csv(csv_path)

# Copy to new_data
new_data = movies.copy()

# Ensure required columns
required_columns = ["video_id", "video_type", "music_type", "tag"]
missing = [col for col in required_columns if col not in new_data.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Fill with "" and force all as string
for col in ["video_type", "music_type", "tag"]:
    new_data[col] = new_data[col].fillna("").astype(str)

# Just in case anything slipped through, ensure all are string type
new_data["video_type"] = new_data["video_type"].apply(lambda x: str(x))
new_data["music_type"] = new_data["music_type"].apply(lambda x: str(x))
new_data["tag"] = new_data["tag"].apply(lambda x: str(x))

# Combine tags safely
new_data["tags"] = (
    new_data["video_type"] + " " +
    new_data["music_type"] + " " +
    new_data["tag"]
)

# Vectorize tags
cv = CountVectorizer(max_features=10000, stop_words='english')
vector = cv.fit_transform(new_data["tags"].values.astype("U"))

# Compute cosine similarity
similarity = cosine_similarity(vector, dense_output=False).astype(np.float32)

# Save
with open("movies_list.pkl", "wb") as f:
    pickle.dump(new_data[["video_id", "video_type", "music_type", "tag"]], f)

with open("similarity.pkl", "wb") as f:
    pickle.dump(similarity, f)

print("✅ Model built and saved successfully!")
