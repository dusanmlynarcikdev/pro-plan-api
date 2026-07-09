from pydantic import BaseModel


class CreateOrGetRequest(BaseModel):
    email: str
