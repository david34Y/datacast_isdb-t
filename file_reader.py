import binascii
import math
import sys
from pathlib import Path
from file_framer import read_and_chunk_file

def recover_file(provided_chunks, provided_padding_bytes):
    # Check if the provided information is complete
    if not provided_padding_bytes or not provided_chunks:
        print("Provided information is incomplete.")
        sys.exit(1)

    # Calculate the padding size based on the provided padding bytes
    padding_size = provided_padding_bytes

    # Add padding if needed to the last chunk
    if padding_size > 0:
        padding_bytes = bytes([0xFF] * padding_size)
        provided_chunks[-1] += padding_bytes

    # Concatenate the chunks to reconstruct the original file
    reconstructed_file = b''.join(provided_chunks)

    return reconstructed_file

# Example usage
chunk_size = 172
archivo = 'Contenido.jpg'
provided_padding_bytes = 23  # Enter the provided number of padding bytes
provided_chunks = read_and_chunk_file(archivo, chunk_size)  # Enter the provided list of chunks

reconstructed_file = recover_file(provided_chunks, provided_padding_bytes)

# Save the reconstructed file
output_file = 'Recovered_' + archivo
with open(output_file, 'wb') as output:
    output.write(reconstructed_file)

print(f"File recovered and saved as: {output_file}")
