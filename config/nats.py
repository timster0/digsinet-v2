from pydantic import BaseModel


class NatsSettings(BaseModel):
    """
    Configuration for NATS

    Attributes:
        host (str): host of the NATS server
        port (int): port of the NATS server
    """

    host: str
    port: int