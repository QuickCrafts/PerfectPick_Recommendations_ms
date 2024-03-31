import pika
import threading
import json
from recommendationModels.book_recommender import get_book_ids, get_book_titles, recommend_books
from recommendationModels.movie_recommender import get_movie_ids, get_movie_titles, recommend_movies
from recommendationModels.song_recommender import get_song_ids, get_song_titles, recommend_songs
from models.recommendations import ItemRemovalModel, RecommendationModel, RecommendationUpdateModel
from config.database import collection_name


def consume_recommendations():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='recommendations')

    def callback(ch, method, properties, body):
        recommendation_data = json.loads(body)
        create_recommendation_from_message(recommendation_data)

    channel.basic_consume(queue='recommendations', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    

def create_recommendation_from_message(recommendation_data):
    user_id = recommendation_data["id_user"]
    liked_movie_ids = recommendation_data["movies"]
    liked_book_ids = recommendation_data["books"]
    liked_song_ids = recommendation_data["songs"]

    existing_recommendation = collection_name.find_one({"id_user": user_id})

    movie_titles = get_movie_titles(liked_movie_ids)
    recommended_movies = []
    for title in movie_titles:
        recommended_movies.extend(recommend_movies(title))
    recommended_movies = list(set(recommended_movies))
    recommended_movie_ids = get_movie_ids(recommended_movies)

    book_titles = get_book_titles(liked_book_ids)
    recommended_books = []
    for title in book_titles:
        recommended_books.extend(recommend_books(title))
    recommended_books = list(set(recommended_books))
    recommended_book_ids = get_book_ids(recommended_books)

    song_titles = get_song_titles(liked_song_ids)
    recommended_songs = []
    for title in song_titles:
        recommended_songs.extend(recommend_songs(title))
    recommended_songs = list(set(recommended_songs))
    recommended_song_ids = get_song_ids(recommended_songs)

    recommendation_data = {
        "id_user": user_id,
        "movies": recommended_movie_ids,
        "books": recommended_book_ids,
        "songs": recommended_song_ids,
    }

    if existing_recommendation:
        collection_name.update_one(
            {"id_user": user_id},
            {"$set": recommendation_data}
        )
        print("Recommendation updated successfully")
        print(' [*] Waiting for messages. To exit press CTRL+C')

    else:
        collection_name.insert_one(recommendation_data)
        print("Recommendation added successfully")
        print(' [*] Waiting for messages. To exit press CTRL+C')

def test_message():
    recommendation_data = {
    "id_user": 245564845,
    "movies": ["tt0106941", "tt0118694"],
    "books": ["AYhxAQHUdCYC", "fyPsAAAAMAAJ"],
    "songs": ["3qhlB30KknSejmIvZZLjOD"]
    }
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
    channel = connection.channel()
    channel.queue_declare(queue='recommendations')
    message = json.dumps(recommendation_data)

    channel.basic_publish(exchange='', routing_key='recommendations', body=message)
    print(f" [x] Sent recommendation data: {message}")

    connection.close()

async def startup_event():
    thread = threading.Thread(target=consume_recommendations, daemon=True)
    thread.start()