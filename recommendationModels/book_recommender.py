import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from unidecode import unidecode

with open('recommendationModels/books.json') as file:
    book_data = json.load(file)

titles = []
authors = []
genres = []
for book in book_data:
    titles.append(book['title'])
    author = book.get('author', '')
    authors.append(author if author else '')
    genre = book.get('genres', '')
    genres.append(genre if genre else '')

features = []
for i in range(len(titles)):
    feature = f"{authors[i]} {genres[i]}"
    features.append(feature)

vectorizer = TfidfVectorizer()
feature_matrix = vectorizer.fit_transform(features)

def recommend_books(book_title, top_n=5):
    book_index = titles.index(book_title)
    book_vector = feature_matrix[book_index]
    similarity_scores = cosine_similarity(book_vector, feature_matrix)
    similar_indices = similarity_scores.argsort()[0][-top_n-1:-1][::-1]
    print
    similar_books = [titles[i] for i in similar_indices]
    return similar_books

def get_book_titles(book_ids):
    book_titles = []
    for book_id in book_ids:
        book_title = get_book_title_from_json(book_id)
        book_titles.append(book_title)
    return book_titles

def get_book_title_from_json(book_id):
    for book in book_data:
        if book["id_book"] == book_id:
            return book["title"]

def get_book_ids(book_titles):
    book_ids = []
    for book_title in book_titles:
        book_id = get_book_id_from_json(book_title)
        book_ids.append(book_id)
    return book_ids

def get_book_id_from_json(book_title):
    for book in book_data:
        if book["title"] == book_title:
            return book["id_book"]
    return None


# Example usage
#book_title = get_book_title_from_json("AYhxAQHUdCYC")
#recommended_books = recommend_books(book_title)
#for book in recommended_books:
#    print(book)