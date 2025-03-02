from fastapi import APIRouter, Request
from service.march_service import MarchService
from schema.marchs import MarchSchema

router = APIRouter(tags=["Marchs"], prefix="/marchs")


@router.get("", status_code=200)
async def get_marchs(request: Request):
    march_service: MarchService = request.state.march_service

    response = march_service.get_marchs()

    return response


@router.get("/{id}", status_code=200)
async def get_march_by_id(request: Request, id: int):
    march_service: MarchService = request.state.march_service

    response = march_service.get_march_by_id(id)

    return response


@router.post("", status_code=201)
async def create_march(request: Request, march_body: MarchSchema):
    march_service: MarchService = request.state.march_service

    response = march_service.create_march(march_body)

    return response


@router.delete("/{id}", status_code=204)
async def delete_march(request: Request, id: int):
    march_service: MarchService = request.state.march_service

    response = march_service.delete_march(id)

    return response


@router.post("/migrate/all", status_code=201)
async def migrate_all(request: Request):
    march_service: MarchService = request.state.march_service

    response = march_service.migrate_all()

    return response
