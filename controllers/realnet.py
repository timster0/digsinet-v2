
import json
from logging import Logger
import os
from config.settings import Settings
from controllers.controller import Controller
from typing import Any, List, final, override, Dict

from controllers.sibling import SiblingController
from interfaces.interface import Interface

@final
class RealnetController(Controller):
    """_Controller for realnet_

    Deploys the main topology and communicates the siblings. Does not deploy siblings.

    Args:
        Controller (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    def __init__(self, logger: Logger, config: Settings, real_topology_definition: dict, siblings: Dict[str, Dict[str, SiblingController]]):
        self.realnet_interfaces: Dict[str, Any] = dict()
        self.siblings: Dict[str, Dict[str, SiblingController]] = siblings
        super().__init__(logger, config, real_topology_definition)

    @property
    def name(self) -> str:
        return "realnet"

    @name.setter
    @override
    def name(self, name: str) -> None:
        # preserve compatibility with base class setter
        self._name = name
    
    async def async_run(self):
        self.deploy_topology()
        assert self.broker

        # Enter main loop
        self.logger.info("Entering realnet main loop...")
        realnet_subscriber, key = await self.broker.subscribe("realnet")

        for sibling_name, sibling_attributes in self.siblings.items():
            self.logger.info(f"Build sibling {sibling_name} using its controller...")
            await self.broker.publish(
                sibling_name,
                {
                    "type": "topology build request",
                    "source": "realnet",
                    "sibling": sibling_name,
                }
            )

            self.logger.info("Waiting for topology build response for realnet...")
            timeout = self.config.sibling_timeout
            try:
                while True:
                    message = await self.broker.poll(realnet_subscriber, timeout=timeout)
                    if message is None:
                        self.logger.fatal(f"Timeout while waiting for topology build response from sibling {sibling_name}. Exiting")
                        await self.broker.close()
                        exit(1)
                    elif message.error():
                        self.logger.fatal(f"Consumer error {message.error()}. Exiting")
                        await self.broker.close()
                        exit(1)
                    else:
                        assert message.value()
                        task = json.loads(message.value())
                        if (
                            task["type"] == "topology build response"
                            and task["sibling"] == sibling_name
                        ):
                            sibling_attributes.update(
                                {
                                    "topology": task["topology"],
                                    "nodes": task["nodes"],
                                    "interfaces": task["interfaces"],
                                    "running": task["running"],
                                }
                            )
                            break
            finally:
                self.logger.debug(f"Topology build response for sibling {sibling_name} received")
        
        # Finished Topology build request and response handling, entering main communication loop

        # TODO: insert main event loop

    def deploy_topology(self):
        os.system(f"clab deploy -t {self.config.topology.file}")

    def load_realnet_interfaces(self):
        self.realnet_interfaces = dict()
        for interface in self.config.realnet.interfaces:
            self.logger.debug(f"Loading realnet interface {interface}")
            # TODO: interface loading