#!/usr/bin/env python3
"""
Main file
"""
import re
import logging


def filter_datum(fields: list, redaction: str,
                 message: str, separator: str) -> str:
   """ returns the log message obfuscated """
   for field in fields:
      message = re.sub(f"{field}=.*?{separator}", f"{field}={redaction}{separator}", message)
   return message
 


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list):
        """" constructor method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filter values in incoming log records"""
        NotImplementedError
        return filter_datum(self.fields, self.REDACTION, super().format(record), self.SEPARATOR)
