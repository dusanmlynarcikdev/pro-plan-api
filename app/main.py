from fastapi import APIRouter, Depends, FastAPI, status

_users_tag = "Users"

app = FastAPI(
    title="Pro Subscription Management REST API",
    servers=[
        {"url": "http://localhost", "description": "Local"},
    ],
    swagger_ui_parameters={"operationsSorter": "alpha"}
)