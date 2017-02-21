__author__ = 'manuel'
from decimal import *


class AislantePropiedades:
    getcontext().prec = 10
    # conductividad termina
    # capacidad calorifica
    kr = Decimal(0.038)
    cr = Decimal(1674)
    #densidad
    densr = Decimal(30)
    # longitud
    xr = Decimal(0.06)

    def __getattr__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        self.__dict__[key] = value
