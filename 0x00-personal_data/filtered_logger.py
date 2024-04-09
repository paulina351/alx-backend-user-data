#!/usr/bin/env python3
"""Regex-ing
"""

import re
from typing import List
import logging

PIL_FIELDS = ('name', 'password', 'phone', 'ssn', 'email')


def filter_datum(fields: List[str], redaction: str,
                 message: str, seperator: str) -> str:
    """log message"""
    for field in fields:
        message = re.sub(f'{field}=.*?{seperator}',
                         f'{field}={redaction}{seperator}', message)
    return message


class RdactingFormatter(logging.Formatter):
    """RedactingFormatter"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPERATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """values using filter_datum"""
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPERATOR)


def get_logger() -> logging.Logger:
    """logging object"""
    logger = loging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    logger.setFormatter(RedactingFormatter(PIL_FIELDS))
    logger.addHandler(stream_handler)

    return logger
