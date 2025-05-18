from traceloggerx import set_logger

# Basic logger without trace or user info
logger = set_logger("basic")

logger.info("Service started.")
logger.debug("Debugging info here.")
logger.warning("This is a warning.")
logger.error("Something went wrong.")