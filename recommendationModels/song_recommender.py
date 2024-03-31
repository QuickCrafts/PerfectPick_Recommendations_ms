import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open('recommendationModels/songs.json', encoding='utf-8') as file:
    song_data = json.load(file)

titles = []
artists = []
albums = []
genres = []
for song in song_data:
    titles.append(song['title'])
    artists.append(song['artist'])
    albums.append(song['album'])
    genres.append(song['genres'] if song['genres'] else '')

features = []
for i in range(len(titles)):
    feature = f"{artists[i]} {albums[i]} {genres[i]}"
    features.append(feature)

vectorizer = TfidfVectorizer()
feature_matrix = vectorizer.fit_transform(features)

def recommend_songs(song_title, top_n=5):
    song_index = titles.index(song_title)
    song_vector = feature_matrix[song_index]
    similarity_scores = cosine_similarity(song_vector, feature_matrix)
    similar_indices = similarity_scores.argsort()[0][-top_n-1:-1][::-1]
    similar_songs = [titles[i] for i in similar_indices]
    return similar_songs

def get_song_titles(song_ids):
    song_titles = []
    for song_id in song_ids:
        song_title = get_song_title_from_json(song_id)
        song_titles.append(song_title)
    return song_titles

def get_song_title_from_json(song_id):
    with open("recommendationModels/songs.json", encoding='utf-8') as file:
        song_data = json.load(file)
    for song in song_data:
        if song["id_song"] == song_id:
            return song["title"]
    return None

def get_song_ids(song_titles):
    song_ids = []
    for song_title in song_titles:
        song_id = get_song_id_from_json(song_title)
        song_ids.append(song_id)
    return song_ids

def get_song_id_from_json(song_title):
    with open("recommendationModels/songs.json", encoding='utf-8') as file:
        song_data = json.load(file)
    for song in song_data:
        if song["title"] == song_title:
            return song["id_song"]
    return None

# Example usage
'''
song_title = "Cruel Summer"
recommended_songs = recommend_songs(song_title)
print(f"Songs similar to '{song_title}':")
for song in recommended_songs:
    print(song)

'''