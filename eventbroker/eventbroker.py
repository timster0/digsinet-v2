from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple
from logging import Logger

from pydantic import BaseModel

class Message(ABC):
    def __init__(self, message: Any):
        self._message = message

    @abstractmethod
    def error(self) -> str | None:
        pass

    @abstractmethod
    def value(self) -> Optional[str]:
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
    async def publish(self, channel: str, data: Any):
        pass

    @abstractmethod
    async def poll(self, consumer: Any, timeout: float) -> Optional[Message]:
        pass

    @abstractmethod
    async def subscribe(self, channel: str, group_id: str | None = None) -> Tuple[Any, str]:
        """_Subscribe to channel_

        Args:
            channel (str): _description_
            group_id (str | None, optional): _description_. Defaults to None.

        Returns:
            Tuple[Any, str]: _Broker defined Subscription and the corresponding channel_
        """
        pass

    @abstractmethod
    async def get_sibling_channels(self) -> List[str]:
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
