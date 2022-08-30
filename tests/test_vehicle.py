import pytest
from app.main import *

@pytest.mark.parametrize("brand, model, num_plate", [("BMW", "X3", "RMI12345"), ("MERCEDES-BENZ", "G CLASS", "KK 12343"), ("JEEP", "WRANGLER", "DBV123RV")])
def test_post_valid_vehicle(brand, model, num_plate, client):
    res = client.post(f"/vehicles/", json={"brand": brand, "model": model, "num_plate": num_plate})
    vehicle = schemas.VehicleCreate(**res.json())
    assert vehicle.model == model
    assert vehicle.brand == brand
    assert vehicle.num_plate == num_plate
    assert isinstance(vehicle.id, int)
    assert res.status_code == 201


@pytest.mark.parametrize("id", [99, 89])
def test_get_by_wrong_id(id, client):
    res = client.get(f'/vehicles/{id}')
    assert res.status_code == 404


@pytest.mark.parametrize("num_plate", ["RMI53079", "RMI12345", "RMI54321"])
def test_get_valid_by_num_plate(num_plate, vehicles, client):  # param order does not seem to have matter
    res = client.get(f"/vehicles/plates/{num_plate}")
    veh = schemas.Vehicle(**res.json())
    assert res.status_code == 200
    assert veh.num_plate == num_plate


@pytest.mark.parametrize("num_plate", ["1234", 313, "ssss"])
def test_get_invalid_by_num_plate(num_plate, client, vehicles):
    res = client.get(f"/vehicles/plates/{num_plate}")
    assert res.status_code == 404

@pytest.mark.parametrize("num_plate", ["RMI%2053079", "RMI 12345", "RMI    54321 "])
def test_get_valid_by_num_plate_with_spaces(num_plate, client, vehicles):
    res = client.get(f"/vehicles/plates/{num_plate}")
    veh = schemas.Vehicle(**res.json())
    print(res.json())
    assert veh.num_plate == vehicles
    assert res.status_code == 200

