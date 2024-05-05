import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL_PROD = os.getenv("SQLALCHEMY_DATABASE_URL")

    DATABASE_URL_TEST = "postgresql://postgres:admin@localhost:5432/cofradia"

    @classmethod
    def get_database_url(cls):
        if os.getenv("ENV") == "test":
            return cls.DATABASE_URL_TEST
        else:
            return cls.DATABASE_URL_PROD