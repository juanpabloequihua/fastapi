from app import schemas
import pytest
from jose import jwt
from app.config import settings

def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == "Welcome to my API!!! Now deployed.!"  
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json = {"email": "hello123@gmail.com", "password": "123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login/", data = {"username": test_user['email'], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms= [settings.algorithm])
    id = payload.get("user_id")

    assert str(id) == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@example.com", "123", 403),
    ("juan@gmail.com", "wrongpass", 403),
    ("wrongemail@example.com", "wrongpass", 403),
    (None, "123", 422),
    ("juan@gmail.com", None, 422)
    ])
def test_incorrect_login(client, test_user, email, password, status_code):
    
    res = client.post("/login/", data = {"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid credentials"

