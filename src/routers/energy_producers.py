# Standard imports
from datetime import datetime

# 3rd party imports
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import extract
from sqlalchemy.orm import Session

# Local imports 
import crud
from database import get_db
from schemas import EnergyProducer, EnergyProducerCreate, Factory, Invoice, HTTPError
from utils import compute_invoice

import models

# Create router for energy producers
router = APIRouter(
    prefix="/energy-producers",
    tags=["Energy producers"],
    responses={404: {"description": "Not found"}}
)


@router.post(
    "/",
    response_model=EnergyProducer,
    status_code=200,
    responses={400: {"model": HTTPError}}
)
def create_energy_producer(
    energy_producer: EnergyProducerCreate, db: Session = Depends(get_db)):
    """
    Create a new energy producer in database.
    """
    db_energy_producer = crud.read_energy_producer_by_name(db, name=energy_producer.name)
    if db_energy_producer:
        raise HTTPException(status_code=400, detail="Energy producer already registered")
    
    return crud.create_energy_producer(db, energy_producer=energy_producer)


@router.get("/", response_model=list[EnergyProducer])
def read_energy_producers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Read all energy producers in database.
    """
    return crud.read_energy_producers(db, skip=skip, limit=limit)


@router.get(
    "/{energy_producer_uid}", 
    response_model=EnergyProducer,
    status_code=200,
    responses={404: {"model": HTTPError}}
)
def read_energy_producer(energy_producer_uid: int, db: Session = Depends(get_db)):
    """
    Read a specific energy producer using its `uid`.
    """
    db_energy_producer = crud.read_energy_producer(db, uid=energy_producer_uid)
    if db_energy_producer is None:
        raise HTTPException(status_code=404, detail="Energy producer not found")
    return db_energy_producer


@router.get(
    "/{energy_producer_uid}/factories", 
    response_model=list[Factory],
    status_code=200,
    responses={404: {"model": HTTPError}}
)
def read_energy_producer_factories(energy_producer_uid: int, db: Session = Depends(get_db)):
    """
    Read all the factories of a specific energy producer using its `uid`.
    """
    db_energy_producer = crud.read_energy_producer(db, uid=energy_producer_uid)
    if db_energy_producer is None:
        raise HTTPException(status_code=404, detail="Energy producer not found")
    return db_energy_producer.factories


@router.get(
    "/{energy_producer_uid}/invoices", 
    response_model=list[Invoice] | list,
    status_code=200,
    responses={404: {"model": HTTPError}}
)
def read_energy_producer_invoices(energy_producer_uid: int, db: Session = Depends(get_db)):
    """
    Read all the invoices of a specific energy producer using its `uid`.
    """
    db_energy_producer = crud.read_energy_producer(db, uid=energy_producer_uid)
    if db_energy_producer is None:
        raise HTTPException(status_code=404, detail="Energy producer not found")

    db_factories = db_energy_producer.factories
    invoices = []
    for db_factory in db_factories:
        invoices = [*invoices, *db_factory.invoices]

    return invoices

@router.get(
    "/{energy_producer_uid}/invoices/{year}/{month}", 
    response_model=list[Invoice],
    status_code=200,
    responses={400: {"model": HTTPError}}
)
def read_energy_producer_invoice_at_date(
    energy_producer_uid: int, 
    year: int, 
    month: int, 
    db: Session = Depends(get_db)):
    """
    Read the invoice of a specific `date` for a specific energy producer using its `uid`.
    """
    db_energy_producer = crud.read_energy_producer(db, uid=energy_producer_uid)
    if db_energy_producer is None:
        raise HTTPException(status_code=404, detail="Energy producer not found")

    if year < 1900:
        raise HTTPException(status_code=400, detail="Year can't be < 1900")
    
    if not 1 <= month <= 12:
        raise HTTPException(status_code=400, detail="Month must be in range [1, 12]")

    custom_date = datetime.strptime(f"{year}-{month}", "%Y-%m")
    db_factories = db_energy_producer.factories
    invoices = []
    for factory in db_factories:
        db_invoice = factory.invoices.filter(
            extract("year", models.Invoice.date) == custom_date.year,
            extract("month", models.Invoice.date) == custom_date.month 
        ).first()
        if db_invoice is None:
            invoice = compute_invoice(db, factory_uid=factory.uid, date=custom_date)
            db_invoice = crud.create_invoice(db, invoice=invoice)

        invoices.append(db_invoice)

    return invoices