import pytest
from .conftest import client, vehicles, events
from src import schemas

event_path = "/events/"


@pytest.mark.parametrize("limit, skip", [(5, 0), (10, 5), (3, 2)])
def test_get_correct_event(limit, skip, client, events, users):
    res = client.get(event_path + f"?limit={limit}&skip={skip}")
    assert res.status_code == 200


def test_get_proper_events(client, events):
    res = client.get(event_path + f"1/")
    event = schemas.Event(**res.json())
    assert res.status_code == 200
    assert event.id == 1
    assert event.vehicle_id == 1


@pytest.mark.parametrize("limit, skip",
                         [(5, 6), (0, 2), (0, 0), (-1, 1), (-1, -2), ("a", 1), ("a", "b")])
def test_wrong_query_parameter(client, events, limit, skip):
    res = client.get(event_path + f"?limit={limit}$skip={skip}")
    assert res.status_code >= 400


@pytest.mark.parametrize("id", [99, 199])
def test_wrong_event_id(client, vehicles, id):
    res = client.get(event_path + f"{id}")
    assert res.status_code == 404
