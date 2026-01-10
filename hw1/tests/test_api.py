import pytest
from hw1.main.models import Client, Parking, ClientParking


@pytest.mark.parametrize("route", ["/clients", "/parkings"])
def test_get_routes(client, route, sample_data):
    _, _ = sample_data
    response = client.get(route)
    assert response.status_code == 200, f"Ошибка при получении маршрута {route}: {response.text}"


def test_create_client(client, db_session):
    payload = {"name": "Пётр", "surname": "Петров", "car_number": "B456CD"}
    response = client.post("/clients", json=payload)
    assert response.status_code == 201
    created_client = Client.query.first()
    assert created_client.name == "Пётр"


def test_create_parking(client, db_session):
    payload = {"address": "ул. Пушкина, д. 5", "count_places": 15, "count_available_places": 15}
    response = client.post("/parkings", json=payload)
    assert response.status_code == 201
    created_parking = Parking.query.first()
    assert created_parking.address == "ул. Пушкина, д. 5"


@pytest.mark.parking
def test_enter_parking(client, db_session, sample_data):
    cl, park = sample_data
    payload = {"client_id": cl.id, "parking_id": park.id}
    response = client.post("/client_parkings", json=payload)
    assert response.status_code == 201
    log = ClientParking.query.first()
    assert log.client_id == cl.id
    assert log.parking_id == park.id


@pytest.mark.parking
def test_leave_parking(client, db_session, sample_data):
    cl, park = sample_data
    entry_payload = {"client_id": cl.id, "parking_id": park.id}
    client.post("/client_parkings", json=entry_payload)
    log = ClientParking.query.first()
    assert log.time_in is not None
    leave_payload = {"client_id": cl.id, "parking_id": park.id}
    response = client.delete("/client_parkings", json=leave_payload)
    assert response.status_code == 200
    updated_log = ClientParking.query.first()
    assert updated_log.time_out is not None
