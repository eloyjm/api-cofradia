from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session , joinedload
from ..db.database import get_db
from ..db.models.user import UserInDB as DBUserInDB
from ..db.models.user import User as DBUser
from ..schemas.users import Token, TokenData, User
import os
from dotenv import load_dotenv
 
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

oAuth2_router = APIRouter()

db_dependency = Annotated[Session,Depends(get_db)]

def get_user_inDB(username: str, db: db_dependency):

    user = db.query(DBUserInDB).filter(DBUserInDB.username == username).options(joinedload(DBUserInDB.user)).first()
    if user != None: 
        return user

def authenticate_user(username: str, password: str, db: db_dependency):
    user = get_user_inDB(username, db)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Por favor, vuelva a iniciar sesión.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        disabled: bool = payload.get("disabled")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, disabled = disabled)
    except JWTError:
        raise credentials_exception
    username=token_data.username
    user = get_user_inDB(username, db)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_user_by_email(email:str, db: db_dependency):
    find_user = db.query(DBUser).filter_by(email = email).first()
    if find_user == None:
        return []
    else:
        return find_user

@oAuth2_router.post("/login",  tags=["OAuth"], response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = get_user_by_email(form_data.username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = authenticate_user(user.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user = db.query(DBUser).filter_by(username = user.username).first()
    disabled = user.disabled
    access_token = create_token(data={"sub": user.username, "disabled": disabled}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}



