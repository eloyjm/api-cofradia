import json
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles

from config.app import config_app
from config.logging.logger import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import hermandad_router
from router import march_router
from router import timetable_router
import os
from database.postgresdb_manager import db_manager
from repository.hermandad_repository import HermandadRepository
from repository.march_repository import MarchRepository
from repository.timetable_repository import TimetableRepository
from service.hermandad_service import HermandadService
from service.march_service import MarchService
from service.timetable_service import TimetableService


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Initializes all repositories before running the API
    """
    try:
        logger.info("Initializing API...")

        db_manager.create_tables()

        hermandad_repository = HermandadRepository(db_manager)
        with open(config_app.hermandades_data_path, encoding="utf-8") as file:
            hermandades_data = json.load(file)

        hermandad_service = HermandadService(
            hermandad_repository, hermandades_data
        )
        march_repository = MarchRepository(db_manager)
        march_service = MarchService(march_repository)

        timetable_repository = TimetableRepository(db_manager)
        timetable_service = TimetableService(
            timetable_repository, hermandad_service
        )

        yield {
            "hermandad_service": hermandad_service,
            "march_service": march_service,
            "timetable_service": timetable_service,
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
app.include_router(march_router.router)
app.include_router(timetable_router.router)
