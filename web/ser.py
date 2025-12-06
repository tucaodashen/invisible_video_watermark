from BasicSystem.log_client import setup_logger, get_logger

setup_logger(default_tags="main", enable_udp=True, enable_console=True)
logger = get_logger()

logger.debug("This is a debug")
logger.info("This is an info")
logger.error("This is an error")
logger.critical("This is a critical")
logger.success("This is a success")
