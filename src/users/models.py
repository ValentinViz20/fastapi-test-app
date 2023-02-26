import uuid

from pydantic import BaseModel


class AddUser(BaseModel):
    name: str
    email: str


class NewUser(BaseModel):
    id: str
    name: str
    email: str
