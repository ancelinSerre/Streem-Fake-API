# Standard imports
from datetime import datetime, timedelta

# 3rd party imports
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local imports
from app import app
from crud import create_invoice
from database import Base, get_db
from utils import compute_invoice

SQLALCHEMY_DATABASE_URL = "sqlite:///./database/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_energy_producer():
    response = client.post(
        "/energy-producers/",
        json={"name": "edf"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "edf"
    assert "uid" in data
    energy_producer_uid = data["uid"]

    response = client.get(f"/energy-producers/{energy_producer_uid}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "edf"
    assert data["uid"] == energy_producer_uid


def test_create_factory():
    response = client.post(
        "/factories/",
        json={"name": "ED_Cha_1", "owner_uid": 1},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "ED_Cha_1"
    assert data["owner_uid"] == 1
    assert "uid" in data
    factory_uid = data["uid"]

    response = client.get(f"/factories/{factory_uid}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "ED_Cha_1"
    assert data["owner_uid"] == 1
    assert data["uid"] == factory_uid


def test_electrical_meter():
    response = client.post(
        "/electrical-meters/",
        json={"name": "ED_Cha_1_em1", "is_producer": True, "factory_uid": 1},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "ED_Cha_1_em1"
    assert data["is_producer"] == True
    assert data["factory_uid"] == 1
    assert "uid" in data
    electrical_meter_uid = data["uid"]

    response = client.get(f"/electrical-meters/{electrical_meter_uid}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "ED_Cha_1_em1"
    assert data["is_producer"] == True
    assert data["factory_uid"] == 1
    assert data["uid"] == electrical_meter_uid


def test_meter_reading():
    curr_date = str(datetime.now().date())
    response = client.post(
        "/meter-readings/",
        json={"date": curr_date, "amount": 100, "electrical_meter_uid": 1},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["date"] == curr_date
    assert data["amount"] == 100
    assert data["electrical_meter_uid"] == 1
    assert "uid" in data
    reading_uid = data["uid"]

    response = client.get(f"/meter-readings/{reading_uid}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["date"] == curr_date
    assert data["amount"] == 100
    assert data["electrical_meter_uid"] == 1
    assert data["uid"] == reading_uid


def test_invoice():
    # Add other electrical meters to the only factory
    client.post(
        "/electrical-meters/",
        json={"name": "ED_Cha_1_em2", "is_producer": False, "factory_uid": 1},
    )
    client.post(
        "/electrical-meters/",
        json={"name": "ED_Cha_1_em3", "is_producer": True, "factory_uid": 1},
    )
    # Add some meter readings...
    curr_date = datetime.now().date()
    for x, amt in enumerate([100, 200, 300, 400]):
        tmp_date = curr_date + timedelta(days=x)
        for uid in range(1, 4):
            client.post(
                "/meter-readings/",
                json={"date": str(tmp_date), "amount": amt, "electrical_meter_uid": uid},
            )

    db = TestingSessionLocal()
    invoice = compute_invoice(
        db, factory_uid=1, date=datetime.strptime("2022-12-01", "%Y-%m-%d").date())
    db_invoice = create_invoice(db, invoice)
    assert db_invoice.date == invoice.date
    assert db_invoice.factory_uid == invoice.factory_uid
    assert db_invoice.production == invoice.production
    assert db_invoice.production == 1100
    assert db_invoice.price == invoice.price
    assert db_invoice.price == 550
    db.close()
