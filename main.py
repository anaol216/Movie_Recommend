# main.py
import pandas as pd
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def generate_recommendations_json(
    csv_file="data/KuaiRand-Pure/KuaiRand-Pure/data/video_features_basic_pure",
    output_json="recommendations.json",
    top_n=5
):
    df = pd.read_csv(csv_file)

    df.fillna("", inplace=True)
    df["tags"] = df["video_type"].astype(str) + " " + df["music_type"].astype(str) + " " + df["tag"].astype(str)

    cv = CountVectorizer(max_features=2000, stop_words="english")
    vectors = cv.fit_transform(df["tags"].values.astype("U"))
    similarity = cosine_similarity(vectors)

    results = {}
    for idx in range(len(df)):
        video_id = str(df.iloc[idx]["video_id"])
        sim_scores = list(enumerate(similarity[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
        top_ids = [str(df.iloc[i[0]]["video_id"]) for i in sim_scores]
        results[video_id] = top_ids

    with open(output_json, "w") as f:
        json.dump(results, f)

    print(f"✅ Recommendations saved to {output_json}")

if __name__ == "__main__":
    generate_recommendations_json()
