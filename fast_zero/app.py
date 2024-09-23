from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Massage

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Massage)
def read_root():
    return {"message": "Olá Mundo"}


@app.get(
    "/html_ola_mundo", status_code=HTTPStatus.OK, response_class=HTMLResponse
)
def read_root_html():
    return "<html> <head> <title> Meu Olá Mundo em HTML </title> </head>\
        <body> <h1> Olá Mundo! </h1> </body> </html>"
