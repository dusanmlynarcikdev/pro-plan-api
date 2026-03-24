from fastapi import FastAPI

app = FastAPI(
    title="Pro Subscription Management REST API",
    servers=[
        {"url": "http://localhost", "description": "Local"},
    ],
    swagger_ui_parameters={"operationsSorter": "alpha"},
)
