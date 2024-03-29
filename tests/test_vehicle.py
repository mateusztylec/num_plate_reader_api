import pytest
from src.main import *
from requests import Request
from src import schemas
from src.logs import logger


@pytest.mark.parametrize("brand, model, num_plate",
                         [("BMW", "X3", "RMI12345"),
                          ("MERCEDES-BENZ","G CLASS","KK 12343"),
                          ("JEEP", "WRANGLER", "DBV123RV")])
def test_post_valid_vehicle(brand: str, 
                            model: str, 
                            num_plate: str, 
                            authorized_user: Request):
    logger.debug("test post vehicle")
    logger.debug(authorized_user.headers)
    res = authorized_user.post(
                    f"/vehicles/",
                    json={
                        "brand": brand,
                        "model": model,
                        "num_plate": num_plate})
    # rozpakowywujemy response na key=value wartosci
    assert res.status_code == 201
    vehicle = schemas.VehicleCreated(**res.json())
    assert vehicle.model == model
    assert vehicle.brand == brand
    assert vehicle.num_plate == num_plate.replace(" ", "")
    assert isinstance(vehicle.id, int)


@pytest.mark.parametrize("brand, model, num_plate",
                       [("BMW", None, "RMI12345"),
                        (None, "G CLASS", "KK 12343"),
                        (None, None,"DBV123RV")])
def test_post_w_missing_values_v1(brand, model, num_plate, authorized_user: Request):
    """ Testing by passing arguments with None value"""
    res = authorized_user.post(
        "/vehicles/",
        json={
            "brand": brand,
            "model": model,
            "num_plate": num_plate})  # parameter with value None
    # res_v2 = client.post("/vehicles/", json={k: v for k, v in
    # json_body.items() if v is not None}) #w/o entries
    vehicle = schemas.VehicleCreated(**res.json())

    assert vehicle.model == model
    assert vehicle.brand == brand
    assert vehicle.num_plate == num_plate.replace(" ", "")
    assert isinstance(vehicle.id, int)
    assert res.status_code == 201


def test_post_with_empty_num_plate_sting(authorized_user):
    res = authorized_user.post("/vehicles/", json={"num_plate": "", "brand": "BMw"})
    assert res.status_code == 422


@pytest.mark.parametrize("brand, model, num_plate",
                         [("BMW", None, "RMI12345"),
                          (None, "G CLASS", "KK 12343"),
                        (None, None, "DBV123RV")])
def test_post_w_missing_values_v2(brand, model, num_plate, authorized_user):
    """ Testing w/o passing arguments where value is None"""
    json_body = {"brand": brand, "model": model, "num_plate": num_plate}
    res = authorized_user.post(
        "/vehicles/",
        json={
            k: v for k,
            v in json_body.items() if v is not None})  # w/o parameter
    vehicle = schemas.VehicleCreated(**res.json())

    assert vehicle.model == model
    assert vehicle.brand == brand
    assert vehicle.num_plate == num_plate.replace(" ", "")
    assert isinstance(vehicle.id, int)
    assert res.status_code == 201


@pytest.mark.parametrize("brand, model, num_plate",
                         [("BMW", None, None), 
                          (None, "G CLASS", None), 
                          (None, None, None)])
def test_post_num_plate_missing(brand, model, num_plate, authorized_user):
    json_body = {"brand": brand, "model": model, "num_plate": num_plate}
    # w parameter with value None
    res_v1 = authorized_user.post("/vehicles/", json=json_body)
    res_v2 = authorized_user.post(
        "/vehicles/",
        json={
            k: v for k,
            v in json_body.items() if v is not None})  # w/o parameter

    assert res_v1.status_code == 422
    assert res_v2.status_code == 422  # FIXME #maybe it should be 404


@pytest.mark.parametrize("id", [99, 89])
def test_get_by_wrong_id(id, authorized_user):
    res = authorized_user.get(f'/vehicles/{id}')
    assert res.status_code == 404


@pytest.mark.parametrize("num_plate", ["RMI53079", "RMI12345", "RMI54321"])
# param order does not seem to have matter
def test_get_valid_by_num_plate(num_plate, vehicles, authorized_user):
    res = authorized_user.get(f"/vehicles/plates/{num_plate}")
    veh = schemas.VehicleResponse(**res.json())
    assert res.status_code == 200
    assert veh.num_plate == num_plate


@pytest.mark.parametrize("num_plate", ["1234", 313, "ssss"])
def test_get_invalid_by_num_plate(num_plate, authorized_user, vehicles):
    res = authorized_user.get(f"/vehicles/plates/{num_plate}")
    assert res.status_code == 404


@pytest.mark.parametrize("num_plate",
                         ["RMI%2053079", "RMI 53079", "RMI    53079 "])
def test_get_valid_by_num_plate_with_spaces(num_plate: str, authorized_user, vehicles):
    res = authorized_user.get(f"/vehicles/plates/{num_plate}")
    # print(f"Type of response: {type(res)}")  <class 'requests...>
    # print(f"Type of query: {type(vehicles[0])}")  <class 'app.models.Vehicle'>
    # print(f"Type of res.json(): {type(res.json())}")  # <class 'dict'>
    # res to jest obiekt klasy requests ktora ma .json()
    veh = schemas.VehicleResponse(**res.json())
    # natomiast vehicles jest klasy app.models.Vehicle
    assert veh.num_plate == vehicles[0].num_plate
    assert res.status_code == 200


@pytest.mark.parametrize("num_plate", ["RMI53079", "RMI54321"])
def test_post_duplicate_num_plate(num_plate, authorized_user, vehicles):
    res = authorized_user.post("/vehicles/", json={"num_plate": num_plate})
    for vehicle in vehicles:
        vehicle
    assert res.status_code == 409


@pytest.mark.parametrize("brand, model",
                         [("AUDI", "A5"), ("FORD", "RANGER RAPTOR")])
def test_update_vehicle(brand, model, authorized_user, vehicles):
    vehicle_before = {"brand": vehicles[0].brand, "model": vehicles[0].model}
    logger.debug(f"{vehicle_before['brand']}")
    res = authorized_user.put(f"/vehicles/1", json={"brand": brand, "model": model})
    logger.debug(f"{vehicle_before['brand']}")
    vehicle_after = schemas.VehicleResponse(**res.json())
    assert res.status_code == 200
    assert vehicle_before["brand"] != vehicle_after.brand
    assert vehicle_before["brand"] != vehicle_after.model


@pytest.mark.parametrize("brand", ["AUDI", "FIAT"])
def test_update_vehicle_one_parameter_v1(brand, authorized_user, vehicles):
    vehicle_before = {
        "brand": vehicles[0].brand,
        "model": vehicles[0].model,
        "num_plate": vehicles[0].num_plate}
    res = authorized_user.put(f"/vehicles/1", json={"brand": brand})
    vehicle_after = schemas.VehicleResponse(**res.json())
    assert res.status_code == 200
    assert vehicle_before["brand"] != vehicle_after.brand
    assert vehicle_before["model"] == vehicle_after.model
    assert vehicle_before["num_plate"] == vehicle_after.num_plate


@pytest.mark.parametrize("model", ["A5", "PANDA"])
def test_update_vehicle_one_parameter_v2(model, authorized_user, vehicles):
    vehicle_before = {
        "brand": vehicles[0].brand,
        "model": vehicles[0].model,
        "num_plate": vehicles[0].num_plate}
    res = authorized_user.put(f"/vehicles/1", json={"model": model})
    vehicle_after = schemas.VehicleResponse(**res.json())
    assert res.status_code == 200
    assert vehicle_before["brand"] == vehicle_after.brand
    assert vehicle_before["model"] != vehicle_after.model
    assert vehicle_before["num_plate"] == vehicle_after.num_plate


@pytest.mark.parametrize("num_plate, brand, model",
                         [("RMI53079", "AUDI", "A5"), 
                          ("RMI%2053079", "FORD", "RANGER RAPTOR"), 
                          ("RMI   53079", "FIAT", None)])
def test_update_vehicle_by_numplate(num_plate, brand, model, authorized_user, vehicles):
    vehicle_before = {
        "brand": vehicles[0].brand,
        "model": vehicles[0].model,
        "num_plate": vehicles[0].num_plate}
    res = authorized_user.put(
        f"/vehicles/plates/{num_plate}",
        json={
            "brand": brand,
            "model": model})
    vehicle_after = schemas.VehicleResponse(**res.json())
    assert res.status_code == 200
    assert vehicle_before["brand"] != vehicle_after.brand


def test_update_vehicle_by_num_plate_error(authorized_user, vehicles):
    res = authorized_user.put("/vehicles/plates/RMI%2053079",
        json={
            "id": 11,
            "brand": "bmw"})
    assert res.status_code == 422  # Don't know if correct #TODO: check


def test_update_vehicle_by_id_error(authorized_user, vehicles):
    res = authorized_user.put(
        "/vehicles/1",
        json={
            "num_plate": "RMI1234",
            "brand": "bmw"})
    assert res.status_code == 422  # Don't know if correct #TODO: check
