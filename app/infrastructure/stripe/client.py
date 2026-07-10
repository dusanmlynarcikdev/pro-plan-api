from uuid import UUID


class Client:
    def __init__(self, api_key: str) -> None: ...
    async def create_checkout_session(
        self, price_id: str, subscription_id: UUID
    ) -> str:
        return "http://example.com"
