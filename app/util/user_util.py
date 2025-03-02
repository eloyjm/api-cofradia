import re
from config.logging.logger import logger
from fastapi import HTTPException
import bcrypt
from datetime import timedelta
from datetime import datetime
from datetime import timezone
from config.app import config_app
from jose import jwt


def password_validator(password: str) -> str:
    if not re.match(r"^(?=.*[A-Z])(?=.*\d).{8,}$", password):
        message = "Password must have at least 8 characters, one uppercase letter and one number"  # noqa: E501
        logger.error(message)
        raise HTTPException(status_code=400, detail=message)
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode(
        "utf-8"
    )
    return hashed_password


def create_access_token(username: str) -> str:
    token_expiration = timedelta(minutes=config_app.access_token_expiration)
    expire = datetime.now(timezone.utc) + token_expiration

    data = {"sub": username, "exp": expire}
    return jwt.encode(
        data, config_app.secret_key, algorithm=config_app.algorithm
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token, config_app.secret_key, algorithms=[config_app.algorithm]
    )
