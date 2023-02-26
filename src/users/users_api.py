import json
import uuid

import pydantic
from fastapi import HTTPException, status

from app.app_setup import app
from database.cosmos_db import users_container, user_key
from src.users import models

from pydantic import validate_email
import azure


@app.get("/users/:{user_id}")
async def get_user(user_id: str):
    existing_item = users_container.read_item(
        item=user_id,
        partition_key=user_id,
    )

    return existing_item


@app.get("/user")
async def get_all_users():
    query = "SELECT * FROM usersId"
    results = users_container.query_items(query=query, enable_cross_partition_query=True)
    items = [item for item in results]

    return items


@app.post("/users", response_model=models.NewUser)
async def add_user_to_db(user: models.AddUser):
    try:
        validate_email(user.email)
    except pydantic.errors.EmailError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email for the user.")

    new_user_id = str(uuid.uuid4())

    new_user = models.NewUser(id=new_user_id, **user.dict())

    users_container.create_item(new_user.dict())

    return new_user


@app.delete("/users/:{user_id}")
async def delete_user(user_id: str):
    try:
        users_container.delete_item(
            item=user_id,
            partition_key=user_id,
        )
    except azure.cosmos.exceptions.CosmosResourceNotFoundError:  # type: ignore
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

