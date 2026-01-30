from argparse import ArgumentParser, Namespace
from logging import Logger
import logging
from types import ModuleType
from typing import Any, Dict, Optional
import yaml
from config import settings
from config.settings import  ControllerSettings, Settings
from controllers.controller import Controller
import importlib


logger: Logger = logging.getLogger("digsinet-v2")

def main():
    global logger

    # Set up logging
    handler = logging.StreamHandler()
    fmt = "[%(asctime)s %(levelname)s pID(%(process)d)] %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    logger.setLevel(logging.INFO)
    
    parser: ArgumentParser = ArgumentParser(
        description="digsinet-v2 command line interface",
    )

    parser.add_argument("--debug", help="Enable debug logging", action="store_true")
    parser.add_argument("--stop", help="Stop all siblings and cleanup containers", action="store_true")
    parser.add_argument("--config", help="Path to configuration file, defaults to digsinet.py", type=str, default="digsinet.yml")
    parser.add_argument("--start", help="Start digsinet-v2 with the specified configuration file", action="store_true")

    arguments: Namespace = parser.parse_args()
    try:
        config: Settings = read_config(arguments.config)
    except Exception as e:
        logger.error("Aborting: Failed to read configuration file: %s", e)
        return

    if arguments.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    if arguments.stop:
        logger.info("Stopping all siblings and cleaning up containers...")
        stop_digsinet(config)
    
    elif arguments.start:
        logger.info("Starting digsinet-v2 with configuration file: %s", arguments.config)
        start_digsinet(config)

def stop_digsinet(config: Settings):
    pass

def start_digsinet(config: Settings):
    # Containerlab definition file. See containerlab docs for more info
    containerlab_topology_definition: Any = load_topology(config)
    topology_name: str = containerlab_topology_definition.get("name")
    topology_prefix: str = "clab"
    controllers = load_controllers(config)
    pass

def read_config(config_file: str) -> Settings:
    """
    Reads the config file and tries to parse it into Settings,
    throwing errors if the format is not as specified.
    """
    with open(config_file) as file:
        data: Any = yaml.safe_load(file)
        config = Settings(**data)
        if settings.validate_config(config):
            return config
        else:
            raise Exception('configuration error: either nats, kafka or rabbitmq settings must be provided')


def load_topology(config: Settings) -> Any:
    """_Load Containerlab topology definition_

    Args:
        config (Settings): _The settings to extract the containerlab definition from_
    """
    with open(config.topology.file, "r") as file:
        topology_definition = yaml.safe_load(file)
        return topology_definition
    
def load_controllers(config: Settings) :
    global logger

    controllers: dict[str, Controller] = dict()
    for controller in config.controllers:
        logger.debug(f"Loading controller {controller}...")
        controller_name = config.controllers.get(controller)
        if controller_name is None:
            logger.error(f"Controller {controller} not found in configuration. Skipping")
            continue
        module: ModuleType = importlib.import_module(controller_name.module)
        controllers[controller] = module
    return controllers

if __name__ == "__main__":
    main()
