"""
This module provides a function to calculate a 32-bit MurmurHash2 fingerprint
for a given file, ignoring whitespace characters. This is the "new" code.
"""
from __future__ import annotations

from pathlib import Path

from numpy import fromfile, uint32, uint8


def get_fingerprint(file_path: str | Path) -> int:
    """
    Calculates a 32-bit MurmurHash2 fingerprint of a file's content.

    This implementation reads the file into a NumPy array and processes it in
    chunks for efficiency. It specifically ignores whitespace characters:
    space (32), tab (9), newline (10), and carriage return (13).

    Args:
        file_path: The path to the file to be processed.

    Returns:
        The 32-bit integer fingerprint of the file content.

    Raises:
        FileNotFoundError: If the file does not exist at the specified path.
    """

    _fromfile = fromfile
    _uint8 = uint8
    _uint32 = uint32
    MULTIPLEX = _uint32(1540483477)
    SEED = _uint32(1)

    try:
        raw_bytes = _fromfile(file_path, dtype=_uint8)
        clean_data = raw_bytes[
            (raw_bytes != 9) &
            (raw_bytes != 10) &
            (raw_bytes != 13) &
            (raw_bytes != 32)
        ]
    except FileNotFoundError:
        raise

    data_len = _uint32(len(clean_data))
    fingerprint = SEED ^ data_len

    chunk_count = len(clean_data) // 4
    if chunk_count > 0:
        chunks = clean_data[:chunk_count * 4].view(dtype=_uint32)

        chunks *= MULTIPLEX
        chunks ^= chunks >> 24
        chunks *= MULTIPLEX

        for value in chunks:
            fingerprint = (fingerprint * MULTIPLEX) ^ value

    tail_index = chunk_count * 4
    tail = clean_data[tail_index:]
    tail_len = len(tail)

    if tail_len > 0:
        tail_word = _uint32(0)
        if tail_len >= 3:
            tail_word ^= _uint32(tail[2]) << 16
        if tail_len >= 2:
            tail_word ^= _uint32(tail[1]) << 8
        tail_word ^= _uint32(tail[0])

        fingerprint = (fingerprint ^ tail_word) * MULTIPLEX


    fingerprint ^= fingerprint >> 13
    fingerprint *= MULTIPLEX
    fingerprint ^= fingerprint >> 15

    return int(fingerprint)
