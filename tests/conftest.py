import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import settings
from app import models
from app.main import app
from app.database import Base
from app.database import get_db

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
def client(session):
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
    return session.query(models.Vehicle).all()
