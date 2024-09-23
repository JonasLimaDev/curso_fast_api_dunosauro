from fastapi import FastAPI
from fast_zero.schemas import Massage
from http import HTTPStatus

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Massage)
def read_root():
    return {"message": "Olá Mundo"}
