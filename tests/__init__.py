#!/usr/bin/python3
"""
Utility functions for file operations
"""
import os
from typing import TextIO
from models.engine.file_storage import FileStorage


def cle_st(stream: TextIO):
    """Clear the content of the given stream"""
    if stream.seekable():
        stream.seek(0)
        stream.truncate(0)


def de_fi(file_path: str):
    """Delete the file at the specified path if it exists"""
    if os.path.isfile(file_path):
        os.unlink(file_path)


def re_st(store: FileStorage, file_path='file.json'):
    """Reset the FileStorage object by reloading data"""
    with open(file_path, mode='w') as file:
        file.write('{}')
        if store is not None:
            store.reload()


def re_te_f(file_name):
    """Read and return the contents of the specified file"""
    lines = []
    if os.path.isfile(file_name):
        with open(file_name, mode='r') as file:
            for line in file.readlines():
                lines.append(line)
    return ''.join(lines)


def wri_te_fi(file_name, text):
    """Write the given text to the specified file"""
    with open(file_name, mode='w') as file:
        file.write(text)
