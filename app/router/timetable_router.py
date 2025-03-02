from fastapi import APIRouter, Request
from service.timetable_service import TimetableService
from schema.timetables import TimetableSchema

router = APIRouter(tags=["Timetables"], prefix="/timetables")


@router.get("", status_code=200)
def get_timetables(request: Request):
    timetable_service: TimetableService = request.state.timetable_service

    return timetable_service.get_timetables()


@router.get("/{id}", status_code=200)
def get_timetables_by_id(request: Request, id: int):
    timetable_service: TimetableService = request.state.timetable_service

    return timetable_service.get_timetables_by_id(id)


@router.get("/hermandades/{her_id}", status_code=200)
def get_timetables_by_hermandad(request: Request, her_id: int):
    timetable_service: TimetableService = request.state.timetable_service

    return timetable_service.get_timetables_by_hermandad(her_id)


@router.post("", status_code=201)
def create_timetable(request: Request, timetable_schema: TimetableSchema):
    timetable_service: TimetableService = request.state.timetable_service

    return timetable_service.create_timetable(timetable_schema)


@router.delete("/{id}", status_code=200)
def delete_timetable(request: Request, id: int):
    timetable_service: TimetableService = request.state.timetable_service

    return timetable_service.delete_timetable(id)


@router.post("/migrate/all", status_code=200)
def migrate_all(request: Request):
    timetable_service: TimetableService = request.state.timetable_service

    return timetable_service.migrate_all_timetables()
