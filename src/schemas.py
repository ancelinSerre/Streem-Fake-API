"""
Schemas used for data validation
"""
# Standard imports
import datetime
from typing import Any

# 3rd party imports
from pydantic import BaseModel


# -------------- Energy Producers

class EnergyProducerBase(BaseModel):
    name: str

class EnergyProducerCreate(EnergyProducerBase):
    pass   

class EnergyProducer(EnergyProducerBase):
    uid: int
    
    class Config:
        orm_mode = True

# -------------- Electrical Meters

class ElectricalMeterBase(BaseModel):
    name: str
    is_producer: bool
    factory_uid: int

class ElectricalMeterCreate(ElectricalMeterBase):
    pass

class ElectricalMeter(ElectricalMeterBase):
    uid: int

    class Config:
        orm_mode = True

# -------------- Electricity Meter Reading

class MeterReadingBase(BaseModel):
    date: datetime.date
    amount: float
    electrical_meter_uid: int

class MeterReadingCreate(MeterReadingBase):
    pass

class MeterReading(MeterReadingBase):
    uid: int

    class Config:
        orm_mode = True

# -------------- Factories

class FactoryBase(BaseModel):
    name: str
    owner_uid: int

class FactoryCreate(FactoryBase):
    pass

class Factory(FactoryBase):
    uid: int

    class Config:
        orm_mode = True

# -------------- Invoices

class InvoiceBase(BaseModel):
    date: datetime.date
    factory_uid: int

class InvoiceCreate(InvoiceBase):
    production: float
    price: float

class Invoice(InvoiceCreate):
    uid: int

    class Config:
        orm_mode = True

# -------------- Errors

class HTTPError(BaseModel):
    detail: str
