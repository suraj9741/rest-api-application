def test_healthcheck(test_client):
    response = test_client.get("/api/v1/students/healthcheck")
    assert response.status_code == 200
    assert response.json["status"] == "ok"

def test_create_student(test_client):
    payload = {
        "first_name": "Suraj",
        "last_name": "Jadhav",
        "email": "test1@test.com",
        "gender": "M",
        "date_of_birth": "2000-05-15"
    }
    response = test_client.post("/api/v1/students/", json=payload)
    assert response.status_code == 201
    assert "id" in response.json

def test_duplicate_email(test_client):
    payload = {
        "first_name": "Suraj",
        "email": "duplicate@test.com"
    }
    # first insert
    test_client.post("/api/v1/students/", json=payload)
    # duplicate insert
    response = test_client.post("/api/v1/students/", json=payload)
    assert response.status_code == 400
    assert "error" in response.json

def test_get_students(test_client):
    response = test_client.get("/api/v1/students/")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_student_by_id(test_client):
    payload = {
        "first_name": "Test",
        "email": "get@test.com"
    }
    create_res = test_client.post("/api/v1/students/", json=payload)
    student_id = create_res.json["id"]
    response = test_client.get(f"/api/v1/students/{student_id}")
    assert response.status_code == 200
    assert response.json["id"] == student_id

def test_get_student_not_found(test_client):
    response = test_client.get("/api/v1/students/9999")
    assert response.status_code == 404

def test_update_student(test_client):
    payload = {
        "first_name": "Old",
        "email": "update@test.com"
    }
    create_res = test_client.post("/api/v1/students/", json=payload)
    student_id = create_res.json["id"]
    update_payload = {
        "first_name": "New"
    }
    response = test_client.put(f"/api/v1/students/{student_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json["first_name"] == "New"

def test_delete_student(test_client):
    payload = {
        "first_name": "Delete",
        "email": "delete@test.com"
    }
    create_res = test_client.post("/api/v1/students/", json=payload)
    student_id = create_res.json["id"]
    response = test_client.delete(f"/api/v1/students/{student_id}")
    assert response.status_code == 200
    assert response.json["deleted_id"] == student_id

def test_delete_not_found(test_client):
    response = test_client.delete("/api/v1/students/9999")
    assert response.status_code == 404