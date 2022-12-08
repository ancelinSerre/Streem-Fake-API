# Standard imports
from datetime import datetime

# 3rd party imports
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Local imports 
import crud
from schemas import Invoice, HTTPError
from database import get_db


# Create router for invoices
router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=list[Invoice])
def read_invoices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Read all the invoices in database.
    """
    return crud.read_invoices(db, skip=skip, limit=limit)


@router.get(
    "/{invoice_uid}", 
    response_model=Invoice,
    status_code=200,
    responses={404: {"model": HTTPError}}
)
def read_invoice(invoice_uid: int, db: Session = Depends(get_db)):
    """
    Read a specific invoice using its `uid`.
    """
    db_invoice = crud.read_invoice(db, uid=invoice_uid)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return db_invoice


@router.get(
    "/{year}/{month}", 
    response_model=list[Invoice],
    status_code=200,
    responses={400: {"model": HTTPError}}
)
def read_invoices_by_date(
    year: int,
    month: int, 
    skip: int = 0,
    limit: int = 100, 
    db: Session = Depends(get_db)):
    """
    Read all the invoices for a specific `date`.
    """
    if year < 1900:
        raise HTTPException(status_code=400, detail="Year can't be < 1900")
    
    if not 1 <= month <= 12:
        raise HTTPException(status_code=400, detail="Month must be in range [1, 12]")
    custom_date = datetime.strptime(f"{year}-{month}", "%Y-%m")
    return crud.read_invoices(db, skip=skip, limit=limit, date=custom_date)
