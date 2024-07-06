#!/usr/bin/env python3
"""
Main file
"""
import re


def filter_datum(fields, redaction, message, separator) -> str:
     """ Returns the log message obfuscated """
     pattern: str = r'({}=)[^{}]+'.format('|'.join(fields), separator)
     return re.sub(pattern, r'\1{}'.format(redaction), message)
