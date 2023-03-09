import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.settings import settings
from src import models
from src.main import app
from src.database import Base
from src.database import get_db
from src.logs import logger
from datetime import datetime

SQLALCHEMY_DATABASE_URL_TEST = f"postgresql://{settings().database_username}:{settings().database_password}@{settings().database_host}:{settings().database_port}/{settings().database_name}_tests"

engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)  # tworzymy silnik xd

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # database session

@pytest.fixture
def session():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):  #TODO: add type hinting
    # # run our code before we return our test
    # command.upgrade("head")
    def override_get_db():
        return session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)  # generuje po prostu obiekt taki sam jak w bibliotece response
    # command.downgrade("base")
    # Base.metadata.drop_all(bind=engine)
    # run out code after our test finished

@pytest.fixture
def vehicles(client, session):

    num_plate_list = ["RMI53079", "RMI12345", "RMI54321"]
    for num_plate in num_plate_list:
        res = client.post("/vehicles/", json={"brand": "BMW", "model": "X3", "num_plate": num_plate})
        assert res.status_code == 201
        logger.debug("added vehicles to the db")
    # logger.debug(f"{session.query(models.Vehicle).all}")
    return session.query(models.Vehicle).all()

# @pytest.fixture
# def users(session):
#     users = [{}]

@pytest.fixture
def events(vehicles, session):
    for _ in range(3):
        event = models.Event(vehicle_id=1)
        session.add(event)
        session.commit()
    

    