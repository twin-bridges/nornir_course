import logging
from nornir import InitNornir

logger = logging.getLogger("nornir")


nr = InitNornir(config_file="config.yaml")
logger.info("Test message")
logger.info("Test message")
logger.info("Test message")
logger.info("Test message")

logger.critical("Super critical")
logger.error("Super error")
logger.level = 10
logger.debug("Hello!!!")
logger.warning("Foo")
