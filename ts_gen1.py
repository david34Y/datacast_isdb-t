import struct
from crccheck.crc import Crc32Mpeg2
from datagram_gen import create_datagrams

def generate_pat():
    pat_header = struct.pack('>BBHH', 0x47, 0x40, 0, 0)
    pat_payload = struct.pack('>BBHH', 0, 0, 0xB00D, 0x100)  # Unique PID for PMT
    crc32 = Crc32Mpeg2.calc(pat_payload)
    pat_payload += struct.pack('>I', crc32)
    # Add padding bytes to make the total length equal to 188
    padding_bytes = b'\xFF' * (188 - len(pat_payload))
    pat_payload += padding_bytes
    
    return pat_header + pat_payload

def generate_pmt():
    pmt_header = struct.pack('>BBHH', 0x47, 0x50, 0, 0)
    pmt_payload = struct.pack('>BBHHHHBBHHBB', 0, 0, 0xB00D, 0x100, 0xE0, 0x1B, 0xE1, 0xF0, 0xF, 0, 0, 0)

    crc32 = Crc32Mpeg2.calc(pmt_payload)
    pmt_payload += struct.pack('>I', crc32)
    # Add padding bytes to make the total length equal to 184
    padding_bytes = b'\xFF' * (184 - len(pmt_header + pmt_payload))
    pmt_payload += padding_bytes
    return pmt_header + pmt_payload

def generate_payload(pid, data, continuity_counter):
    # Payload header
    payload_header = struct.pack('>BBHHB', 0x47, 0x40 | (pid >> 8), pid & 0xFF, 0, 0x30 | (continuity_counter & 0x0F))

    # Payload
    payload = b"".join(data)


    return payload_header + payload



# Example video data
video_pid = 0x101  # Unique PID for video stream
video_data = create_datagrams('Contenido.jpg', 172)

continuity_counter = 0

# Generate video payload packets
video_packets = [generate_payload(video_pid, video_data[i:i+184], continuity_counter) for i in range(0, len(video_data), 184)]
continuity_counter = (continuity_counter + 1) % 16  # Increment and wrap around after 15


# Write to a TS file
with open('output.ts', 'wb') as ts_file:
    ts_file.write(generate_pat())
    ts_file.write(generate_pmt())
    for video_packet in video_packets:
        ts_file.write(video_packet)

print("TS file generated successfully.")
