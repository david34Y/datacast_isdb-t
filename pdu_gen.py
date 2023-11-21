from pathlib import Path
import math
from file_framer import read_and_chunk_file
from DvHeader import CustomHeader

def create_pdus(file_name, chunk_size):
    resulting_chunks, padding_size = read_and_chunk_file(file_name, chunk_size)
    resulting_chunks_length = len(resulting_chunks)

    file_size = Path(file_name).stat().st_size
    file_size_counter = math.ceil(file_size / chunk_size)

    dvheaders = []
    for i in range(resulting_chunks_length - 1):
        custom_header = CustomHeader(0b00, 0, file_size_counter, file_size, i + 1)
        header_bytes = custom_header.to_bytes()
        dvheaders.append(header_bytes)

    final_custom_header = CustomHeader(0b00, padding_size, file_size_counter, file_size, resulting_chunks_length)
    dvheaders.append(final_custom_header.to_bytes())

    pdus = []
    for i in range(resulting_chunks_length):
        pdus.append(dvheaders[i] + resulting_chunks[i])

    return pdus
