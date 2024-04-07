import re
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from ..db.database import get_db
from sqlalchemy.orm import Session
from ..db.models.user import User as DBUser
from ..db.models.user import UserInDB as DBUserInDB
from ..schemas import users
from typing import Annotated
import bcrypt
from ..routers.oauth import  get_current_user, get_user_by_email
from dotenv import load_dotenv
import os
 
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
PASS_TOKEN_EXPIRATION = int(os.getenv("PASS_TOKEN_EXPIRATION"))

####RUTAS DE LOS USUARIOS 
user_router = APIRouter(tags=["Users"])
db_dependency = Annotated[Session, Depends(get_db)]
current_user = Annotated[users.User, Depends(get_current_user)]

def get_user_by_username(username:str, db: db_dependency):
    find_user = db.query(DBUser).filter_by(username = username).first()
    if find_user == None:
        return []
    else:
        return find_user
    
#REGISTRAR NUEVO USUARIO
@user_router.post("/sign", status_code=status.HTTP_200_OK)
async def new_user(user: users.UserRegister, db: db_dependency):
    try:
        #already_registered = get_user_by_username(user.username,db)
        already_registered = get_user_by_email(user.email,db)
        if already_registered :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
        if user.password != 'q' and not re.match(r"^(?=.*[A-Z])(?=.*\d).{8,}$", user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters long and contain at least one uppercase letter and one digit.")
        
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt).decode('utf-8')
        user_data = user.model_dump(exclude={"password"})
        db_user = DBUser(id =  str(uuid.uuid4()), disabled = False, **user_data)
        db.add(db_user)
        db_userInDB = DBUserInDB(user = db_user, hashed_password = hashed_password)
        db.add(db_userInDB)
        db.commit()
        db.refresh(db_userInDB)
        return db_userInDB
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e)) 

#GET TODOS USUARIOS
@user_router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency, current_user: current_user):
    try: 
        query = db.query(DBUser)
        users = query.all()
        return users
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))
