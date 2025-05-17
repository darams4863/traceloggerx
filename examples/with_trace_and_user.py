from logutils.logger import set_logger

# Logger with default user_id
logger = set_logger("user-session", extra={"user_id": "user_123"})

# Each log can carry an individual trace_id
logger.info("Page visited", extra={"trace_id": "req-456"})