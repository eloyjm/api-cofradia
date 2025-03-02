from fastapi import APIRouter, Request, UploadFile, File, Depends
from service.hermandad_service import HermandadService
from schema.hermandades import UpdateHermandad
from models.hermandades import DayEnum
from typing import Optional
from config.app import config_app

router = APIRouter(tags=["Hermandades"], prefix="/hermandades")


@router.get("", status_code=200)
async def get_hermandades(request: Request):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.get_hermandades()

    return response


@router.get("/day/{day}", status_code=200)
async def get_hermandad_by_day(request: Request, day: DayEnum):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.get_hermandad_by_day(day)

    return response


@router.get("/{id}", status_code=200)
async def get_hermandad_by_id(request: Request, id: int):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.get_hermandad_by_id(id)

    return response


@router.patch("/{id}", status_code=201)
async def update_hermandad(
    request: Request, id: int, hermandad_body: UpdateHermandad
):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.update_hermandad(id, hermandad_body)

    return response


@router.get("/{id}/shield", status_code=200)
async def get_hermandad_shield(request: Request, id: int):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.get_hermandad_shield(id)

    return response


@router.get("/{id}/suit", status_code=200)
async def get_hermandad_suit(request: Request, id: int):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.get_hermandad_suit(id)

    return response


@router.post("/prediction", status_code=200)
async def hermandad_prediction(
    request: Request,
    day: Optional[DayEnum] = None,
    img: UploadFile = File(...),
):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = await hermandad_service.run_prediction(day, img)

    return response


@router.post("/populate/all", status_code=201)
async def populate_all_hermandades(
    request: Request, oauth=Depends(config_app.oauth2_scheme)
):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.populate_all_hermandades()

    return response


@router.post("/migrate/wiki", status_code=201)
async def migrate_wiki(
    request: Request,
    day: Optional[DayEnum] = None,
    id: Optional[int] = None,
    oauth=Depends(config_app.oauth2_scheme),
):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.migrate_wiki(day, id)

    return response
