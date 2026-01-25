from argparse import ArgumentParser, Namespace
from logging import Logger
import logging


def main():
    
    logger: Logger = logging.getLogger("digsinet-v2")
    
    parser: ArgumentParser = ArgumentParser(
        description="digsinet-v2 command line interface",
    )

    parser.add_argument("--debug", help="Enable debug logging", action="store_true")
    parser.add_argument("--stop", help="Stop all siblings and cleanup containers", action="store_true")
    parser.add_argument("--config", help="Path to configuration file, defaults to digsinet.py", type=str, default="digsinet.yml")

    arguments: Namespace = parser.parse_args()



if __name__ == "__main__":
    main()
