from datetime import date, timedelta
from app.models.room import Room
from app.models.guest import Guest


def test_full_booking_lifecycle(client, db_session, admin_token_headers):
    # 1. Подготавливаем данные
    room = Room(number="101", type="single", price_per_night=2500.0, floor=1, status="available")
    guest = Guest(first_name="Иван", last_name="Иванов", email="ivan@test.com", phone="+1234567890",
                  passport_number="AB123")

    db_session.add(room)
    db_session.add(guest)
    db_session.commit()

    # ОБЯЗАТЕЛЬНО обновляем объекты, чтобы подтянуть их сгенерированные ID
    db_session.refresh(room)
    db_session.refresh(guest)

    # 2. Создаем бронь
    booking_data = {
        "room_id": room.id,
        "guest_id": guest.id,
        "check_in_date": str(date.today()),
        "check_out_date": str(date.today() + timedelta(days=2))
    }

    response = client.post("/bookings/", json=booking_data, headers=admin_token_headers)
    # Если будет ошибка 422, assert покажет нам точный текст от Pydantic!
    assert response.status_code == 201, f"Ошибка создания брони: {response.text}"

    booking_id = response.json()["id"]
    assert response.json()["total_price"] == 5000.0  # 2500 * 2 дня

    # 3. Проверка на пересечение дат
    response_overlap = client.post("/bookings/", json=booking_data, headers=admin_token_headers)
    assert response_overlap.status_code == 400
    assert "уже забронирована" in response_overlap.json()["detail"]

    # 4. Check-in (Заселение гостя)
    checkin_response = client.post(f"/bookings/{booking_id}/checkin", headers=admin_token_headers)
    assert checkin_response.status_code == 200, f"Ошибка check-in: {checkin_response.text}"
    stay_id = checkin_response.json()["id"]

    db_session.refresh(room)
    assert room.status == "occupied"

    # 5. Check-out (Выезд гостя)
    checkout_response = client.post(f"/bookings/stays/{stay_id}/checkout", headers=admin_token_headers)
    assert checkout_response.status_code == 200, f"Ошибка check-out: {checkout_response.text}"

    db_session.refresh(room)
    assert room.status == "cleaning"