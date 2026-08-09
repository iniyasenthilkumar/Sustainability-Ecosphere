import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    # Flask application secret key for session signing
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ecosphere-hackathon-super-secret-key-12345'
    
    # Database URI configuration
    # Fallback to local SQLite if DATABASE_URL is not defined in .env
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'ecosphere.db')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
