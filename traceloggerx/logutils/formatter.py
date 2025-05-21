import json
import logging

from colorlog import ColoredFormatter

LOG_COLORS_CONFIG = {
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'bold_red',
}

class CustomColoredFormatter(ColoredFormatter):
    def format(self, record):
        record.white_asctime = f"\033[37m{self.formatTime(record, self.datefmt)}\033[0m"
        return super().format(record)

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

class JSONFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "filename": record.filename,
            "funcName": record.funcName,
            "lineNo": record.lineno,
            "process": record.process,
            "thread": record.threadName,
        }
        for key, value in record.__dict__.items():
            if key not in log_record and not key.startswith('_'):
                log_record[key] = value

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record, ensure_ascii=False)