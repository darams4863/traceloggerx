import io
import json
import logging
import sys
import traceback

from .formatter import CustomColoredFormatter
from .handlers import get_file_handler, get_stream_handler

ROOT_PKG = "default"

class ContextualLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        context = dict(self.extra) if self.extra else {}
        user_extra = kwargs.pop("extra", {})
        context.update(user_extra)
        kwargs["extra"] = context
        return msg, kwargs

def set_logger(
    pkg: str,
    log_dir: str = "./logs",
    level: str | int | None = None,
    stream_only: bool = False,
    json_format: bool = False,
    extra: dict | None = None
):
    logger = logging.getLogger(pkg)

    if isinstance(level, str):
        level_num: int = getattr(logging, level.upper(), logging.INFO)
    elif isinstance(level, int):
        level_num: int = level
    else:
        level_num: int = logging.DEBUG

    logger.setLevel(level_num)

    if not logger.handlers:
        logger.addHandler(get_stream_handler())
        if not stream_only:
            logger.addHandler(get_file_handler(pkg, log_base_dir=log_dir, json_format=json_format))

    if extra is None:
        extra = {}
    return ContextualLoggerAdapter(logger, extra)

def handle_exception(exc_type, exc_value, exc_traceback):
    logger = logging.getLogger(ROOT_PKG)
    formatted = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logger.error("Unhandled exception occurred:\n%s", formatted)

def init_logger():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
    sys.excepthook = handle_exception
    set_logger(ROOT_PKG)

class SafeColoredFormatter(CustomColoredFormatter):
    def format(self, record):
        extras = {}
        for k, v in record.__dict__.items():
            if k not in (
                'name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename',
                'module', 'exc_info', 'exc_text', 'stack_info', 'lineno', 'funcName',
                'created', 'msecs', 'relativeCreated', 'thread', 'threadName',
                'processName', 'process', 'white_asctime', 'log_color'
            ):
                extras[k] = v
        if extras:
            record.extra = json.dumps(extras, ensure_ascii=False)
        else:
            record.extra = ""
        return super().format(record)