from uuid import UUID

from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domain.subscription.email import Email
from app.infrastructure.persistence.schema.subscription import SubscriptionSchema
from tests.generator.subscription import generate

PATH = "/api/subscriptions"


async def test_create(client: TestClient, session: AsyncSession) -> None:
    session.add(SubscriptionSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    response = client.post(PATH, json={"email": "john2@doe.com"})
    session.expunge_all()

    assert response.status_code == status.HTTP_200_OK

    repository_subscriptions = (await session.exec(select(SubscriptionSchema))).all()

    assert len(repository_subscriptions) == 2

    assert repository_subscriptions[0].id == UUID(
        "019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"
    )
    assert repository_subscriptions[0].email == "john@doe.com"
    assert not repository_subscriptions[0].is_active

    assert repository_subscriptions[1].email == "john2@doe.com"
    assert not repository_subscriptions[1].is_active

    assert response.json() == {"id": str(repository_subscriptions[1].id)}


async def test_get(client: TestClient, session: AsyncSession) -> None:
    session.add(SubscriptionSchema.from_domain(generate()))
    session.add(
        SubscriptionSchema.from_domain(
            generate(
                UUID("019d43e5-eecd-7ab5-a891-7688443b13f6"),
                Email("john2@doe.com"),
            )
        )
    )
    await session.flush()
    session.expunge_all()

    response = client.post(PATH, json={"email": "john2@doe.com"})
    session.expunge_all()

    assert response.status_code == status.HTTP_200_OK
    assert response.content == b'{"id":"019d43e5-eecd-7ab5-a891-7688443b13f6"}'

    repository_subscriptions = (await session.exec(select(SubscriptionSchema))).all()

    assert len(repository_subscriptions) == 2

    assert repository_subscriptions[0].id == UUID(
        "019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"
    )
    assert repository_subscriptions[0].email == "john@doe.com"
    assert not repository_subscriptions[0].is_active

    assert repository_subscriptions[1].id == UUID(
        "019d43e5-eecd-7ab5-a891-7688443b13f6"
    )
    assert repository_subscriptions[1].email == "john2@doe.com"
    assert not repository_subscriptions[1].is_active


def test_invalid_email(
    client: TestClient,
) -> None:
    response = client.post(PATH, json={"email": "doe.com"})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.content == b'{"detail":"Invalid email"}'
