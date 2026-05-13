def test_reports_endpoints(client, admin_token_headers):
    # Тест отчета по занятости
    occ_response = client.get("/reports/occupancy", headers=admin_token_headers)
    assert occ_response.status_code == 200
    assert "occupancy_rate" in occ_response.json()

    # Тест отчета по выручке
    rev_response = client.get("/reports/revenue", headers=admin_token_headers)
    assert rev_response.status_code == 200
    assert "total_revenue" in rev_response.json()