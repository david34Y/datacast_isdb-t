class CustomHeader:
    def __init__(self, transmission, reserved_bits, chunk_number, package_size, counter):
        self.transmission = transmission
        self.reserved_bits = reserved_bits
        self.chunk_number = chunk_number
        self.package_size = package_size
        self.counter = counter

    def to_bytes(self):
        # Pack header fields into a binary representation
        values = (
            (self.transmission << 6) |
            ((self.reserved_bits >> 8) & 0x3F),
            (self.reserved_bits & 0xFF),
            ((self.chunk_number >> 8) & 0x7F),
            (self.chunk_number & 0xFF),
            (self.package_size >> 8),
            (self.package_size & 0xFF),
            (self.counter >> 8),
            (self.counter & 0xFF)
        )

        return bytes(values)


class HeaderReader:
    @staticmethod
    def read_header(header_bytes):
        transmission = (header_bytes[0] >> 6) & 0x03
        reserved_bits = ((header_bytes[0] & 0x3F) << 8) | header_bytes[1]
        chunk_number = ((header_bytes[2] & 0x7F) << 8) | header_bytes[3]
        package_size = (header_bytes[4] << 8) | header_bytes[5]
        counter = (header_bytes[6] << 8) | header_bytes[7]

        print(f"Transmission: {bin(transmission)}")
        print(f"Reserved Bits: {reserved_bits}")
        print(f"Chunk Number: {chunk_number}")
        print(f"Package Size: {package_size} bytes")
        print(f"Counter: {counter}")
