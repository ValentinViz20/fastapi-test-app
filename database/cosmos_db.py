from dotenv import load_dotenv
import os

from azure.cosmos import CosmosClient, PartitionKey
import azure

load_dotenv(".env")

ENDPOINT = os.getenv("COSMOS_ENDPOINT")
KEY = os.environ["COSMOS_KEY"]

DATABASE_NAME = "Assist-Tech-Challenge-DB"
USERS_CONTAINER_NAME = "users-container"
FORMS_CONTAINER_NAME = "forms-container"

client = CosmosClient(url=ENDPOINT, credential=KEY)


# Connect to the db
database = client.create_database_if_not_exists(id=DATABASE_NAME)
print("Database\t", database.id)


# Create a new container for each "category" like users, forms, docs, etc
user_key = PartitionKey(path="/id", kind="Hash")
users_container: azure.cosmos.container.ContainerProxy = database.create_container_if_not_exists(
    id=USERS_CONTAINER_NAME, partition_key=user_key, offer_throughput=400
)

form_key_path = PartitionKey(path="/formsId")
forms_container = database.create_container_if_not_exists(
    id=FORMS_CONTAINER_NAME, partition_key=form_key_path, offer_throughput=400
)




