from fastapi import APIRouter, Request, Depends
from typing import Annotated
from schema.users import UserSchema
from service.user_service import UserService
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(tags=["Users"])


@router.post("/sign-up", status_code=201)
async def sign_up(request: Request, user: UserSchema):
    user_service: UserService = request.state.user_service

    response = user_service.sign_up(user)

    return response


@router.post("/login", status_code=200)
async def sign_in(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user_service: UserService = request.state.user_service

    response = user_service.sign_in(form_data)

    return response


@router.get("/users", status_code=200)
async def get_users(request: Request):
    user_service: UserService = request.state.user_service

    response = user_service.get_users()

    return response
