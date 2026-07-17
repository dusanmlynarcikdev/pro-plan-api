from pytest import mark, raises

from app.domain.customer.email import Email
from app.domain.customer.errors import InvalidEmailError


def test_create() -> None:
    result = Email("john@doe.com")

    assert "john@doe.com" == result.value


@mark.parametrize("email", ("", "john", "john@", "john@doe", "johndoe.com"))
def test_invalid_email(email: str) -> None:
    with raises(InvalidEmailError):
        Email(email)
