import pytest
from app.main import *

@pytest.mark.parametrize("brand, model, num_plate", [("BMW", "X3", "RMI12345"), ("MERCEDES-BENZ", "G CLASS", "KK 12343"), ("JEEP", "WRANGLER", "DBV123RV")])
def test_post_valid_vehicle(brand, model, num_plate, client):
    res = client.post(f"/vehicles/", json={"brand": brand, "model": model, "num_plate": num_plate})
    vehicle = schemas.VehicleCreate(**res.json())
    assert vehicle.model == model
    assert vehicle.brand == brand
    assert vehicle.num_plate == num_plate
    print(vehicle.id)
    assert isinstance(vehicle.id, int)
    assert res.status_code == 201

# def test_get_by_wrong_id():
#     assert get_vehicles_by_id()