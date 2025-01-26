from fastapi import FastAPI, Depends
from .app.db.database import Base,engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from sqlalchemy.orm import Session
import uvicorn
from .app.routers.hermandades import hermandades_router
from .app.db.migrations.populate_db import populate_database
from .app.routers.timetables import timetables_router
from .app.routers.users import user_router
from .app.routers.oauth import oAuth2_router
from .app.routers.marchas import marchas_router
from dotenv import load_dotenv
import os

load_dotenv()
db_dependency = Annotated[Session, Depends(get_db)]

app = FastAPI()
app.include_router(hermandades_router)
app.include_router(timetables_router)
app.include_router(user_router)
app.include_router(marchas_router)
app.include_router(oAuth2_router)

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created")
    except Exception as e:
        print("Error creating tables:", e)
        
create_tables()
populate_database()
'''
if os.getenv("ENV") == "test":
    populate_database()
'''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#ARRANQUE
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)