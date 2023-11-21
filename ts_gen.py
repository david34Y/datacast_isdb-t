import struct
from crccheck.crc import Crc32Mpeg2
from datagram_gen import create_datagrams

def generate_pat():
    # PAT header
    pat_header = struct.pack('>BBHH', 0x47, 0x40, 0, 0)  # TS header, PAT table_id, section_syntax_indicator, etc.

    # PAT payload
    pat_payload = struct.pack('>BBHH', 0, 0, 0xB00D, 1)  # program_number, reserved, PID for PMT, etc.

    # Calculate CRC32 for the PAT payload
    crc32 = Crc32Mpeg2.calc(pat_payload)
    pat_payload += struct.pack('>I', crc32)

    return pat_header + pat_payload

def generate_pmt():
    # PMT header
    pmt_header = struct.pack('>BBHH', 0x47, 0x50, 0, 0)  # TS header, PMT table_id, section_syntax_indicator, etc.

    # PMT payload
    pmt_payload = struct.pack('>BBHBBHHBB', 0, 0, 0xB00D, 1, 0xE0, 0x1B, 0xE1, 0xF0, 0xF)  # program_number, reserved, PID for video, etc.

    # Calculate CRC32 for the PMT payload
    crc32 = Crc32Mpeg2.calc(pmt_payload)
    pmt_payload += struct.pack('>I', crc32)

    return pmt_header + pmt_payload

def generate_payload(pid, data):
    # Payload header
    payload_header = struct.pack('>BBHH', 0x47, 0x40 | (pid >> 8), pid & 0xFF, 0)  # TS header, PID, etc.

    # Join the list of datagrams into a single bytes object
    payload = b''.join(data)

    return payload_header + payload

# Example video data
video_pid = 0x100  # Example PID for video stream
video_data = create_datagrams('Contenido.jpg', 172)

# Generate video payload packets
video_packets = [generate_payload(video_pid, video_data[i:i+184]) for i in range(0, len(video_data), 184)]

# Write to a TS file
with open('output.ts', 'wb') as ts_file:
    ts_file.write(generate_pat())
    ts_file.write(generate_pmt())
    for video_packet in video_packets:
        ts_file.write(video_packet)

print("TS file generated successfully.")
