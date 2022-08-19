import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.settings import settings
from app.main import app, get_db
from app.database import Base

SQLALCHEMY_DATABASE_URL_TEST = f"postgresql://{settings().database_username}:{settings().database_password}@{settings().database_host}:{settings().database_port}/{settings().database_name}_tests"

engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST) # tworzymy silnik xd

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