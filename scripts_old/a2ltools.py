import re


def get_c_type_size(type):
    type_size_mapping = {
        'UBYTE': 1,
        'SBYTE': 1,
        'SWORD': 2,
        'UWORD': 2,
        'ULONG': 4,
        'SLONG': 4,
        'UFLOAT': 4,
        'FLOAT32_IEEE': 4,
        # Add more types as needed
    }

    size = type_size_mapping.get(type)

    if size is not None:
        return size
    else:
        raise Exception("Not implemented: " + type)


def get_med9_size(type):
    type_size_mapping = {
        'KwbUb': 'UBYTE',
        'KwbUw': 'UWORD',
        'KwbWS8': 'SBYTE',
        'KwbWU16': 'UWORD',
        'KwbWU32': 'ULONG',
        'KwbWU8': 'UBYTE',
        'KwSb': 'SBYTE',
        'KwSw': 'SWORD',
        'KwUb': 'UBYTE',
        'KwUl': 'ULONG',
        'KwUw': 'UWORD',
        'KwWS16': 'SWORD',
        'KwWS32': 'SLONG',
        'KwWS8': 'SBYTE',
        'KwWU16': 'UWORD',
        'KwWU32': 'ULONG',
        'KwWU8': 'UBYTE',
        'KwbUl': 'ULONG',
        '_REC_S1VAL_20_u1': "UBYTE",
        '_REC_S1VAL_20_s2': "UWORD",
        # MED9.2:
        'KwWR32': "ULONG",
        'KwbWR32': "ULONG",
        'KwbSw': "SWORD",
        'KwbSb': "SBYTE",
        '_REC_S1VAL_20_u2': 'UWORD',
        '_REC_VAL___DDS__Nor_u1': 'UBYTE',
        '_REC_VAL___DDS__Nor_s2': 'SWORD',
        '_REC_VAL_20_u1': 'UBYTE',
        '_REC_VAL_20_s2': 'SWORD',
        '_REC_S1VAL_20_U2': 'UWORD',
        '_REC_S1VAL_20_U1': 'UBYTE',
        '_REC_S1VAL_20_S2': 'SWORD',
        '_REC_S1VAL_20_S1': 'SBYTE',
        '_REC_S1VAL_20_U4': "ULONG",
        '_REC_S1VAL_2_U1': 'UBYTE',
        '_REC_S1VAL_20_S4': 'SLONG',
        '_REC_S1VAL_20_F4': 'FLOAT32_IEEE',
        '_REC_S1VAL_2_U2': "UWORD",
        '_REC_S1VAL_2_U4': "ULONG",
        # MSV 70:
        '_REC_VAL_2_u1': "UBYTE",
        '_REC_VAL_2_u2': "UWORD",
        '_REC_VAL_2_s1': "SBYTE",
        '_REC_VAL_2_s2': 'SWORD',
        '_REC_VAL_2_S4': 'FLOAT32_IEEE',
        '_REC_VAL_20_u2': "UWORD",
        '_REC_VAL_20_s1': "SBYTE",
        '_REC_VAL_20_u4': 'ULONG',
        '_REC_VAL_20_S4': 'FLOAT32_IEEE',
        # MED 17:
        'Val_Ws8': "SBYTE",
        'Val_Ws16': 'SWORD',
        'Val_Ws32': 'SLONG',
        'Val_Wu8': "UBYTE",
        'Val_Wu16': 'UWORD',
        'Val_Wu32': 'ULONG',

        'Kw_Ws8': "SBYTE",
        'Kw_Ws16': 'SWORD',
        'Kw_Ws32': 'SLONG',
        'Kw_Wu8': "UBYTE",
        'Kw_Wu16': 'UWORD',
        'Kw_Wu32': 'ULONG',

        'ValA_Wu8': "UBYTE",
        'ValA_Wu16': "UWORD",
        'ValA_Wu32': "ULONG",
        'ValA_Ws8': "SBYTE",
        'ValA_Ws16': "SWORD",
        'ValA_Ws32': "SLONG",

        'KwbWS16': "SWORD",
        'RB_Val_Wu8': "UBYTE",


        '_REC_S1VAL_20_SV_U1' : "UBYTE",
        '_REC_S1VAL_20_SV_U2' : 'UWORD',
        '_REC_S1VAL_20_SV_S1': 'SBYTE',
        '_REC_S1VAL_20_SV_U4': "ULONG",
        '_REC_S1VAL_20_SV_S2' : "UWORD",
        'RB_Val_Ws16' : "SWORD",
        'RB_Val_Ws32' :"SLONG",
        'RB_Val_Wu16' : "UWORD",
        'RB_ValA_Wu16' : 'UWORD',
        'RB_Val_Wu32': "ULONG",
        'Kwb_Wu32' : "ULONG",

        'KwSl':'SLONG'

    }

    size = type_size_mapping.get(type)

    if size is not None:
        return size
    else:
        #raise("Not implemented: " + type)
        print("Not implemented: " + type)
        return "ULONG"


def read_a2l_variables(filename):
    '''
    Credits go to: http://nefariousmotorsports.com/forum/index.php?topic=13749.0title=
    Args:
        filename: filenameo of a2l

    Returns: dict of measurements

    '''
    retmaps = {}
    with open(filename, 'r', encoding='latin-1') as fp:
        measurements = fp.read().split("/begin MEASUREMENT")
        # Removes Asap Line
        measurements.pop(0)
        # print("Found: %d measurement(s)" % len(measurements))
        for m in measurements:
            splitted = m.split("\n")
            # Strip array
            splitted = [s.strip() for s in splitted]
            # Remove all void strings
            splitted = [s for s in splitted if s != ""]
            name = splitted[0]
            description = splitted[1]
            size = get_c_type_size(splitted[2])
            ecu_address = [s for s in splitted if s.startswith("ECU_ADDRESS")]
            if len(ecu_address) > 0:
                ecu_address = ecu_address[0]
                ecu_address = ecu_address.replace('ECU_ADDRESS', '').strip()
            else:
                print("ERROR: Address not found, A2L wrong")

            bitmask = [s for s in splitted if s.startswith("BIT_MASK")]
            if len(bitmask) > 0:
                bitmask = bitmask[0]
                bitmask = bitmask.replace('BIT_MASK', '').strip()
                bitmask = re.findall(r'0x[0-9a-fA-F]{1,2}', bitmask)
                if len(bitmask) > 0:
                    bitmask = bitmask[0]
                else:
                    bitmask = False
            else:
                bitmask = False

            # elif (l.startswith("ECU_ADDRESS")):
            # addr = l[12:]

            retmaps[name] = {
                'name': name,
                'description': description,
                'type': "dynamic_variable",
                # Read Addr:
                'addr': ecu_address,
                'size': size,
            }
            if bitmask:
                retmaps[name]["bitmask"] = bitmask

    return retmaps


def match_asap_block(strings):
    ecu_address = 0
    hex_addresses = []
    pattern = r'/begin IF_DATA ASAP1B_KWP2000  DP_BLOB  (0[xX][0-9A-Fa-f]+).*?  /end IF_DATA'

    for s in strings:
        match = re.search(pattern, s)
        if match:
            hex_addresses.append(match.group(1))
    if len(hex_addresses):
        ecu_address = int(hex_addresses[0], 16)
    return ecu_address


def read_a2l_static_values(filename):
    '''
    Credits go to: http://nefariousmotorsports.com/forum/index.php?topic=13749.0title=
    Args:
        filename: filenameo of a2l

    Returns: dict of measurements

    '''
    retmaps = {}
    with open(filename, 'r', encoding='latin-1') as fp:
        static_values = fp.read().split("/begin CHARACTERISTIC")
        # Removes Asap Line
        static_values.pop(0)
        # print("Found: %d measurement(s)" % len(measurements))
        for m in static_values:
            splitted = m.split("\n")
            # Strip array
            splitted = [s.strip() for s in splitted]
            # Remove all void strings
            splitted = [s for s in splitted if s != ""]
            name = splitted[0]
            description = splitted[1]
            type = splitted[2]

            ecu_address = match_asap_block(splitted)
            if ecu_address == 0:
                ecu_address = splitted[3]
                ecu_address = int(ecu_address, 16)
            # ecu_address = ecu_address + 0x400000
            # ecu_address -= 0xE00000
            # ecu_address += 0x400000
            ecu_address = hex(ecu_address)
            if type == "VALUE":
                type = "static_variable"
                size = splitted[4]
                size = get_med9_size(size)
                size = get_c_type_size(size)
            elif type == "VAL_BLK":
                type = "static_variable"
                size = splitted[4]
                size = get_med9_size(size)
                size = get_c_type_size(size)
            elif type == "ASCII":
                type = "static_string"
                size = 1
            elif type == "CURVE":
                type = "map"
                size = 1
            elif type == "MAP":
                type = "map"
                size = 1
            elif type == "CUBOID":
                type = "map"
                size = 1
            else:
                raise Exception("Not implemented: " + type)

            retmaps[name] = {
                'name': name,
                'description': description,
                'type': type,
                # Read Addr:
                'addr': ecu_address,
                'size': size,
            }

    return retmaps
