# Убрали ручное создание TestClient(app), теперь используем фикстуру client
def test_get_rooms(client):
    response = client.get("/rooms/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)