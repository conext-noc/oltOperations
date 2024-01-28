import binascii

def hex_to_string(hex_string):
    unhex_bytes = binascii.unhexlify(hex_string.replace("0x",""))

    # Extract individual components
    year = int.from_bytes(unhex_bytes[:2], byteorder='big')
    month, day, hour, minute, second, timezone = unhex_bytes[2:8]

    return (f"{year}-{month}-{day}", f"{hour}:{minute}:{second}")
