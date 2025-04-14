import chardet
from pya2l import DB
from pya2l.build import model

from src.preprocess_a2l import preprocess_a2l

filename = "8E0907115D_Original.A2L"

a2l_name = filename[:-4] + "_preprocessed.a2l"
preprocess_a2l(filename, a2l_name)

db = DB()
session = db.import_a2l(a2l_name, remove_existing=True)
