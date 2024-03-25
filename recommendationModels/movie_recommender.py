import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open('C:/Users/dmriv/Documents/GitHub/PerfectPick_Recommendations_ms/recommendationModels/movies.json') as file:
    movie_data = json.load(file)

titles = []
genres = []
directors = []
writers = []
casts = []

for movie in movie_data:
    titles.append(movie['title'])
    genres.append(movie['genre'])
    directors.append(movie['director'])
    writers.append(movie['writers'])
    casts.append(movie['cast'])

features = []
for i in range(len(titles)):
    feature = f"{genres[i]} {directors[i]} {writers[i]} {casts[i]}"
    features.append(feature)

vectorizer = TfidfVectorizer()
feature_matrix = vectorizer.fit_transform(features)

def recommend_movies(movie_title, top_n=5):
    movie_index = titles.index(movie_title)
    movie_vector = feature_matrix[movie_index]

    similarity_scores = cosine_similarity(movie_vector, feature_matrix)
    similar_indices = similarity_scores.argsort()[0][-top_n-1:-1][::-1]

    similar_movies = [titles[i] for i in similar_indices]
    return similar_movies

movie_title = "For Love or Money"
recommended_movies = recommend_movies(movie_title)
print(f"Movies similar to '{movie_title}':")
for movie in recommended_movies:
    print(movie)
