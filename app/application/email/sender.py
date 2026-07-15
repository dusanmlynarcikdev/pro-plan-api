from typing import Protocol

from app.application.email.message import Message


class Sender(Protocol):
    async def send(self, message: Message) -> None: ...
