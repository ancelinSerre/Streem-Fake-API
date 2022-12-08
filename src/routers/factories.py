# Standard imports
from datetime import datetime

# 3rd party imports
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import extract
from sqlalchemy.orm import Session

# Local imports 
import crud
import models
from database import get_db
from schemas import ElectricalMeter, Factory, FactoryCreate, Invoice, HTTPError
from utils import compute_invoice

# Create router for factories
router = APIRouter(
    prefix="/factories",
    tags=["Factories"],
    responses={404: {"description": "Not found"}}
)


@router.post(
    "/",
    response_model=Factory,
    status_code=200,
    responses={400: {"model": HTTPError}}
)
def create_factory(
    factory: FactoryCreate, db: Session = Depends(get_db)):
    """
    Create a new factory in database.
    """
    return crud.create_factory(db, factory=factory)


@router.get("/", response_model=list[Factory])
def read_factories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Read all the factories in database.
    """
    return crud.read_factories(db, skip=skip, limit=limit)


@router.get(
    "/{factory_uid}", 
    response_model=Factory,
    status_code=200,
    responses={404: {"model": HTTPError}}
)
def read_factory(factory_uid: int, db: Session = Depends(get_db)):
    """
    Read a specific factory using its `uid`.
    """
    db_factory = crud.read_factory(db, uid=factory_uid)
    if db_factory is None:
        raise HTTPException(status_code=404, detail="Factory not found")
    return db_factory


@router.get(
    "/{factory_uid}/electrical-meters", 
    response_model=list[ElectricalMeter],
    status_code=200,
    responses={404: {"model": HTTPError}}
)
def read_factory_electrical_meters(factory_uid: int, db: Session = Depends(get_db)):
    """
    Read all the electric meters of a specific factory using its `uid`.
    """
    db_factory = crud.read_factory(db, uid=factory_uid)
    if db_factory is None:
        raise HTTPException(status_code=404, detail="Factory not found")
    return db_factory.electrical_meters


@router.get(
    "/{factory_uid}/invoices", 
    response_model=list[Invoice],
    status_code=200,
    responses={404: {"model": HTTPError}}
)
def read_factory_invoices(factory_uid: int, db: Session = Depends(get_db)):
    """
    Read all the invoices of a specific factory using its `uid`.
    """
    db_factory = crud.read_factory(db, uid=factory_uid)
    if db_factory is None:
        raise HTTPException(status_code=404, detail="Factory not found")
    return db_factory.invoices.all()

@router.get(
    "/{factory_uid}/invoices/{year}/{month}", 
    response_model=Invoice,
    status_code=200,
    responses={404: {"model": HTTPError}}
)
def read_factory_invoice_at_date(
    factory_uid: int, 
    year: int, 
    month: int, 
    db: Session = Depends(get_db)):
    """
    Read the invoice of a specific `year` and `month` for a specific factory using its `uid`.
    """
    db_factory = crud.read_factory(db, uid=factory_uid)
    if db_factory is None:
        raise HTTPException(status_code=404, detail="Factory not found")

    if year < 1900:
        raise HTTPException(status_code=400, detail="Year can't be < 1900")
    
    if not 1 <= month <= 12:
        raise HTTPException(status_code=400, detail="Month must be in range [1, 12]")

    
    custom_date = datetime.strptime(f"{year}-{month}", "%Y-%m")
    invoice = db_factory.invoices.filter(
        extract("year", models.Invoice.date) == custom_date.year,
        extract("month", models.Invoice.date) == custom_date.month 
    ).first()
    if invoice is None:
        # Call function to create an invoice
        # Use a fixed price for 1 kWh produced
        invoice = compute_invoice(db, factory_uid=factory_uid, date=custom_date)
        return crud.create_invoice(db, invoice=invoice)

    return invoice