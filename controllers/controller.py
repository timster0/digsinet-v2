from abc import ABC, abstractmethod

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

    def __init__(self):
        """
        Initialize the controller.

        Args:
            config (dict): contents of configuration file and derived supplemental configuration
                values.
            real_topology_definition (dict): real network topology definition (e.g., containerlab YAML)
            real_nodes (dict): nodes in the real network
            sibling (str): name of the sibling to create
            broker (EventBroker): broker for event streaming (e.g. RabbitMQ, Kafka)

        Returns:
            None

        Raises:
            None
        """
        pass