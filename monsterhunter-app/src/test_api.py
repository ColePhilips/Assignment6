import pytest
from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api
from api import app, Monster  # Import the app and Monster class from your api.py
from unittest.mock import patch, MagicMock

# Create a test client
@pytest.fixture
def client():
    app.config["MONGO_URI"] = "mongodb://localhost:27017/test_db"  # Use a test database
    with app.test_client() as client:
        yield client

# Mock MongoDB
@pytest.fixture
def mock_mongo():
    with patch('api.mongo') as mock:
        mock.db.monsters = MagicMock()
        # Reset the state of the mock before each test
        mock.db.monsters.find_one.return_value = None  # Ensure no monster exists by default
        mock.db.monsters.count_documents.return_value = 0  # Ensure count is 0 by default
        yield mock

#1 Test POST /monsters
def test_create_monster(client, mock_mongo):
    response = client.post('/monsters', json={
        "name": "Test Monster",
        "description": "A monster for testing",
        "type": "Test Type"
    })
    assert response.status_code == 200
    assert response.json['name'] == "Test Monster"

#2 Test POST for /monsters without a name
def test_create_monster_without_name(client, mock_mongo):
    response = client.post('/monsters', json={
        #"name": "Test Monster",
        "description": "Test Description",
        "type": "Test Type"
    })
    assert response.status_code == 400
    assert response.json['message'] == "Name and description are required!"

#3 Test POST for /monsters with missing description
def test_create_missing_description(client, mock_mongo):
    response = client.post('/monsters', json={
        "name": "Test Monster",
        #"description": "Test Description",
        "type": "Test Type"
    })
    assert response.status_code == 400
    assert response.json['message'] == "Name and description are required!"

#4 Test POST for /monsters with invalid data
def test_create_invalid_id(client, mock_mongo):
    response = client.post('/monsters', json={})
    assert response.status_code == 400
    assert response.json['message'] == "Name and description are required!"

#5 Test POST for /monsters with duplicate name
def test_create_duplicate(client, mock_mongo):
    mock_mongo.db.monsters.find_one.return_value = {"name": "Duplicate Monster"}
    response = client.post('/monsters', json={
        "name": "Duplicate Monster",
        "description": "A monster for testing",
        "type": "Test Type"
    })
    assert response.status_code == 400
    assert response.json['message'] == "Monster with this name already exists!"

#6 Test GET for /monsters
def test_get_all_monsters(client, mock_mongo):
    mock_mongo.db.monsters.find.return_value = [
        {"id": 1, "name": "Monster1", "description": "Description1", "type": "Type1"},
        {"id": 2, "name": "Monster2", "description": "Description2", "type": "Type2"}
    ]
    response = client.get('/monsters')
    assert response.status_code == 200
    assert len(response.json) == 2

#7 Test GET for /monsters/<id>
def test_get_monster_by_id(client, mock_mongo):
    mock_mongo.db.monsters.find_one.return_value = {
        "id": 1, "name": "Monster1", "description": "Description1", "type": "Type1"
    }
    response = client.get('/monsters/1')
    assert response.status_code == 200
    assert response.json['name'] == "Monster1"

#8 Test GET for /monsters/<id> for not found
def test_get_not_found(client, mock_mongo):
    mock_mongo.db.monsters.find_one.return_value = None
    response = client.get('/monsters/999')
    assert response.status_code == 404
    assert response.json['message'] == "Monster not found"

#9 Test GET for /monsters with no monsters
def test_get_empty_db(client, mock_mongo):
    mock_mongo.db.monsters.find.return_value = []
    response = client.get('/monsters')
    assert response.status_code == 200
    assert response.json == []

#10 Test GET for /monsters/<id> with non-integer id
def test_get_nonInteger(client, mock_mongo):
    response = client.get('/monsters/a')
    assert response.status_code == 404

#11 Test GET for /monsters with specific type filter
def test_get_filter(client, mock_mongo):
    mock_mongo.db.monsters.find.return_value = [
        {"id": 1, "name": "Monster1", "description": "Description1", "type": "Fire"},
        {"id": 2, "name": "Monster2", "description": "Description2", "type": "Fire"}
    ]
    response = client.get('/monsters?type=Fire')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert all(monster['type'] == "Fire" for monster in response.json)

#12 Test PUT for /monsters/<id>
def test_update_monster(client, mock_mongo):
    mock_mongo.db.monsters.update_one.return_value.matched_count = 1
    response = client.put('/monsters/1', json={
        "name": "Updated Monster",
        "description": "Updated Description",
        "type": "Updated Type"
    })
    assert response.status_code == 200
    assert response.json['name'] == "Updated Monster"

#13 Test PUT for /monsters/<id> for not found
def test_update_not_found(client, mock_mongo):
    mock_mongo.db.monsters.update_one.return_value.matched_count = 0
    response = client.put('/monsters/999', json={
        "name": "Updated Monster",
        "description": "Updated Description",
        "type": "Updated Type"
    })
    assert response.status_code == 404
    assert response.json['message'] == "Monster not found!"

#14 Test PUT for /monsters/<id> with missing fields
def test_update_missing_field(client, mock_mongo):
    response = client.put('/monsters/1', json={
        #"name": "Updated Monster",
        #"description": "Updated Description",
        "type": "Updated Type"
    })
    assert response.status_code == 400
    assert response.json['message'] == "Name and description are required fields"

#15 Test PUT for /monsters/<id> with non-integer id
def test_update_nonInteger(client, mock_mongo):
    response = client.put('/monsters/a', json={
        "name": "Updated Monster",
        "description": "Updated Description",
        "type": "Updated Type"
    })
    assert response.status_code == 404

#16 Test DELETE for /monsters/<id>
def test_delete_monster(client, mock_mongo):
    mock_mongo.db.monsters.delete_one.return_value.deleted_count = 1
    response = client.delete('/monsters/1')
    assert response.status_code == 200
    assert response.json['message'] == "Monster deleted successfully!"

#17 Test DELETE for /monsters/<id> for not found
def test_delete_not_found(client, mock_mongo):
    mock_mongo.db.monsters.delete_one.return_value.deleted_count = 0
    response = client.delete('/monsters/999')
    assert response.status_code == 404
    assert response.json['message'] == "Monster not found!"

#18 Test DELETE for /monsters/<id> with invalid id
def test_delete_invalid_id(client, mock_mongo):
    response = client.delete('/monsters/InvalidID')
    assert response.status_code == 404

#19 Test DELETE for /monsters/<id> with non-integer id
def test_delete_nonInteger(client, mock_mongo):
    response = client.delete('/monsters/a')
    assert response.status_code == 404

#20 Test that the app runs without errors
def test_app_runs(client, mock_mongo):
    assert client is not None