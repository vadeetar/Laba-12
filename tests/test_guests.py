def test_create_guest(client, admin_token_headers):
    guest_data = {
        "first_name": "Анна",
        "last_name": "Смирнова",
        "email": "anna.s@test.com",
        "phone": "+1987654321",
        "passport_number": "CD456"
    }
    response = client.post("/guests/", json=guest_data, headers=admin_token_headers)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Анна"

def test_read_guests(client, admin_token_headers):
    response = client.get("/guests/", headers=admin_token_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)