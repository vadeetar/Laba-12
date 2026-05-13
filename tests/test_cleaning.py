from app.models.room import Room
from app.models.cleaning_task import CleaningTask

def test_cleaning_tasks_lifecycle(client, db_session, admin_token_headers):
    # Подготавливаем грязную комнату и задачу
    room = Room(number="202", type="double", price_per_night=3000.0, floor=2, status="cleaning")
    db_session.add(room)
    db_session.commit()
    db_session.refresh(room)

    task = CleaningTask(room_id=room.id, status="pending", notes="Убраться после выезда")
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    # Проверяем получение списка задач
    response = client.get("/cleaning/", headers=admin_token_headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

    # Завершаем уборку
    comp_response = client.post(f"/cleaning/{task.id}/complete", headers=admin_token_headers)
    assert comp_response.status_code == 200
    assert comp_response.json()["status"] == "done"

    # Проверяем, что комната снова доступна для брони
    db_session.refresh(room)
    assert room.status == "available"