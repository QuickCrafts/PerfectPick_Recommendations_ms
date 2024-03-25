import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from ast import literal_eval

# Load the dataset
df1 = pd.read_csv('C:/Users/dmriv/Documents/GitHub/PerfectPick_Recommendations_ms/recommendationModels/tmdb_5000_credits.csv')
df2 = pd.read_csv('C:/Users/dmriv/Documents/GitHub/PerfectPick_Recommendations_ms/recommendationModels/tmdb_5000_movies.csv')

# Rename columns in df1
df1.columns = ['id', 'tittle', 'cast', 'crew']

# Merge df1 and df2 on 'id' column
df2 = df2.merge(df1, on='id')

# Fill missing values in 'overview' column with an empty string
df2['overview'] = df2['overview'].fillna('')

# Create TF-IDF matrix from 'overview' column
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df2['overview'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Create a reverse mapping of movie titles to indices
indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()

# Function to get recommendations based on cosine similarity
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df2['title'].iloc[movie_indices]

# Convert specific columns to Python objects using literal_eval
features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(literal_eval)

# Function to extract the director's name from the crew column
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

# Function to get the top 3 elements from a list or return an empty list if not a list
def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names
    return []

# Apply the functions to the respective columns
df2['director'] = df2['crew'].apply(get_director)

features = ['cast', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(get_list)

# Function to clean the data by converting to lowercase and removing spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

features = ['cast', 'keywords', 'director', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(clean_data)

# Function to create a "soup" by combining specific columns
def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])

df2['soup'] = df2.apply(create_soup, axis=1)

# Create a count matrix from the "soup" column
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

# Reset the index of df2
df2 = df2.reset_index()

# Create a reverse mapping of movie titles to indices
indices = pd.Series(df2.index, index=df2['title'])

# Get recommendations for a specific movie
print(get_recommendations('The Dark Knight Rises', cosine_sim2))