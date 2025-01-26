from config.logging.logger import logger
from fastapi import APIRouter, Request, status
from service.hermandad_service import HermandadService
from schema.hermandades import UpdateHermandad

router = APIRouter(tags=["Hermandades"])


@router.get("/hermandades", status_code=status.HTTP_200_OK)
async def get_hermandades(request: Request):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.get_hermandades()
    logger.info("GET /hermandades HTTP/1.1 200 OK")
    return response


@router.get("/hermandades/day/{day}", status_code=status.HTTP_200_OK)
async def get_hermandad_by_day(request: Request, day: str):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.get_hermandad_by_day(day)
    logger.info(f"GET /hermandades/day/{day} HTTP/1.1 200 OK")
    return response


@router.get("/hermandades/{id}", status_code=status.HTTP_200_OK)
async def get_hermandad_by_id(request: Request, id: int):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.get_hermandad_by_id(id)
    logger.info(f"GET /hermandades/{id} HTTP/1.1 200 OK")
    return response


@router.patch("/hermandades/{id}", status_code=status.HTTP_201_CREATED)
async def update_hermandad(
    request: Request, id: int, hermandad_body: UpdateHermandad
):
    hermandad_service: HermandadService = request.state.hermandad_service

    response = hermandad_service.update_hermandad(id, hermandad_body)
    logger.info(f"PATCH /hermandades/{id} HTTP/1.1 201 Created")
    return response
