from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá Mundo"}


def test_read_root_deve_retornar_ok_e_html_ola_mundo():
    client = TestClient(app)

    response = client.get("/html_ola_mundo")

    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == "<html> <head> <title> Meu Olá Mundo em HTML </title> </head>\
        <body> <h1> Olá Mundo! </h1> </body> </html>"
    )
