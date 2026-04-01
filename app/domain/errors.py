class DomainError(Exception):
    pass


class DomainNotFoundError(DomainError):
    pass


class DomainValidationError(DomainError):
    pass
