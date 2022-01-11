import os


class Config:
    """Base configuration variables."""
    MONGO_CONNECTION_STRING = os.environ.get('MONGO_CONNECTION_STRING')
    if not MONGO_CONNECTION_STRING:
       raise ValueError("No MONGO_CONNECTION_STRING set for Flask application. Did you follow the setup instructions?")
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
       raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")