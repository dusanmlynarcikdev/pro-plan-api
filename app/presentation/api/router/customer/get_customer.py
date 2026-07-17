from fastapi import APIRouter, status

from app.domain.customer.customer import Customer
from app.domain.customer.email import Email
from app.presentation.api.dependencies import GetCustomerUseCase
from app.presentation.api.responses import ERROR_RESPONSE_MODEL
from app.presentation.api.router.customer.responses import CustomerResponse

router = APIRouter()


@router.get(
    "/customers/{email}",
    response_model=CustomerResponse,
    responses={status.HTTP_404_NOT_FOUND: ERROR_RESPONSE_MODEL},
)
async def get_customer(email: str, get_customer: GetCustomerUseCase) -> Customer:
    """
    :raises CustomerNotFound:
    :raises InvalidEmail:
    """
    return await get_customer(Email(email))
