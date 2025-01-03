from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import re
from sqlalchemy.orm import Session
from models import Base, Movie, Rating, Session


def clean_title(title):
    return re.sub("[^a-zA-Z0-9 ]", "", title)

def search(session, title, genre=None):
    movies = pd.read_sql("SELECT * FROM movies", session.bind)
    title = clean_title(title)
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf = vectorizer.fit_transform(movies['clean_title'])

    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices].iloc[::-1]
    
    if genre:
        results = results[results['genre'].str.contains(genre, case=False, na=False)]
    return results


def collaborative_filtering(movie_id, session):
    ratings = pd.read_sql("SELECT userid, movieid, rating FROM ratings", session.bind)
    movies = pd.read_sql("SELECT * FROM movies", session.bind)
    if 'movieid' not in ratings.columns:
        raise ValueError("movieid column is missing in the ratings data")

    similar_users = ratings[(ratings["movieid"] == movie_id) & (ratings["rating"] > 3)]["userid"].unique()

    similar_user_recs = ratings[(ratings["userid"].isin(similar_users)) & (ratings["rating"] > 3)]["movieid"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

    all_users = ratings[(ratings["movieid"].isin(similar_user_recs.index)) & (ratings["rating"] > 3)]
    all_user_recs = all_users["movieid"].value_counts() / len(all_users["userid"].unique())

    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1).fillna(0)
    rec_percentages.columns = ["similar", "all"]
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    recommendations = rec_percentages.head(10).merge(
        movies,
        left_index=True,
        right_on="id"  
    )[['score', 'title', 'genre']]
    
    return recommendations.to_dict(orient="records")
