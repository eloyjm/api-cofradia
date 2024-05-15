import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL_PROD = os.getenv("SQLALCHEMY_DATABASE_URL_ENV")

    DATABASE_URL_TEST = os.getenv("SQLALCHEMY_DATABASE_URL_TEST")

    @classmethod
    def get_database_url(cls):
        if os.getenv("ENV") == "test":
            return cls.DATABASE_URL_TEST
        else:
            return cls.DATABASE_URL_PROD