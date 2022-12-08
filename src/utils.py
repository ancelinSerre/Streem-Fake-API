# Standard imports
import datetime

# 3rd party imports
from sqlalchemy import extract
from sqlalchemy.orm import Session

# Local imports
from crud import read_energy_producer, read_factory
from models import MeterReading, Invoice


PRICE_PER_KWH = 0.5  # Constant price for 1 kWh produced (in €)


def compute_invoice(db: Session, factory_uid: int, date: datetime.date) -> Invoice:
    """
    Compute an invoice for a factory at a specific date.
    We assume that the price per kWh is a fixed amount every day (0.5€/kWh)
    Using this function, an invoice might be created with a production of 0 kWh.
    """
    electricity_produced = 0
    factory = read_factory(db, factory_uid)
    if factory is None:
        raise ValueError("Factory not found")
    
    electrical_meters = factory.electrical_meters
    # There we want to sum all the electrical productions of each electrical meters at a
    # given date for each factory owned by the energy producer
    for elec_meter in electrical_meters:
        # Get the all the readings for the given month
        meter_readings = elec_meter.readings.filter(
            extract("year", MeterReading.date) == date.year,
            extract("month", MeterReading.date) == date.month
        ).all()
        # Sum each electricity meter readings
        for mr in meter_readings:
            # Set a default value (0) for production if it's None
            reading = mr.amount if mr is not None else 0
            # Handle case where there is one or many electrical meters that consume energy.
            # In this case, we need to substract the 'amount' value as it is a consumption.
            electricity_produced += reading if elec_meter.is_producer else (reading * -1)

    return Invoice(
        date=date,
        production=electricity_produced,  # in kWh
        price=electricity_produced * PRICE_PER_KWH,  # in €
        factory_uid=factory_uid
    )
