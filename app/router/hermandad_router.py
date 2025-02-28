from config.logging.logger import logger
from fastapi import APIRouter, Request, UploadFile, File
from service.hermandad_service import HermandadService
from schema.hermandades import UpdateHermandad
from models.hermandades import DayEnum
from typing import Optional

router = APIRouter(tags=["Hermandades"], prefix="/hermandades")


@router.get("", status_code=200)
async def get_hermandades(request: Request):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.get_hermandades()

    logger.info("GET /hermandades HTTP/1.1 200 OK")
    return response


@router.get("/day/{day}", status_code=200)
async def get_hermandad_by_day(request: Request, day: DayEnum):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.get_hermandad_by_day(day)

    logger.info(f"GET /hermandades/day/{day} HTTP/1.1 200 OK")
    return response


@router.get("/{id}", status_code=200)
async def get_hermandad_by_id(request: Request, id: int):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.get_hermandad_by_id(id)

    logger.info(f"GET /hermandades/{id} HTTP/1.1 200 OK")
    return response


@router.patch("/{id}", status_code=201)
async def update_hermandad(
    request: Request, id: int, hermandad_body: UpdateHermandad
):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.update_hermandad(id, hermandad_body)

    logger.info(f"PATCH /hermandades/{id} HTTP/1.1 201 Created")
    return response


@router.get("/{id}/shield", status_code=200)
async def get_hermandad_shield(request: Request, id: int):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.get_hermandad_shield(id)

    logger.info(f"GET /hermandades/{id}/shield HTTP/1.1 200 OK")
    return response


@router.get("/{id}/suit", status_code=200)
async def get_hermandad_suit(request: Request, id: int):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.get_hermandad_suit(id)

    logger.info(f"GET /hermandades/{id}/suit HTTP/1.1 200 OK")
    return response


@router.get("/prediction", status_code=200)
async def get_hermandad_prediction(
    request: Request,
    day: Optional[DayEnum] = None,
    img: UploadFile = File(...),
):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.run_prediction(day, img)

    logger.info("GET /prediction HTTP/1.1 200 OK")
    return response


@router.post("/populate/all", status_code=201)
async def populate_all_hermandades(request: Request):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.populate_all_hermandades()

    logger.info("POST /hermandades/populate/all HTTP/1.1 201 Created")
    return response


@router.post("/migrate/wiki", status_code=201)
async def migrate_wiki(
    request: Request, day: Optional[DayEnum] = None, id: Optional[int] = None
):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.migrate_wiki(day, id)

    logger.info("GET /hermandades/migrate/wiki HTTP/1.1 201 Created")
    return response
