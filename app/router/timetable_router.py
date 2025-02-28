from config.logging.logger import logger
from fastapi import APIRouter, Request
from service.timetable_service import TimetableService
from schema.timetables import TimetableSchema
from models.hermandades import DayEnum

router = APIRouter(tags=["Timetables"], prefix="/timetables")


@router.get("", status_code=200)
def get_timetables(request: Request):
    timetable_service: TimetableService = request.state.timetable_service

    logger.info("GET /timetables HTTP/1.1 200 OK")
    return timetable_service.get_timetables()


@router.get("/{id}", status_code=200)
def get_timetables_by_id(request: Request, id: int):
    timetable_service: TimetableService = request.state.timetable_service

    logger.info(f"GET /timetables/{id} HTTP/1.1 200 OK")
    return timetable_service.get_timetables_by_id(id)


@router.get("/hermandades/{her_id}", status_code=200)
def get_timetables_by_hermandad(request: Request, her_id: int):
    timetable_service: TimetableService = request.state.timetable_service

    logger.info(f"GET /timetables/hermandades/{her_id} HTTP/1.1 200 OK")
    return timetable_service.get_timetables_by_hermandad(her_id)


@router.post("", status_code=201)
def create_timetable(request: Request, timetable_schema: TimetableSchema):
    timetable_service: TimetableService = request.state.timetable_service

    logger.info("POST /timetables HTTP/1.1 201 Created")
    return timetable_service.create_timetable(timetable_schema)


@router.delete("/{id}", status_code=200)
def delete_timetable(request: Request, id: int):
    timetable_service: TimetableService = request.state.timetable_service

    logger.info(f"DELETE /timetables/{id} HTTP/1.1 200 OK")
    return timetable_service.delete_timetable(id)


@router.post("/migrate/all", status_code=200)
def migrate_all(request: Request):
    timetable_service: TimetableService = request.state.timetable_service

    logger.info("POST /timetables/migrate/all HTTP/1.1 200 OK")
    return timetable_service.migrate_all_timetables()


@router.post("/migrate/day/{day}", status_code=200)
def migrate_day(request: Request, day: DayEnum):
    timetable_service: TimetableService = request.state.timetable_service

    logger.info(f"POST /timetables/migrate/day/{day} HTTP/1.1 200 OK")
    return timetable_service.migrate_day_timetables(day)


@router.post("/migrate/hermandad/{her_id}", status_code=200)
def migrate_hermandad(request: Request, her_id: int):
    timetable_service: TimetableService = request.state.timetable_service

    logger.info(f"POST /timetables/migrate/hermandad/{her_id} HTTP/1.1 200 OK")
    return timetable_service.migrate_hermandad_timetables(her_id)
