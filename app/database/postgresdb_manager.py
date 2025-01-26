from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

from config.database import database
from config.logging.logger import logger


class DatabaseManager:
    def __init__(self):
        try:
            self.engine = create_engine(database.get_connection_uri())
        except SQLAlchemyError as e:
            raise SQLAlchemyError(
                f"SQLAlchemy Error connecting to the database: {e}"
            )

        self.session_local = sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False
        )
        self.base_schemas = declarative_base()

    def get_db(self):
        db = self.session_local()
        try:
            yield db

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Error connecting to the database: {e}",
            )

        finally:
            db.close()

    def create_tables(self):
        """
        Creates all database tables defined in the application.
        """
        if self.engine is None:
            raise RuntimeError("Error: Database connection not initialized")
        self.base_schemas.metadata.create_all(bind=self.engine)

    def close_connection(self):
        """
        Closes the database connection by disposing the engine.
        """
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")
        else:
            logger.warning("No database connection to close")


db_manager = DatabaseManager()
