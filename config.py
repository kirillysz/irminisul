from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path="config.env")

class Config:
    UPLOAD_DIR = "app/api/v1/uploads"
    RECAPTCHA_SECRET = getenv("RECAPTCHA")

    ENDPOINT = getenv("ENDPOINT")
    DB_KEY = getenv("DB_KEY")
    PROJECT_ID = getenv("PROJECT_ID")
    DATABASE_ID = getenv("DATABASE_ID")
    COLLECTION_ID = getenv("COLLECTION_ID")
    ENDPOINT = getenv("ENDPOINT")
    BUCKET_ID = getenv("BUCKET_ID")