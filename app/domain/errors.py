class DomainError(Exception):
    pass


class DomainConflictError(DomainError):
    pass


class DomainNotFoundError(DomainError):
    pass


class DomainValidationError(DomainError):
    pass
