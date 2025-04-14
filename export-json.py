from pya2l import DB, model

from src.datatypes import get_datatype_size
from src.get_maps import get_maps
from src.get_vars import get_vars
from src.json import write_json_file



filename = "8E0907115D_Original.a2l"

a2l_name = filename[:-4] + "_preprocessed.a2l"
json_file = filename[:-4] + ".json"

db = DB()
session = db.open_existing(a2l_name)


static_values = get_maps(session)
dynamic_values = get_vars(session)
allvalues = {**static_values, **dynamic_values}
write_json_file(json_file, allvalues)
