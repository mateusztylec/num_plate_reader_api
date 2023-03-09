import pytest
from src.main import *
from src import schemas
from src.logs import logger


@pytest.mark.parametrize("brand, model, num_plate", [("BMW", "X3", "RMI12345"), ("MERCEDES-BENZ", "G CLASS", "KK 12343"), ("JEEP", "WRANGLER", "DBV123RV")])
def test_post_valid_vehicle(brand, model, num_plate: str, client):
    res = client.post(f"/vehicles/", json={"brand": brand, "model": model, "num_plate": num_plate})
    vehicle = schemas.VehicleCreate(**res.json())  # rozpakowywujemy response na key=value wartosci
    assert vehicle.model == model
    assert vehicle.brand == brand
    assert vehicle.num_plate == num_plate.replace(" ","")
    assert isinstance(vehicle.id, int)
    assert res.status_code == 201

@pytest.mark.parametrize("brand, model, num_plate", [("BMW", None, "RMI12345"), (None, "G CLASS", "KK 12343"), (None, None, "DBV123RV")])
def test_post_w_missing_values_v1(brand, model, num_plate, client):
    """ Testing by passing arguments with None value"""
    res = client.post("/vehicles/", json={"brand": brand, "model": model, "num_plate": num_plate})  #parameter with value None
    # res_v2 = client.post("/vehicles/", json={k: v for k, v in json_body.items() if v is not None}) #w/o entries
    vehicle = schemas.VehicleCreate(**res.json())

    assert vehicle.model == model
    assert vehicle.brand == brand
    assert vehicle.num_plate == num_plate.replace(" ","")
    assert isinstance(vehicle.id, int)
    assert res.status_code == 201

def test_post_with_empty_num_plate_sting(client):
    res = client.post("/vehicles/", json={"num_plate": "", "brand": "BMw"})
    assert res.status_code == 422

@pytest.mark.parametrize("brand, model, num_plate", [("BMW", None, "RMI12345"), (None, "G CLASS", "KK 12343"), (None, None, "DBV123RV")])
def test_post_w_missing_values_v2(brand, model, num_plate, client):
    """ Testing w/o passing arguments where value is None"""
    json_body = {"brand": brand, "model": model, "num_plate": num_plate}
    res = client.post("/vehicles/", json={k: v for k, v in json_body.items() if v is not None}) #w/o parameter
    vehicle = schemas.VehicleCreate(**res.json())

    assert vehicle.model == model
    assert vehicle.brand == brand
    assert vehicle.num_plate == num_plate.replace(" ","")
    assert isinstance(vehicle.id, int)
    assert res.status_code == 201
    
@pytest.mark.parametrize("brand, model, num_plate", [("BMW", None, None), (None, "G CLASS", None), (None, None, None)])
def test_post_num_plate_missing(brand, model, num_plate, client):
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
    for vehicle in vehicles:
        vehicle
    assert res.status_code == 409

@pytest.mark.parametrize("brand, model", [("AUDI", "A5"), ("FORD", "RANGER RAPTOR")])
def test_update_vehicle(brand, model, client, vehicles):
    vehicle_before = {"brand": vehicles[0].brand, "model": vehicles[0].model}
    logger.debug(f"{vehicle_before['brand']}")
    res = client.put(f"/vehicles/1", json={"brand": brand, "model": model})
    logger.debug(f"{vehicle_before['brand']}")
    vehicle_after = schemas.VehicleResponse(**res.json())
    assert res.status_code == 200
    assert vehicle_before["brand"] != vehicle_after.brand
    assert vehicle_before["brand"] != vehicle_after.model

@pytest.mark.parametrize("brand", ["AUDI","FIAT"])
def test_update_vehicle_one_parameter_v1(brand, client, vehicles):
    vehicle_before = {"brand": vehicles[0].brand, "model": vehicles[0].model, "num_plate": vehicles[0].num_plate}
    res = client.put(f"/vehicles/1", json={"brand": brand})
    vehicle_after = schemas.VehicleResponse(**res.json())
    assert res.status_code == 200
    assert vehicle_before["brand"] != vehicle_after.brand
    assert vehicle_before["model"] == vehicle_after.model
    assert vehicle_before["num_plate"] == vehicle_after.num_plate


@pytest.mark.parametrize("model", ["A5", "PANDA"])
def test_update_vehicle_one_parameter_v2(model, client, vehicles):
    vehicle_before = {"brand": vehicles[0].brand, "model": vehicles[0].model, "num_plate": vehicles[0].num_plate}
    res = client.put(f"/vehicles/1", json={"model": model})
    vehicle_after = schemas.VehicleResponse(**res.json())
    assert res.status_code == 200
    assert vehicle_before["brand"] == vehicle_after.brand
    assert vehicle_before["model"] != vehicle_after.model
    assert vehicle_before["num_plate"] == vehicle_after.num_plate


@pytest.mark.parametrize("num_plate, brand, model", [("RMI53079", "AUDI", "A5"), ("RMI%2053079","FORD", "RANGER RAPTOR"), ("RMI   53079","FIAT", None) ])
def test_update_vehicle_by_numplate(num_plate, brand, model, client, vehicles):
    vehicle_before = {"brand": vehicles[0].brand, "model": vehicles[0].model, "num_plate": vehicles[0].num_plate}
    res = client.put(f"/vehicles/plates/{num_plate}", json={"brand": brand, "model": model})
    vehicle_after = schemas.VehicleResponse(**res.json())
    assert res.status_code == 200
    assert vehicle_before["brand"] != vehicle_after.brand

def test_update_vehicle_by_num_plate_error(client, vehicles):
    res = client.put("/vehicles/plates/RMI%2053079", json={"id": 11, "brand": "bmw"})
    assert res.status_code == 422  #Don't know if correct #TODO: check


def test_update_vehicle_by_id_error(client, vehicles):
    res = client.put("/vehicles/1", json={"num_plate": "RMI1234", "brand": "bmw"})
    assert res.status_code == 422  #Don't know if correct #TODO: check