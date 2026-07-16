class DomainError(Exception):
    pass


class ConflictDomainError(DomainError):
    pass


class NotFoundDomainError(DomainError):
    pass


class ValidationDomainError(DomainError):
    pass
