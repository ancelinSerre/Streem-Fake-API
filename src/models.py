# 3rd party imports
from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Local imports
from database import Base


class EnergyProducer(Base):
    """
    Energy producer data model.
    Represents a company.
    An energy producer has multiple factories that produce electricity everyday.
    """
    __tablename__ = "energy_producers"

    uid = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    factories = relationship("Factory", back_populates="owner")

    def __repr__(self) -> str:
        return f"<EnergyProducer(name={self.name})>"


class Factory(Base):
    """
    Factory data model.
    A factory is composed of electrical meters.
    """
    __tablename__ = "factories"

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    owner_uid = Column(Integer, ForeignKey("energy_producers.uid"))

    owner = relationship("EnergyProducer", back_populates="factories")
    electrical_meters = relationship("ElectricalMeter", back_populates="factory")
    invoices = relationship("Invoice", back_populates="factory", lazy="dynamic")


    def __repr__(self) -> str:
        return f"<Factory(name={self.name}, owner={self.owner.name})>"


class Invoice(Base):
    """
    Invoice data model.
    Each energy producer can have multiple invoices, one per factory per month.
    """
    __tablename__ = "invoices"

    uid = Column(Integer, primary_key=True)
    date = Column(Date)
    production = Column(Float)
    price = Column(Float)
    factory_uid = Column(Integer, ForeignKey("factories.uid"))

    factory = relationship("Factory", back_populates="invoices")

    def __repr__(self) -> str:
        return (
            f"<Invoice("
            + f"factory_uid={self.factory_uid}, "
            + f"date={self.date}, "
            + f"production={self.production} kWh, "
            + f"price={self.price} €>"
        )


class ElectricalMeter(Base):
    """
    Electrical meter data model.
    Some consume electricity, some produce electricity.
    """
    __tablename__ = "electrical_meters"

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    is_producer = Column(Boolean, default=False)
    factory_uid = Column(Integer, ForeignKey("factories.uid"))

    factory = relationship("Factory", back_populates="electrical_meters")
    readings = relationship(
        "MeterReading", back_populates="electrical_meter", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<ElectricalMeter(name={self.name}, factory={self.factory.name})>"


class MeterReading(Base):
    """
    Electricity meter reading data model.
    Register amount of electricity produced or consumed everyday.
    """
    __tablename__ = "meter_readings"

    uid = Column(Integer, primary_key=True)
    date = Column(Date)
    amount = Column(Float)
    electrical_meter_uid = Column(Integer, ForeignKey("electrical_meters.uid"))

    electrical_meter = relationship("ElectricalMeter", back_populates="readings")

    def __repr__(self) -> str:
        return (
            f"<MeterReading("
            + f"factory={self.factory.name}, "
            + f"date={self.date}, "
            + f"production={self.production} kWh)>"
        )
