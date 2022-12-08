# Standard imports
import csv
import random 
from datetime import datetime, timedelta

# Local imports
import crud
from database import SessionLocal
from models import ElectricalMeter, MeterReading, EnergyProducer, Factory

random.seed(datetime.now().timestamp())


COMPANIES = [
    "CleanEnergy",
    "SolarPower",
    "EcoWind",
    "GreenAge",
    "InfinitPower",
    "FutureNRG"
]

factory_cities = []
with open("../data/cities.csv", "r", encoding="utf8") as fp:
    factory_cities = [row["name"] for row in csv.DictReader(fp, delimiter=",")]


def build_factory_name(company: str, city: str, idx: int) -> str:
    """
    Build a factory name with the following format: XX_YYY_Z
    - XX are the 2 upper case characters in the company name.
    - YYY are the first 3 letters in the city name.
    - Z is like an ID, it's useful because we could have more than one factory in a same city.
    """
    upper_case_company = "".join((c for c in company if c.isupper()))
    three_letters_city = city[:3]
    return f"{upper_case_company}_{three_letters_city}_{idx}"


def decision(probability):
    """
    Used to decide if an electrical meter is a producer or not
    """
    return random.random() < probability


def generate_fake_data():
    """
    Generate some fake data for the API using random.
    """

    db = SessionLocal()

    electrical_meters = []
    start_date = datetime.strptime("2022-01-01", "%Y-%m-%d")
    day_count = (datetime.now() - start_date).days

    for company in COMPANIES:
        # Step 1: Insert companies
        company_uid = crud.create_energy_producer(db, EnergyProducer(name=company)).uid

        # Step 2: Insert between 2 and 6 factories for each company
        nb_factories = random.choice(range(2, 7))
        for idx_f in range(nb_factories):
            city = random.choice(factory_cities)
            factory_name = build_factory_name(company, city, idx_f)
            factory_uid = crud.create_factory(db, Factory(
                name=factory_name,
                owner_uid=company_uid 
            )).uid

            # Step 3: Insert between 1 and 4 electrical meters for each factory
            nb_elec_meters = random.choice(range(1, 5))
            for idx_em in range(nb_elec_meters):
                em = crud.create_electrical_meter(db, ElectricalMeter(
                    name=f"{factory_name}_em{idx_em}",
                    is_producer=decision(0.8),  # 80% prob. to be a producer
                    factory_uid=factory_uid 
                ))
                electrical_meters.append(em)

    # Step 4: Insert a meter reading for each day from 01/01/2022 to now 
    # for each electrical meters
    for em in electrical_meters:
        # from 01/01/2022 to now  
        for single_date in (start_date + timedelta(n) for n in range(day_count)):
            crud.create_meter_reading(db, MeterReading(
                date=single_date.date(),
                amount=(
                    random.choice(range(1000)) if em.is_producer else random.choice(range(500))
                ),
                electrical_meter_uid=em.uid
            ))

    db.close()