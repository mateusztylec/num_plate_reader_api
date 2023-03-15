import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.settings import settings
from src.models import models
from src.main import app
from requests import Request
from src.oauth import verify_access_token
from src.database import Base
from src.role import Role
from src.database import get_db
from src.utils import get_password_hash
from src.logs import logger
from datetime import datetime
from src import schemas

SQLALCHEMY_DATABASE_URL_TEST = f"postgresql://{settings().database_username}:{settings().database_password}@{settings().database_host}:{settings().database_port}/{settings().database_name}_tests"

engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)  # tworzymy silnik xd

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)  # database session


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
def client(session):  # TODO: add type hinting
    # # run our code before we return our test
    # command.upgrade("head")
    def override_get_db():
        return session

    app.dependency_overrides[get_db] = override_get_db
    # generuje po prostu obiekt taki sam jak w bibliotece response
    yield TestClient(app)
    # command.downgrade("base")
    # Base.metadata.drop_all(bind=engine)
    # run out code after our test finished


@pytest.fixture
def vehicles(client, session):
    num_plate_list = ["RMI53079", "RMI12345", "RMI54321"]
    logger.debug("try add vehicle to db")
    for num_plate in num_plate_list:
        vehicle_schemas = schemas.VehicleBase(brand="BMW",
                                        model="X3",
                                        num_plate=num_plate)
        session.add(models.Vehicle(**vehicle_schemas.dict()))
        session.commit()
    return session.query(models.Vehicle).all()

def add_role_to_db(session):
    roles_list = Role.attributes()
    for single_role in roles_list:
        role = models.Role(role_name = single_role.name, id = single_role.id)
        session.add(role)
        session.commit()

@pytest.fixture
def user(session, client):
    add_role_to_db(session)
    logger.debug("Added role to db")
    user_role_admin = { "email": "user@gmail.com",
                        "name": "John",
                        "surname":"Kowalski",
                        "password": get_password_hash("Zaq12wsx"),
                        "role_id": Role.ADMIN.id}
    user = models.User(**user_role_admin)
    session.add(user)
    session.commit()
    logger.debug("added user to db")
    return user_role_admin

@pytest.fixture
def token(client: Request, user):
    logger.debug("trying to create otken")
    response = client.post("/users/login/", 
                          data={"username": user["email"],
                                "password": "Zaq12wsx"})
    if response.status_code >= 400:
        raise Exception("Invalid credentials!")
    else:
        response = schemas.Token(**response.json())
        logger.debug("token created")
        return response.access_token

@pytest.fixture
def authorized_user(client, token):
    logger.debug("trying to authorized_user")
    token_info = verify_access_token(token)
    logger.debug(token_info)
    logger.debug("token verified")
    client.headers = {**client.headers, 
                      "Authorization": f"Bearer {token}"}
    logger.debug(client.headers)
    return client

    
    


@pytest.fixture
def events(vehicles, session):
    for _ in range(3):
        event = models.Event(vehicle_id=1)
        session.add(event)
        session.commit()
