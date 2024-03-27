from fastapi import FastAPI
from routes.route import router
from consumer.consumer import startup_event, consume_recommendations


app = FastAPI()
app.include_router(router)
app.add_event_handler("startup", startup_event)
