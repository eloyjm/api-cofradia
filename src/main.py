from fastapi import FastAPI
from .app.db.database import Base,engine
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .app.routers.hermandades import hermandades_router
from .app.db.migrations.populate_db import populate_database
from .app.routers.timetables import timetables_router

app = FastAPI()
app.include_router(hermandades_router)
app.include_router(timetables_router)

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print("Error al crear las tablas:", e)
create_tables()
populate_database()


origins = [
    "http://localhost:3000", "*", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#ARRANQUE
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)