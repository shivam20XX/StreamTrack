import os
print("Running from:", os.getcwd())
from dotenv import load_dotenv

load_dotenv()

TMDB_KEY = os.getenv('TMDB_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p'


DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'streamtrack'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}
