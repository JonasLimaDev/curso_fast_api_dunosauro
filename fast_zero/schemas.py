from pydantic import BaseModel


class Massage(BaseModel):
    message: str
