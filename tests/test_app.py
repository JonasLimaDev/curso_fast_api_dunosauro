from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá Mundo"}


def test_read_root_deve_retornar_ok_e_html_ola_mundo(client):
    response = client.get("/html_ola_mundo")

    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == "<html> <head> <title> Meu Olá Mundo em HTML </title> </head>\
        <body> <h1> Olá Mundo! </h1> </body> </html>"
    )


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "jonas",
            "password": "senha",
            "email": "jonas@email.com",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "jonas",
        "email": "jonas@email.com",
    }


def test_read_user(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_exception_create_user_username_already_existis(client, user):
    response = client.post(
        "/users/",
        json={
            "username": user.username,
            "password": "senha",
            "email": "jonas_lima@test.com",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Username already exists"}


def test_exception_create_user_email_already_existis(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "jonas_lima",
            "password": "senha",
            "email": user.email,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Email already exists"}


def test_read_user_with_user(client, user):
    response = client.get("/users/")
    user_schema = UserPublic.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_read_user_by_id(client, user):
    response = client.get(f"/users/{user.id}")
    user_schema = UserPublic.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_user_by_id_exception_user_not_found(client):
    response = client.get("/users/100")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "jonas_lima",
            "password": "senha",
            "email": "jonas_lima@test.com",
            "id": user.id,
        },
    )

    assert response.json() == {
        "id": user.id,
        "username": "jonas_lima",
        "email": "jonas_lima@test.com",
    }


def test_exception_update_user(client, token):
    response = client.put(
        "/users/2",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "jonas_lima",
            "password": "senha",
            "email": "jonas_lima@test.com",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Not enough permission"}


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User Deleted"}


def test_exception_delete_user(client, token):
    response = client.delete(
        "/users/2",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Not enough permission"}


def test_get_token(client, user):
    response = client.post(
        "/token",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token


def test_exception_get_token(client, user):
    response = client.post(
        "/token",
        data={"username": "teste@email.com", "password": user.clean_password},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST

    assert response.json() == {"detail": "Incorrect email or password"}
