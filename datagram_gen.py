from pathlib import Path
import math
from file_framer import read_and_chunk_file
from DvHeader import CustomHeader, HeaderReader
from pdu_gen import create_pdus
import binascii
from crccheck.crc import Crc32Mpeg2

def create_datagrams(file_name, chunk_size):
    pdus = create_pdus(file_name, chunk_size)
    datagrams = []

    for pdu in pdus:
        crc = Crc32Mpeg2.calc(pdu)
        
        if len(hex(crc)[2:]) == 8:
            crc_byte = binascii.unhexlify(hex(crc)[2:])
        else:    
            strcrc = "0" * (8 - len(hex(crc)[2:])) + hex(crc)[2:]
            crc_byte = binascii.unhexlify(strcrc)

        datagrams.append(pdu + crc_byte)

    return datagrams

