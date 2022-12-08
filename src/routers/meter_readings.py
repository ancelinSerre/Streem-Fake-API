# 3rd party imports
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Local imports 
import crud
from schemas import MeterReading, MeterReadingCreate, HTTPError
from database import get_db


# Create router for electrical meters
router = APIRouter(
    prefix="/meter-readings",
    tags=["Electricity meter readings"],
    responses={404: {"description": "Not found"}}
)


@router.post(
    "/",
    response_model=MeterReading,
    status_code=200,
    responses={400: {"model": HTTPError}}
)
def create_meter_reading(
    meter_reading: MeterReadingCreate, db: Session = Depends(get_db)):
    """
    Create a new meter reading in database.
    """
    return crud.create_meter_reading(db, meter_reading=meter_reading)


@router.get("/", response_model=list[MeterReading])
def read_meter_readings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Read all the meter readings in database.
    """
    return crud.read_meter_readings(db, skip=skip, limit=limit)


@router.get(
    "/{meter_reading_uid}", 
    response_model=MeterReading,
    status_code=200,
    responses={404: {"model": HTTPError}}
)
def read_meter_reading(meter_reading_uid: int, db: Session = Depends(get_db)):
    """
    Read a specific meter reading using its `uid`.
    """
    db_meter_reading = crud.read_meter_reading(db, uid=meter_reading_uid)
    if db_meter_reading is None:
        raise HTTPException(status_code=404, detail="Meter reading not found")
    return db_meter_reading


@router.get(
    "/{year}/", 
    response_model=list[MeterReading],
    status_code=200,
    responses={400: {"model": HTTPError}}
)
def read_meter_readings_by_year(
    year: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)):
    """
    Read all the meter readings for a specific `year`.
    """
    if year < 1900:
        raise HTTPException(status_code=400, detail="Year can't be < 1900")

    return crud.read_meter_readings(
        db, skip=skip, limit=limit, year=year
    )


@router.get(
    "/{year}/{month}", 
    response_model=list[MeterReading],
    status_code=200,
    responses={400: {"model": HTTPError}}
)
def read_meter_readings_by_month(
    year: int,
    month: int,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)):
    """
    Read all the meter readings for a specific `month`.
    """
    if year < 1900:
        raise HTTPException(status_code=400, detail="Year can't be < 1900")

    if not 1 <= month <= 12:
        raise HTTPException(status_code=400, detail="Month must be in range [1, 12]")

    return crud.read_meter_readings(
        db, skip=skip, limit=limit, year=year, month=month
    )


@router.get(
    "/{year}/{month}/{day}", 
    response_model=list[MeterReading],
    status_code=200,
    responses={400: {"model": HTTPError}}
)
def read_meter_readings_by_day(
    year: int,
    month: int,
    day: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)):
    """
    Read all the meter readings for a specific `day`.
    """
    if year < 1900:
        raise HTTPException(status_code=400, detail="Year can't be < 1900")

    if not 1 <= month <= 12:
        raise HTTPException(status_code=400, detail="Month must be in range [1, 12]")

    if not 1 <= day <= 31:
        raise HTTPException(status_code=400, detail="Day must be in range [1, 31]")

    return crud.read_meter_readings(
        db, skip=skip, limit=limit, year=year, month=month, day=day
    )
