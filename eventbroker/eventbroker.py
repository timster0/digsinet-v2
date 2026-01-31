from abc import ABC, abstractmethod
from typing import Any, List
from logging import Logger

from pydantic import BaseModel

class Message(ABC):
    def __init__(self, message: Any):
        self._message = message

    @abstractmethod
    def error(self):
        pass

    @abstractmethod
    def value(self):
        pass

class EventBrokerConfig(BaseModel):
    """_ABC for a configuration for an EventBroker_

    Inherits from Pydantic BaseModel for easy validation and parsing.
    Override this class to add specific configuration parameters for different EventBroker implementations.

    """
    pass

class EventBroker(ABC):

    async def __init__(self, config: EventBrokerConfig, channels: List[str], logger: Logger):
        pass

    @abstractmethod
    async def publish(self, channel: str, data):
        pass

    @abstractmethod
    async def poll(self, consumer, timeout) -> Message:
        pass

    @abstractmethod
    async def subscribe(self, channel: str, group_id: str | None = None):
        pass

    @abstractmethod
    async def get_sibling_channels(self):
        pass

    @abstractmethod
    async def new_sibling_channel(self, channel: str):
        pass

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def close_consumer(self, consumer: str):
        pass
