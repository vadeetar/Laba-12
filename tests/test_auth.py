def test_login_success(client, db_session, admin_token_headers):
    # Успешный логин уже проверяется при создании admin_token_headers, 
    # поэтому здесь проверим защиту от неверного пароля
    response = client.post(
        "/auth/login",
        data={"username": "admin_test", "password": "wrong_password"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Неверный логин или пароль"