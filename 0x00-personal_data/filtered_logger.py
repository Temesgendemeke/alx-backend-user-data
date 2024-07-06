#!/usr/bin/env python3
"""
Main file
"""
import re


def filter_datum(fields: list, redaction: str, message: str, separator: str) -> str:
    return re.sub(f"({'|'.join(fields)})=([^{separator}]*)", f"\\1={redaction}", message)
