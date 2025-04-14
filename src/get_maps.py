import sys

from pya2l import model
from pya2l.api import inspect
from src.datatypes import get_datatype_size



def check_dependencies():
    try:
        import numpy
    except ImportError:
        print("Error: numpy is not installed.")
        sys.exit(1)

    try:
        import scipy
    except ImportError:
        print("Error: scipy is not installed.")
        #sys.exit(1)
        pass

    #print("Both numpy and scipy are installed.")

def calc_map_size(session, mapname: str):
    try:
        #mapname = 'ZWDKM1'
        characteristic = inspect.Characteristic(session, mapname)
        # Calc X-Values:
        datatype = characteristic.deposit.fncValues["datatype"]
        data_size = get_datatype_size(datatype)
        map_size = data_size
        for axis_ref in characteristic.axisDescriptions:
            map_size *= axis_ref.maxAxisPoints
        # Calc X Axis:
        if characteristic.deposit.axisPts["x"]:
            map_size += characteristic.deposit.axisPts["x"]["memSize"]
        # Calc Y Axis:
        if characteristic.deposit.axisPts["y"]:
            map_size += characteristic.deposit.axisPts["y"]["memSize"]
        # No Axis:
        if characteristic.deposit.noAxisPts["x"]:
            map_size += get_datatype_size(characteristic.deposit.noAxisPts["x"]["datatype"])

    except Exception as e:
        map_size = 1
        print(e)
        print(mapname)
        pass
    return map_size


def get_maps(session):
    check_dependencies()
    characteristics = session.query(model.Characteristic).order_by(model.Characteristic.name).all()
    retmaps = {}
    for characteristic in characteristics:
        name = characteristic.name
        #if name != "LDRXN_1_A":
        #    continue
        description = characteristic.longIdentifier
        type = "map"
        ecu_address = characteristic.address
        #ecu_address = ecu_address - 0xE00000
        size = calc_map_size(session, characteristic.name)

        retmaps[name] = {
            'name': name,
            'description': description,
            'type': type,
            # Read Addr:
            'addr': hex(ecu_address),
            'size': size,
        }
    return retmaps
