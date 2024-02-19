from model import *
from model.relations import *
from model.cache import region, api


ID = 2
KEY = f'id_food{ID}'
pero = region.get(KEY)
print(pero)
if pero is api.NO_VALUE:
    pero = Session.query(Book).filter(Book.ID_book==ID).one()
    region.set(KEY, pero)