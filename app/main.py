import json
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles

from config.app import config_app
from config.logging.logger import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import hermandad_router
import os
from database.postgresdb_manager import db_manager
from repository.hermandad_repository import HermandadRepository
from service.hermandad_service import HermandadService


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Initializes all repositories before running the API
    """
    try:
        logger.info("Initializing API...")

        db_manager.create_tables()

        hermandad_repository = HermandadRepository(db_manager)

        hermandad_service = HermandadService(hermandad_repository)

        yield {
            "hermandad_service": hermandad_service,
        }

    except Exception as e:

        logger.error(f"Error during application startup: {e}")

    finally:

        logger.info("Shutting down application...")
        db_manager.close_connection()

app = FastAPI(
    lifespan=lifespan,
    title="CofradIA API",
    version=config_app.version,
    docs_url="/docs",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials="false",
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hermandad_router.router)

# Save the OpenAPI schema when the APP is up
openapi_data = app.openapi()
with open(config_app.openapi_path, "w") as file:
    json.dump(openapi_data, file, indent=4)
