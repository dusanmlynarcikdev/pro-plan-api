class ClientError(Exception):
    pass


class MissingCheckoutSessionUrlError(ClientError):
    def __init__(self) -> None:
        super().__init__("Missing checkout session url")
