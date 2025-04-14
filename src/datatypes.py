def get_datatype_size(name: str) -> int:
    data_sizes = {
        "UWORD": 2,
        "UBYTE": 1,
        "SBYTE": 1,
        "SWORD": 2,
        "ULONG": 4,
        "SLONG": 4,
        "FLOAT32_IEEE": 4,
    }
    return data_sizes[name]
