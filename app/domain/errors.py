class DomainError(Exception):
    pass


class ConflictDomainError(DomainError):
    pass


class DomainNotFoundError(DomainError):
    pass


class DomainValidationError(DomainError):
    pass
