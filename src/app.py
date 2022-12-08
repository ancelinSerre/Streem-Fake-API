# Standar imports
import logging

# 3rd party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger

# Local imports 
import models
from routers import (
    energy_producers, 
    electrical_meters, 
    factories, 
    invoices,
    meter_readings
)
from database import engine
# from insert_fake_data import generate_fake_data

# Tell the logger to use gunicorn’s log level instead of the default one
# if the app is loaded via gunicorn
gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
logger.handlers = gunicorn_error_logger.handlers
if __name__ != "__main__":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)

app = FastAPI()

# No CORS restrictions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

# Include all routers for each data model
app.include_router(energy_producers.router)
app.include_router(factories.router)
app.include_router(invoices.router)
app.include_router(electrical_meters.router)
app.include_router(meter_readings.router)

# Initialize database tables
models.Base.metadata.create_all(bind=engine)


# Load dummy data in order to test the API
# generate_fake_data()

@app.get("/", tags=["Default"])
def welcome_api_users():
    """
    Welcome API users.
    """
    return "Hello 👋, check the API docs 👉 <url>:<port>/docs"