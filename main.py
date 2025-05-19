#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle


# In[3]:


movies = pd.read_csv("archive (2)/KuaiRand-Pure/KuaiRand-Pure/data/video_features_basic_pure.csv")
movies.head()


# In[ ]:


# Get info about the dataset
movies.info()
# Get descriptive statistics
movies.describe(include='all')


# In[ ]:


# Check for missing values
movies.isnull().sum()


# In[ ]:


# Check columns
movies.columns


# In[ ]:


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


# In[ ]:


cv = CountVectorizer(max_features=10000, stop_words='english')
vector = cv.fit_transform(new_data["tags"].values.astype("U")).toarray()
vector.shape


# In[ ]:


similarity = cosine_similarity(vector)


# In[ ]:


def recommend(video_id):
    index = new_data[new_data["video_id"] == video_id].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)
    recommended = []

    for i in distances[1:6]:  # Top 5 recommendations
        recommended.append(new_data.iloc[i[0]]["video_id"])

    return recommended


# In[ ]:


recommend(1)  # Replace with an actual video_id from your data


# In[ ]:


pickle.dump(new_data, open("movies_list.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))


# In[ ]:


loaded_movies = pickle.load(open("movies_list.pkl", "rb"))
loaded_similarity = pickle.load(open("similarity.pkl", "rb"))

