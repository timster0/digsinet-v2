from abc import ABC, abstractmethod
import asyncio
from logging import Logger
from multiprocessing import Process
from typing import final

from config.settings import Settings

class Controller(ABC):
    """
    Abstract base class for controllers.

    Attributes:
        config (dict): contents of configuration file and derived supplemental configuration values.
        real_topology_definition (dict): real network topology definition (e.g., containerlab YAML)
        real_nodes (dict): nodes in the real network
        broker (EventBroker): broker for event streaming (e.g. RabbitMQ, Kafka)

    Methods:
        name()
        import_app(app: str, module: str)
        build_topology(sibling: str, config: dict, topology_definition: dict)
        run()
    """
    @property
    def name(self):
        """
        Name of the controller.

        Args:
            None

        Returns:
            str: name of the controller

        Raises:
            None
        """

        return self._name

    @name.setter
    @abstractmethod
    def name(self, name: str):
        """
        Name of the controller.

        Args:
            None

        Returns:
            str: name of the controller

        Raises:
            None
        """

        self._name = name

    @final
    def __init__(
        self,
        logger: Logger,
        config: Settings,
        real_topology_definition: dict,
    ):
        """
        Initialize the controller.

        Also initializes an event broker for event streaming and communicating with other controllers.
        
        Args:
            config (dict): contents of configuration file and derived supplemental configuration
                values.
            real_topology_definition (dict): real network topology definition (e.g., containerlab YAML)
            real_nodes (dict): nodes in the real network
            sibling (str): name of the sibling to create

        Returns:
            None

        Raises:
            None
        """

        self.logger: Logger = logger
        self.config: Settings = config
        self.real_topology_definition: dict = real_topology_definition
        self.broker = None  # TODO: Initialize event broker here

        self.process: Process = Process(target=self.run, name="Controller " + self.name)
        self.process.start()
        self.logger.info(f"Started controller process for {self.name} with PID {self.process.pid}")

    @final
    def run(self):
        """
        Start the controller with the applications for the assigned sibling / realnet
        Args:
            None

        Returns:
            None

        Raises:
            None
        """

        asyncio.run(self.async_run())

    @abstractmethod
    async def async_run(self):
        """
        Start the controller with the applications for the assigned sibling / realnet.
        This method is to be overridden by subclasses.
        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        pass