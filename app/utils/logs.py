import logging
import sys
from os import getenv
from pathlib import Path
from loguru import logger


log_format = (
    '{{<level>"level": "{level}"</level>, '
    '<green>"time":  "{time:YYYY-MM-DD HH:mm:ss.SSS}"</green>, '
    '"request_id": "{extra[request_id]}", '
    '<cyan>"name": "{name}"</cyan>, '
    '<cyan>"function": "{function}"</cyan>, '
    '"message": "{message}" }}'
)

logging_config = {
    "path": getenv('LOG_PATH', "../logs"),
    "filename": getenv('LOG_NAME', "app.log"),
    "level": getenv('LOGLEVEL', "info"),
    "rotation": getenv('ROTATION', "20 days"),
    "retention": getenv('RETENTION', "1 months"),
}


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:  # pragma: no cover
            level = self.loglevel_mapping[record.levelno]  # pragma: no cover

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())


class FilterQuotes(logging.Filter):
    @classmethod
    def filter_quotes(cls, record):
        record['message'] = record['message'].replace('"', "'")
        return record


class CustomizeLogger:

    @classmethod
    def make_logger(cls):
        logger = cls.customize_logging(
            Path(logging_config.get('path')),
            Path(logging_config.get('filename')),
            level=logging_config.get('level'),
            retention=logging_config.get('retention'),
            rotation=logging_config.get('rotation'),
            format=log_format
        )
        return logger

    @classmethod
    def customize_logging(
        cls,
        filepath: Path,
        filename: Path,
        level: str,
        rotation: str,
        retention: str,
        format: str
    ):

        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
            filter=FilterQuotes.filter_quotes
        )
        logger.add(
            str(filepath/filename),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
            filter=FilterQuotes.filter_quotes
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ['uvicorn',
                     'uvicorn.error',
                     'fastapi'
                     ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)
