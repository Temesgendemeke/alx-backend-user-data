#!/usr/bin/env python3
"""
Main file
"""
import re

def filter_datum(fields: list, redaction: str, message: str, separator: str) -> str:
     """ returns the log message obfuscated """
     for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
     return message
