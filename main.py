import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load dataset
movies = pd.read_csv("data/KuaiRand-Pure/KuaiRand-Pure/data/video_features_basic_pure.csv")

# Copy to new_data
new_data = movies.copy()

# Fill only object (string) columns with ""
for col in ["video_type", "music_type", "tag"]:
    if new_data[col].dtype == "float64":
        new_data[col] = new_data[col].fillna("").astype(str)
    else:
        new_data[col] = new_data[col].fillna("").astype(str)

# Combine selected features into a single text field
new_data["tags"] = (
    new_data["video_type"] + " " +
    new_data["music_type"] + " " +
    new_data["tag"]
)

# Vectorize
cv = CountVectorizer(max_features=10000, stop_words='english')
vector = cv.fit_transform(new_data["tags"].values.astype("U")).toarray()

# Similarity matrix
similarity = cosine_similarity(vector)

# Save pickles
pickle.dump(new_data, open("movies_list.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))