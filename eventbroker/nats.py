

from logging import Logger
from typing import Dict, List, Any, Optional, Tuple
from config.nats import NatsSettings
from eventbroker.eventbroker import EventBroker, Message
from nats.aio.msg import Msg as NatsMsg
from nats.aio.subscription import Subscription as NatsSubscription
from nats.aio.client import Client
import json
import nats

class NatsMessage(Message):
    def __init__(self, message: NatsMsg):
        self._message = message

    def error(self) -> str | None:
        if self._message:
            return None
        else:
            return "NATS Message Error"

    def value(self) -> str | None:
        return self._message.data.decode() # Defaults to UTF-8
    
class NatsClient(EventBroker):
    async def __init__(self, config: NatsSettings, channels: List[str], logger: Logger):
        await super().__init__(config, channels, logger)
        self.config: NatsSettings = config
        self.subjects: List[str] = channels
        self.logger: Logger = logger
        self.client: Client = await nats.connect(f"{self.config.host}:{self.config.port}")
        self.subscribers: Dict[str, NatsSubscription] = dict()

    async def publish(self, channel: str, data: Any):
        if channel not in self.subjects:
            self.logger.warning(f"NATS subject {channel} is an unknown subject")
        serialized_data: str = json.dumps(data, default=lambda x: "<not serializable>")
        self.logger.info(f"Publishing message to NATS subject {channel}: {serialized_data}")
        await self.client.publish(channel, bytes(serialized_data, 'utf-8'))

    async def poll(self, consumer: NatsSubscription, timeout: float) -> Optional[NatsMessage]:
        try:
            return NatsMessage(await consumer.next_msg(timeout=timeout))
        except TimeoutError:
            return None
        except Exception as exception:
            self.logger.error(f"Unhandled exception when polling for NATS subject {consumer.subject}: {exception}")
            return None
        
    async def subscribe(self, channel: str, group_id: str | None = None) -> Tuple[Any, str]:
        if channel not in self.subscribers.keys():
            subscription: NatsSubscription = await self.client.subscribe(channel)
            self.subscribers.update({channel: subscription})
            self.logger.info(f"Subscribed to NATS subject {channel} in group {group_id}")
        else:
            self.logger.warning(f"Tried to subscribe to NATS subject with active subscription: {channel}")
        return self.subscribers[channel], channel

    async def get_sibling_channels(self):
        return self.subjects
    
    async def close(self):
        # Unsubscribe from all subjects
        for subject, subscriber in self.subscribers.items():
            await self.close_consumer(subject)
        self.logger.info("All NATS subscribers closed")
        # Delete all subjects
        del self.subjects
        self.logger.info("Deleted all NATS subjects")
        # Shut down client
        await self.client.flush()
        await self.client.close()
        self.logger.info("Closed NATS client")            

    async def close_consumer(self, consumer: str):
        if consumer in self.subscribers.keys():
            await self.subscribers[consumer].unsubscribe()
            self.logger.info(f"Subscriber for NATS subject {consumer} closed.")
            # del self.subscribers[key]
        else:
            self.logger.warning(f"Unable to close subscriber for NATS subject {consumer}: Subscriber not found")

    # This method is not used publicly
    async def new_sibling_channel(self, channel: str):
        pass