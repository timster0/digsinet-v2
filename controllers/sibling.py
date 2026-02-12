

from logging import Logger
from typing import List

from config.settings import Settings
from controllers.controller import Controller


class SiblingController(Controller):

    def __init__(self, logger: Logger, config: Settings, real_topology_definition: dict, sibling: str):
        self.siblings: List[str] = list()
        self.siblings.append(sibling)

        super().__init__(logger, config, real_topology_definition)
    
    async def async_run(self):
        # TODO: enter the main sibling controller loop
        pass
        