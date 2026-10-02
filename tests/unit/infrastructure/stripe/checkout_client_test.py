from unittest.mock import AsyncMock, Mock

from pytest import mark
from stripe.params.checkout import (
    SessionCreateParams,
    SessionCreateParamsAutomaticTax,
    SessionCreateParamsCustomerUpdate,
    SessionCreateParamsLineItem,
    SessionCreateParamsNameCollection,
    SessionCreateParamsNameCollectionBusiness,
    SessionCreateParamsSubscriptionData,
    SessionCreateParamsTaxIdCollection,
)

from app.infrastructure.stripe.checkout_client import CheckoutClient

AUTOMATIC_TAX_PARAMS = SessionCreateParams(
    automatic_tax=SessionCreateParamsAutomaticTax(enabled=True),
    billing_address_collection="required",
)

BUSINESS_CUSTOMERS_PARAMS = SessionCreateParams(
    name_collection=SessionCreateParamsNameCollection(
        business=SessionCreateParamsNameCollectionBusiness(enabled=True, optional=True)
    ),
    tax_id_collection=SessionCreateParamsTaxIdCollection(enabled=True),
)


@mark.parametrize(
    ("automatic_tax", "business_customers", "expected"),
    [
        (False, False, SessionCreateParams()),
        (
            True,
            False,
            SessionCreateParams(
                **AUTOMATIC_TAX_PARAMS,
                customer_update=SessionCreateParamsCustomerUpdate(address="auto"),
            ),
        ),
        (
            False,
            True,
            SessionCreateParams(
                **BUSINESS_CUSTOMERS_PARAMS,
                customer_update=SessionCreateParamsCustomerUpdate(name="auto"),
            ),
        ),
        (
            True,
            True,
            SessionCreateParams(
                **AUTOMATIC_TAX_PARAMS,
                **BUSINESS_CUSTOMERS_PARAMS,
                customer_update=SessionCreateParamsCustomerUpdate(
                    address="auto", name="auto"
                ),
            ),
        ),
    ],
)
async def test_create_session_with_existing_customer(
    automatic_tax: bool,
    business_customers: bool,
    expected: SessionCreateParams,
) -> None:
    await _test_create_session(
        "customer-1",
        automatic_tax,
        business_customers,
        SessionCreateParams(**expected, customer="customer-1"),
    )


@mark.parametrize(
    ("automatic_tax", "business_customers", "expected"),
    [
        (False, False, SessionCreateParams()),
        (True, False, AUTOMATIC_TAX_PARAMS),
        (False, True, BUSINESS_CUSTOMERS_PARAMS),
        (
            True,
            True,
            SessionCreateParams(**AUTOMATIC_TAX_PARAMS, **BUSINESS_CUSTOMERS_PARAMS),
        ),
    ],
)
async def test_create_session_without_customer(
    automatic_tax: bool,
    business_customers: bool,
    expected: SessionCreateParams,
) -> None:
    await _test_create_session(None, automatic_tax, business_customers, expected)


async def _test_create_session(
    stripe_customer_id: str | None,
    automatic_tax: bool,
    business_customers: bool,
    expected: SessionCreateParams,
) -> None:
    stripe_client = Mock()
    stripe_client.v1.checkout.sessions.create_async = AsyncMock(
        return_value=Mock(url="https://checkout.stripe.com/c/pay/cs_test_123")
    )

    await CheckoutClient(stripe_client).create_session(
        "customer-1",
        stripe_customer_id,
        "price-1",
        "https://example.com/success",
        None,
        automatic_tax,
        business_customers,
    )

    stripe_client.v1.checkout.sessions.create_async.assert_awaited_once_with(
        SessionCreateParams(
            **expected,
            line_items=[SessionCreateParamsLineItem(price="price-1", quantity=1)],
            mode="subscription",
            subscription_data=SessionCreateParamsSubscriptionData(
                metadata={"customer_id": "customer-1"}
            ),
            success_url="https://example.com/success",
        )
    )
