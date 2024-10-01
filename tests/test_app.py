from http import HTTPStatus


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
            "email": "jonas@test.com",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "jonas",
        "email": "jonas@test.com",
        "id": 1,
    }


def test_read_user(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "username": "jonas",
                "email": "jonas@test.com",
                "id": 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "username": "jonas_lima",
            "password": "senha",
            "email": "jonas_lima@test.com",
        },
    )

    assert response.json() == {
        "id": 1,
        "username": "jonas_lima",
        "email": "jonas_lima@test.com",
    }


def test_exception_update_user(client):
    response = client.put(
        "/users/2",
        json={
            "username": "jonas_lima",
            "password": "senha",
            "email": "jonas_lima@test.com",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_user(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User Deleted"}


def test_exception_delete_user(client):
    response = client.delete(
        "/users/2",
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}
