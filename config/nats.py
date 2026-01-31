from eventbroker.eventbroker import EventBrokerConfig


class NatsSettings(EventBrokerConfig):
    """
    Configuration for NATS

    Attributes:
        host (str): host of the NATS server
        port (int): port of the NATS server
    """

    host: str
    port: int