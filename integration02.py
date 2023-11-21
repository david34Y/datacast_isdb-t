from pathlib import Path
import math
from file_framer import read_and_chunk_file
from DvHeader import CustomHeader, HeaderReader
from pdu_gen import create_pdus
import binascii
from crccheck.crc import Crc32Mpeg2

# Example usage
archivo = 'Contenido.jpg'
chunk_size = 172
pdus = create_pdus(archivo, chunk_size)
pdud = list()

for pdu in pdus:
    crc = Crc32Mpeg2.calc(pdu)
    if len(hex(crc)[2:])==8: 
        crc_byte = binascii.unhexlify(hex(crc)[2:])
    else:    
        strcrc = "0"*(8-len(hex(crc)[2:])) + hex(crc)[2:]
        crc_byte = binascii.unhexlify(strcrc)

    pdud.append(pdu+crc_byte)

print(len(pdud[1]))
print(len(pdud[-1]))