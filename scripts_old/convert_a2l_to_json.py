import os.path

from a2ltools import read_a2l_static_values, read_a2l_variables
from src.json import write_json_file

a2l_file = "8E0907115D_Original.A2L"
json_file = a2l_file[:-4] + ".json"

static_values = read_a2l_static_values(a2l_file)
dynamic_values = read_a2l_variables(a2l_file)
allvalues = {**static_values, **dynamic_values}
write_json_file(json_file, allvalues)
