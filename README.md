
# Recommendation Microservice

Generation and management recommendations based on past user likes.

---
<br />

## API Reference

#### Get Recommendation

Return last recommendation not used with arrays of movies, songs and books that user may like.

```http
  GET /recommendation/${id}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `int` | **Required**. User id |

| Response Status | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `200` | `success` | Returns information about possible recommendations|
| `404` | `error` | "User not found"|
| `400` | `error` | "Id not provided" |
| `500` | `error` | Any other error message|

```typescript
// Response interface
interface Response_recommendation_MS{
  id: number // User id
  movies: string[] // Id movies
  books: string[] // Id books
  songs: string[] // Id songs
}
```

#### Generate New Recommendation

Create a new recommendation to use later even if exits one not used yet.

```http
  POST /recommendation/${id}
```

```typescript
interface Get_Catalog{
  movies: Movie[] // Movie all info document[]
  books: Book[] // Book all info document[]
  songs: Song[] // Song all info document[]
}

interface Get_Likes{
  id: number // User id
  movies: Record<number, number>[] // {movie id, user rating}[]
  books: Record<number, number>[] // {book id, user rating}[]
  songs: Record<number, number>[] // {song id, user rating}[]
}

// Body interface
interface New_Recommendation{
  id: number //User id
  likes: GetLikes //User info likes
  catalog: Get_Catalog // Complete catalog
}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `int` | **Required**. User id |

| Response Status | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `201` | `success` | "Recommendation generated"|
| `404` | `error` | "User not found"|
| `400` | `error` | "Id not provided" |
| `500` | `error` | Any other error message|

#### Update recommendation use

Change to used the last user recommendation and review model, generate and save a new recommendation to use. (Regular model training for better recommendations).

```http
  PUT /recommendation/${id}
```

```typescript
interface Get_Catalog{
  movies: Movie[] // Movie all info document[]
  books: Book[] // Book all info document[]
  songs: Song[] // Song all info document[]
}

interface Like_Relation{
  id: string
  user_id: string
  type: 'MOV' | 'BOO' | 'SON'
  rating?: float // given by the user searched
  like_type: 'LK' | 'DLK' | 'BLK' // Liked | Disliked | Blank (no info yet)
  wishlist: boolean // Inside user wishlist? Yes or No
}

interface Get_Likes{
  id: number // User id
  movies: Like_Relation[]
  books: Like_Relation[]
  songs: Like_Relation[]
}

interface Get_User{
  id: string // User id
  firstname: string
  lastname: string // User last name
  avatar_url?: string // Url of avatar image
  birthdate?: string // String with the timestamp
  gender?: 'M' | 'F' | 'O' | 'P' // User gender coded
  country?: Country // Country information
  created_time: string // String with the timestamp
  email: string
  verified: boolean
  setup: boolean
}

// Body interface
interface New_Recommendation{
  likes: GetLikes //User info likes
  catalog: Get_Catalog // Complete catalog
  user: Get_User
}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `int` | **Required**. User id |

| Response Status | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `201` | `success` | "Recommendation updated and regenerated"|
| `404` | `error` | "Recommendation not found"|
| `400` | `error` | "Id not provided" |
| `500` | `error` | Any other error message|


---
<br />
<br />
<br />


## Run Locally

Clone the project

[//]: <> (@todo correct all)

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  pip install requirements.txt
```

Start the server

```bash
  uvicorn main:app --reload 

