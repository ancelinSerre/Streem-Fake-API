# Standard imports
from datetime import date

# 3rd party imports
from fastapi.logger import logger
from sqlalchemy import extract
from sqlalchemy.orm import Session

# Local imports
import schemas
from models import (
    ElectricalMeter,
    MeterReading,
    EnergyProducer,
    Factory,
    Invoice
)

# -------------- Energy Producers

def read_energy_producer(db: Session, uid: int):
    """
    Read a specific energy producer using its `uid`.
    """
    return db.query(EnergyProducer).filter(EnergyProducer.uid == uid).first()

def read_energy_producer_by_name(db: Session, name: str):
    """
    Read a specific energy producer using its `name`.
    """
    return db.query(EnergyProducer).filter(EnergyProducer.name == name).first()

def read_energy_producers(db: Session, skip: int = 0, limit: int = 100):
    """
    Read all the energy producers in database.
    """
    return db.query(EnergyProducer).offset(skip).limit(limit).all()

def create_energy_producer(db: Session, energy_producer: schemas.EnergyProducerCreate):
    """
    Create a new energy producer in database.
    """
    db_energy_producer = EnergyProducer(name=energy_producer.name)
    db.add(db_energy_producer)
    db.commit()
    db.refresh(db_energy_producer)
    logger.debug("Energy producer created: %s", db_energy_producer)
    return db_energy_producer

# -------------- Factories

def read_factory(db: Session, uid: int):
    """
    Read a specific factory using its `uid`.
    """
    return db.query(Factory).filter(Factory.uid == uid).first()

def read_factories(db: Session, skip: int = 0, limit: int = 100):
    """
    Read all the factories in database.
    """
    return db.query(Factory).offset(skip).limit(limit).all()

def create_factory(db: Session, factory: schemas.FactoryCreate):
    """
    Create a new factory in database.
    """
    db_factory = Factory(name=factory.name, owner_uid=factory.owner_uid)  
    db.add(db_factory)
    db.commit()
    db.refresh(db_factory)
    logger.debug("Factory created: %s", db_factory)
    return db_factory

# -------------- Electrical Meters

def read_electrical_meter(db: Session, uid: int):
    """
    Read a specific electrical meter using its `uid`.
    """
    return db.query(ElectricalMeter).filter(ElectricalMeter.uid == uid).first()

def read_electrical_meters(db: Session, skip: int = 0, limit: int = 100):
    """
    Read all the electrical meters in database.
    """
    return db.query(ElectricalMeter).offset(skip).limit(limit).all()

def create_electrical_meter(db: Session, electrical_meter: schemas.ElectricalMeterCreate):
    """
    Create a new electrical meter in database.
    """
    db_electrical_meter = ElectricalMeter(
        name=electrical_meter.name,
        is_producer=electrical_meter.is_producer,
        factory_uid=electrical_meter.factory_uid
    )
    db.add(db_electrical_meter)
    db.commit()
    db.refresh(db_electrical_meter)
    logger.debug("Electrical meter created: %s", db_electrical_meter)
    return db_electrical_meter

# -------------- Meter readings

def read_meter_reading(db: Session, uid: int):
    """
    Read a specific meter reading using its `uid`.
    """
    return db.query(MeterReading).filter(MeterReading.uid == uid).first()

def read_meter_readings(
    db: Session,
    year: int = None,
    month: int = None,
    day: int = None,
    skip: int = 0,
    limit: int = 100):
    """
    Read all the meter readings in database.
    """
    if year is not None:
        if month is not None:
            if day is not None:
                # Full date case
                return db.query(MeterReading).filter(
                    extract("year", MeterReading.date) == year,
                    extract("month", MeterReading.date) == month,
                    extract("day", MeterReading.date) == day
                ).offset(skip).limit(limit).all()

            # Month case
            return db.query(MeterReading).filter(
                extract("year", MeterReading.date) == year,
                extract("month", MeterReading.date) == month
            ).offset(skip).limit(limit).all()

        # Default case, only year
        return db.query(MeterReading).filter(
            extract("year", MeterReading.date) == year
        ).offset(skip).limit(limit).all()

    return db.query(MeterReading).offset(skip).limit(limit).all()

def create_meter_reading(
    db: Session, meter_reading: schemas.MeterReadingCreate):
    """
    Create a new electrical production in database.
    """
    db_meter_reading = MeterReading(
        date=meter_reading.date,
        amount=meter_reading.amount,
        electrical_meter_uid=meter_reading.electrical_meter_uid
    )
    db.add(db_meter_reading)
    db.commit()
    db.refresh(db_meter_reading)
    logger.debug("Meter reading created: %s", db_meter_reading)
    return db_meter_reading

# -------------- Invoices

def read_invoice(db: Session, uid: int):
    """
    Read a specific invoice using its `uid`.
    """
    return db.query(Invoice).filter(Invoice.uid == uid).first()

def read_invoices(
    db: Session, skip: int = 0, limit: int = 100, date: date = None):
    """
    Read all the invoices in database.
    """
    if date is not None:
        return db.query(Invoice).filter(
            extract("month", Invoice.date) == date.month
        ).offset(skip).limit(limit).all()

    return db.query(Invoice).offset(skip).limit(limit).all()

def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    """
    Create a new invoice in database.
    """
    db_invoice = Invoice(
        date=invoice.date,
        production=invoice.production,
        price=invoice.price,
        factory_uid=invoice.factory_uid
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    logger.debug("Invoice created: %s", db_invoice)
    return db_invoice
