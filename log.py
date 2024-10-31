import datetime
import json
import logging
import os

from colorama import Fore, init
from enum import Enum
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from pythonjsonlogger import jsonlogger
from typing import Any, Dict


init(autoreset=True)


class EventType(Enum):
    LOG = 1
    TASK_STARTED = 2
    TASK_FINISHED = 3
    TASK_STOPPED = 4
    TASK_CRASHED = 5
    STEP_COMPLETE = 6
    PROGRESS = 7
    METRICS = 8


LOGGING_COLOR = {
    # "FATAL": Fore.RED,
    "ERROR": Fore.RED,
    "WARNING": Fore.YELLOW,
    "INFO": Fore.GREEN,
    "DEBUG": Fore.BLUE,
    # "TRACE": Fore.CYAN,
}

def _get_default_logging_fields():
    supported_keys = [
        "asctime",
        # 'created',
        'filename',
        'funcName',
        'levelname',
        # 'levelno',
        'lineno',
        # 'module',
        # 'msecs',
        "message",
        # 'name',
        # 'pathname',
        # 'process',
        # 'processName',
        # 'relativeCreated',
        # 'thread',
        # 'threadName'
    ]
    return " ".join(["%({0:s})".format(k) for k in supported_keys])


def dumps_ignore_nan(obj, *args, **kwargs):
    return json.dumps(obj, *args, **kwargs)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    additional_fields = {}

    def __init__(self, format_string, color):
        super().__init__(format_string, json_serializer=dumps_ignore_nan)
        self.color = color

    def process_log_record(self, log_record):
        log_record["timestamp"] = log_record.pop("asctime", None)

        levelname = log_record.pop("levelname", None)
        if levelname is not None:
            log_record["level"] = levelname.lower()

        e_info = log_record.pop("exc_info", None)
        if e_info is not None:
            if e_info == "NoneType: None":  # python logger is not ok here
                pass
            else:
                log_record["stack"] = e_info.split("\n")

        return jsonlogger.JsonFormatter.process_log_record(self, log_record)

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)

        for field, val in CustomJsonFormatter.additional_fields.items():
            if (val is not None) and (field not in log_record):
                log_record[field] = val

    def formatTime(self, record, datefmt=None):
        ct = datetime.datetime.fromtimestamp(record.created)
        t = ct.strftime("%Y-%m-%dT%H:%M:%S")
        s = "%s.%03dZ" % (t, record.msecs)
        return s

    def format(self, record: logging.LogRecord) -> str:
        """Formats a log record and serializes to json"""
        message_dict: Dict[str, Any] = {}
        if isinstance(record.msg, dict):
            message_dict = record.msg
            record.message = ""
        else:
            record.message = record.getMessage()
        if "asctime" in self._required_fields:
            record.asctime = self.formatTime(record, self.datefmt)

        if record.exc_info and not message_dict.get("exc_info"):
            message_dict["exc_info"] = self.formatException(record.exc_info)
        if not message_dict.get("exc_info") and record.exc_text:
            message_dict["exc_info"] = record.exc_text
        if record.stack_info and not message_dict.get("stack_info"):
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        log_record: Dict[str, Any] = {}
        self.add_fields(log_record, record, message_dict)
        log_record = self.process_log_record(log_record)
        if self.color:
            return f"\r{LOGGING_COLOR[record.levelname]}{self.serialize_log_record(log_record)}"
        return self.serialize_log_record(log_record)


def add_logger_handler(the_logger, log_handler, loglevel_text, color=True):
    logger_fmt_string = _get_default_logging_fields()
    formatter = CustomJsonFormatter(logger_fmt_string, color)
    formatter.json_ensure_ascii = False
    log_handler.setLevel(loglevel_text.upper())
    log_handler.setFormatter(formatter)
    the_logger.addHandler(log_handler)


def add_default_logging_into_console(the_logger, loglevel_text):
    log_handler = logging.StreamHandler()
    add_logger_handler(the_logger, log_handler, loglevel_text)


def add_default_logging_into_file(the_logger, loglevel_text, log_file):
    if not Path(log_file).parent.exists():
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    log_handler_file = TimedRotatingFileHandler(filename=log_file, when='D', interval=1, encoding="utf-8", delay=True)
    add_logger_handler(the_logger, log_handler_file, loglevel_text, False)


def set_global_logger(console_level="ERROR", add_file=True, file_level="INFO", log_file=os.path.join(os.getcwd(), "log.log")):
    the_logger = logging.getLogger('logger')
    the_logger.propagate = False
    the_logger.handlers = []
    the_logger.setLevel("DEBUG")

    if add_file:
        add_default_logging_into_file(the_logger, file_level, log_file)
        add_default_logging_into_console(the_logger, console_level)
    else:
        add_default_logging_into_console(the_logger, console_level)

    return the_logger
