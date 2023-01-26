import pytest
from .conftest import client, vehicles

event_path = "/events/"

@pytest.mark.parametrize("limit, skip", [(5, 0), (10, 5), (3, 2)])
def test_get_correct_event(limit, skip, client):
    res = client.get(event_path+f"?limit={limit}&skip={skip}")
    assert res.status_code == 200
