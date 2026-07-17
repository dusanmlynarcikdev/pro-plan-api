from app.domain.errors import NotFoundDomainError


class CustomerNotFoundError(NotFoundDomainError):
    def __init__(self) -> None:
        super().__init__("Customer not found")
