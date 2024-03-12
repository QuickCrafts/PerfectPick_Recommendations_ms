
# Recommendation Microservice

Generation and management recommendations based on past user likes.

---
<br />

## API Reference

## GET /recommendation/{id_user}

This endpoint retrieves the recommendations for a specific user.

### Parameters

- `id_user` (path, required): an integer that represents the user's ID.

### Responses

- `200 OK`: Returns a list of recommendations for the specified user.
- `404 Not Found`: If no recommendations are found for the specified user.

### Example

```bash
curl -X GET "http://localhost:8000/recommendation/1"
```

## POST /recommendation/

This endpoint creates a new recommendation.

### Request Body

- `recommendation` (required): A JSON object that represents the recommendation. The structure of this object should follow the `RecommendationModel`.

### Responses

- `200 OK`: Returns a success message if the recommendation was added successfully.

### Example

```bash
curl -X POST "http://localhost:8000/recommendation/" -H "Content-Type: application/json" -d '{"key1":"value1", "key2":"value2"}'
```
## PUT /recommendation/{id_user}

This endpoint updates a recommendation for a specific user.

### Parameters

- `id_user` (path, required): an integer that represents the user's ID.

### Request Body

- `recommendation` (required): A JSON object that represents the updated recommendation. The structure of this object should follow the `RecommendationUpdateModel`.

### Responses

- `200 OK`: Returns a success message if the recommendation was updated successfully.

### Example

```bash
curl -X PUT "http://localhost:8000/recommendation/1" -H "Content-Type: application/json" -d '{"key1":"value1", "key2":"value2"}'
```

## DELETE /recommendation/{id_user}

This endpoint deletes all the recommendations for a specific user.

### Parameters

- `id_user` (path, required): an integer that represents the user's ID.

### Responses

- `200 OK`: Returns a success message if the recommendations were deleted successfully. The response body will contain a JSON object with a `data` field containing the message "recommendation deleted successfully".

### Example

```bash
curl -X DELETE "http://localhost:8000/recommendation/1"
```

## PUT /recommendation/remove/{id_user}

This endpoint removes an item from a user's recommendation.

### Parameters

- `id_user` (path, required): an integer that represents the user's ID.

### Request Body

- `removal_info` (required): A JSON object that represents the item to be removed. The structure of this object should follow the `ItemRemovalModel`.

### Responses

- `200 OK`: Returns a success message if the item was removed successfully. The response body will contain a JSON object with a `message` field containing the message "Item removed successfully".
- `400 Bad Request`: If an invalid section is specified.
- `404 Not Found`: If the user is not found or the item is not in the list.

### Example

```bash
curl -X PUT "http://localhost:8000/recommendation/remove/1" -H "Content-Type: application/json" -d '{"section":"movies", "id_to_remove":"123"}'
```

## Deployment

To deploy this project run

[//]: <> (@todo correct)

```bash
  docker pull mongo
  docker build -t fastapi-app . 
  docker network create mynetwork
  docker run -d --name myfastapi --network mynetwork -p 80:80 fastapi-app 
  docker run -d --name mymongo --network mynetwork -v mongodbdata:/data/db mongo
```



## Run Locally

Clone the project

[//]: <> (@todo correct all)

```bash
  git clone https://github.com/QuickCrafts/PerfectPick_Recommendations_ms.git
```

Go to the project directory

```bash
  cd PerfectPick_Recommendations_ms
```

Install dependencies

```bash
  pip install requirements.txt
```

Start the server

```bash
  uvicorn main:app --reload 
```
