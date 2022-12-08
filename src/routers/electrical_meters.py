# 3rd party imports
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Local imports 
import crud
from schemas import ElectricalMeter, ElectricalMeterCreate, MeterReading, HTTPError
from database import get_db


# Create router for electrical meters
router = APIRouter(
    prefix="/electrical-meters",
    tags=["Electrical meters"],
    responses={404: {"description": "Not found"}}
)


@router.post(
    "/",
    response_model=ElectricalMeter,
    status_code=200,
    responses={400: {"model": HTTPError}}
)
def create_electrical_meter(
    electrical_meter: ElectricalMeterCreate, db: Session = Depends(get_db)):
    """
    Create a new electrical meter in database.
    """
    return crud.create_electrical_meter(db, electrical_meter=electrical_meter)


@router.get("/", response_model=list[ElectricalMeter])
def read_electrical_meters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Read all the electric meters in database.
    """
    return crud.read_electrical_meters(db, skip=skip, limit=limit)


@router.get(
    "/{electrical_meter_uid}", 
    response_model=ElectricalMeter,
    status_code=200,
    responses={404: {"model": HTTPError}}
)
def read_electrical_meter(electrical_meter_uid: int, db: Session = Depends(get_db)):
    """
    Read a specific electrical meter using its `uid`.
    """
    db_electrical_meter = crud.read_electrical_meter(db, uid=electrical_meter_uid)
    if db_electrical_meter is None:
        raise HTTPException(status_code=404, detail="Electrical meter not found")
    return db_electrical_meter


@router.get(
    "/{electrical_meter_uid}/readings", 
    response_model=list[MeterReading],
    status_code=200,
    responses={404: {"model": HTTPError}}
)
def read_factory_electrical_meters(electrical_meter_uid: int, db: Session = Depends(get_db)):
    """
    Read all the meter readings of a specific electrical meter using its `uid`.
    """
    db_electrical_meter = crud.read_electrical_meter(db, uid=electrical_meter_uid)
    if db_electrical_meter is None:
        raise HTTPException(status_code=404, detail="Electrical meter not found")
    return db_electrical_meter.readings.all()
