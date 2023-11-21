import binascii
import math
from pathlib import Path
import sys

def read_and_chunk_file(file_path, chunk_size):
    file_size = Path(file_path).stat().st_size
    file_size_counter = math.ceil(file_size / chunk_size)

    # Read the file in chunks and store in a list
    chunks = []
    with open(file_path, 'rb') as file:
        for _ in range(file_size_counter):
            chunk = file.read(chunk_size)
            if not chunk:
                break
            chunks.append(chunk)

    # Check if the last chunk needs padding
    last_chunk_size = len(chunks[-1])
    padding_size = chunk_size - last_chunk_size

    # Add padding if needed
    if padding_size > 0:
        padding_bytes = bytes([0xFF] * padding_size)
        chunks[-1] += padding_bytes


    return chunks, padding_size