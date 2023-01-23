import pytest
from app.main import *
from app import schemas

@pytest.mark.parametrize("brand, model, num_plate", [("BMW", "X3", "RMI12345"), ("MERCEDES-BENZ", "G CLASS", "KK 12343"), ("JEEP", "WRANGLER", "DBV123RV")])
def test_post_valid_vehicle(brand, model, num_plate, client):
    res = client.post(f"/vehicles/", json={"brand": brand, "model": model, "num_plate": num_plate})
    vehicle = schemas.VehicleCreate(**res.json())
    assert vehicle.model == model
    assert vehicle.brand == brand
    assert vehicle.num_plate == num_plate
    assert isinstance(vehicle.id, int)
    assert res.status_code == 201

@pytest.mark.parametrize("brand, model, num_plate", [("BMW", None, "RMI12345"), (None, "G CLASS", "KK 12343"), (None, None, "DBV123RV")])
def test_post_vehicle_w_missing_values_v1(brand, model, num_plate, client):
    """ Testing by passing arguments with None value"""
    res = client.post("/vehicles/", json={"brand": brand, "model": model, "num_plate": num_plate})  #parameter with value None
    # res_v2 = client.post("/vehicles/", json={k: v for k, v in json_body.items() if v is not None}) #w/o entries
    vehicle = schemas.VehicleCreate(**res.json())

    assert vehicle.model == model
    assert vehicle.brand == brand
    assert vehicle.num_plate == num_plate
    assert isinstance(vehicle.id, int)
    assert res.status_code == 201


@pytest.mark.parametrize("brand, model, num_plate", [("BMW", None, "RMI12345"), (None, "G CLASS", "KK 12343"), (None, None, "DBV123RV")])
def test_post_vehicle_w_missing_values_v2(brand, model, num_plate, client):
    """ Testing w/o passing arguments where value is None"""
    json_body = {"brand": brand, "model": model, "num_plate": num_plate}
    res = client.post("/vehicles/", json={k: v for k, v in json_body.items() if v is not None}) #w/o parameter
    vehicle = schemas.VehicleCreate(**res.json())

    assert vehicle.model == model
    assert vehicle.brand == brand
    assert vehicle.num_plate == num_plate
    assert isinstance(vehicle.id, int)
    assert res.status_code == 201
    
@pytest.mark.parametrize("brand, model, num_plate", [("BMW", None, None), (None, "G CLASS", None), (None, None, None)])
def test_num_plate_missing(brand, model, num_plate, client):
    json_body = {"brand": brand, "model": model, "num_plate": num_plate}
    res_v1 = client.post("/vehicles/", json=json_body) #w parameter with value None
    res_v2 = client.post("/vehicles/", json={k: v for k, v in json_body.items() if v is not None}) #w/o parameter
    
    assert res_v1.status_code == 422
    assert res_v2.status_code == 422  #FIXME #maybe it should be 404 


@pytest.mark.parametrize("id", [99, 89])
def test_get_by_wrong_id(id, client):
    res = client.get(f'/vehicles/{id}')
    assert res.status_code == 404


@pytest.mark.parametrize("num_plate", ["RMI53079", "RMI12345", "RMI54321"])
def test_get_valid_by_num_plate(num_plate, vehicles, client):  # param order does not seem to have matter
    res = client.get(f"/vehicles/plates/{num_plate}")
    veh = schemas.VehicleResponse(**res.json())
    assert res.status_code == 200
    assert veh.num_plate == num_plate


@pytest.mark.parametrize("num_plate", ["1234", 313, "ssss"])
def test_get_invalid_by_num_plate(num_plate, client, vehicles):
    res = client.get(f"/vehicles/plates/{num_plate}")
    assert res.status_code == 404

@pytest.mark.parametrize("num_plate", ["RMI%2053079", "RMI 53079", "RMI    53079 "])
def test_get_valid_by_num_plate_with_spaces(num_plate: str, client, vehicles):
    res = client.get(f"/vehicles/plates/{num_plate}")
    # print(f"Type of response: {type(res)}")  <class 'requests...>
    # print(f"Type of query: {type(vehicles[0])}")  <class 'app.models.Vehicle'>
    # print(f"Type of res.json(): {type(res.json())}")  # <class 'dict'>
    veh = schemas.VehicleResponse(**res.json())  #res to jest obiekt klasy requests ktora ma .json()
    # natomiast vehicles jest klasy app.models.Vehicle
    assert veh.num_plate == vehicles[0].num_plate
    assert res.status_code == 200

@pytest.mark.parametrize("num_plate", ["RMI53079", "RMI54321"])
def test_post_duplicate_num_plate(num_plate, client, vehicles):
    res = client.post("/vehicles/", json={"num_plate": num_plate})
    assert res.status_code == 409
