import urllib

from pya2l import model

from src.datatypes import get_datatype_size


def unescape_unicode(escaped_string):
    """
    Unescape a string containing Unicode escape sequences (e.g., '\\u00e4' -> 'ä') and
    handle potential double encoding issues.

    Parameters:
    escaped_string (str): The string containing Unicode escape sequences.

    Returns:
    str: The unescaped string.
    """
    # First, decode any Unicode escape sequences
    decoded_string = escaped_string.encode('utf-8').decode('unicode_escape')

    # Check if the string still contains characters that appear double encoded
    try:
        # Attempt to decode the string again to handle double encoding
        decoded_string = bytes(decoded_string, 'utf-8').decode('utf-8')
    except UnicodeDecodeError:
        pass

    return decoded_string


def get_vars(session):
    measurements = session.query(model.Measurement).order_by(model.Measurement.name).all()
    retmaps = {}
    for m in measurements:
        name = m.name
        #break
        #if name != "B_mxps2e":
        #    continue
        description = m.longIdentifier
        type = "variable"
        if m.ecu_address is None:
            print("Problem...")
            continue

        ecu_address = m.ecu_address.address
        size = get_datatype_size(m.datatype)
        arr = {
            'name': name,
            'description': description,
            'type': type,
            # Read Addr:
            'addr': hex(ecu_address),
            'size': size,
        }
        # Bit mask:
        if m.bit_mask:
            arr["bit_mask"] = hex(m.bit_mask.mask)
        #BIT_MASK

        retmaps[name] = arr
    return retmaps
