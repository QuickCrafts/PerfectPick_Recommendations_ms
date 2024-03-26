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

def get_movie_titles(movie_ids):
    movie_titles = []
    for movie_id in movie_ids:
        movie_title = get_movie_title_from_json(movie_id)
        movie_titles.append(movie_title)
    return movie_titles

def get_movie_title_from_json(movie_id):
    with open("C:/Users/dmriv/Documents/GitHub/PerfectPick_Recommendations_ms/recommendationModels/movies.json") as file:
        movie_data = json.load(file)
    
    for movie in movie_data:
        if movie["id_movie"] == movie_id:
            return movie["title"]
    
    return None


def get_movie_ids(movie_titles):
    movie_ids = []
    for movie_title in movie_titles:
        movie_id = get_movie_id_from_json(movie_title)
        movie_ids.append(movie_id)
    return movie_ids

def get_movie_id_from_json(movie_title):
    with open("C:/Users/dmriv/Documents/GitHub/PerfectPick_Recommendations_ms/recommendationModels/movies.json") as file:
        movie_data = json.load(file)
    
    for movie in movie_data:
        if movie["title"] == movie_title:
            return movie["id_movie"]
    
    return None

'''
movie_title = "For Love or Money"
recommended_movies = recommend_movies(movie_title)
print(f"Movies similar to '{movie_title}':")
for movie in recommended_movies:
    print(movie)
'''