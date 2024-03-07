
# Recommendation Microservice

Generation and management recommendations based on past user likes.

## API Reference

#### Get Recommendation

Return last recomendation not used with arrays of movies, songs and books that user may like with  Id JSONss information of each one.

```http
  GET /recommendation/${id}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `string` | **Required**. User id |

| Response Status | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `200` | `success` | Returns information about possible recommendations|
| `404` | `error` | "User not found"|
| `400` | `error` | "Id not provided" |
| `500` | `error` | Any other error message|

```typescript
// Response interface
{
    id: string // User id
    movies: string[] // Id movies
    books: string[] // Id books
    songs: string[] // Id songs
}
```

#### Generate New Recommendation

Create a new recomendation to use later even if exits one not used yet.

```http
  POST /recommendation/${id}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `string` | **Required**. User id |

| Response Status | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `201` | `success` | "Recommendation generated"|
| `404` | `error` | "User not found"|
| `400` | `error` | "Id not provided" |
| `500` | `error` | Any other error message|

#### Update recommendation use

Change to used the last user recommendation.

```http
  PUT /recommendation/${id}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `string` | **Required**. User id |

| Response Status | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `201` | `success` | "Recommendation updated to used"|
| `404` | `error` | "Recommendation not found"|
| `400` | `error` | "Id not provided" |
| `500` | `error` | Any other error message|

#### Generate recommendation trigger

Regular model training to better recommendations. When the last recommendation is updated to used this function is triggered to review model, generate and save a new recommendation.

```typescript
// Trigger
generateRecommend(userId);
```

## Deployment

To deploy this project run

[//]: <> (@todo correct)

```bash
  npm run deploy
```

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
  npm install
```

Start the server

```bash
  npm 

