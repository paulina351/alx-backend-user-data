#!/usr/bin/env python3
"""Regex-ing
"""

import re
import logging
import os
import mysql.connector
from typing import List

PIL_FIELDS = ('name', 'password', 'phone', 'ssn', 'email')


def get_db() -> mysql.connector.connection.MySQLConnection:
    """connection to mysql"""
    user = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")
    myDB = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=db_name
    )
    return myDB


class RedactingFormatter(logging.Formatter):
    """A class implementation"""

    REDACTION = "****"
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

        def filter_datum(fields: List[str], redaction: str,
                         message: str, eperator: str) -> str:
            """return log"""
            for field in fields:
                message = re.sub(rf'{field}=(.*?){seperator}',
                                 f'{field}={redaction}{seperator}', message)
            return message


def get_logger() -> logging.Logger:
    """logging object"""
    logger = loging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    logger.setFormatter(RedactingFormatter(PIL_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def main() -> None:
    """Function"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        message = ""
        for a in range(len(row)):
            message += f"{PIL_FIELDS[a]}={row[a]};"
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
