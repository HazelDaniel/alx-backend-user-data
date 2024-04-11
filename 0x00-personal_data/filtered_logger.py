#!/usr/bin/env python3
""" Using regex to replace occurrences of field values in ; separated fields"""
import re
from typing import List
import logging
import os


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """obfuscates log messages with regex"""
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message
