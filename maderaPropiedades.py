__author__ = 'manuel'
from decimal import *


class MaderaPropiedades:
    getcontext().prec = 10
    # conductividad termina
    kw = Decimal(0.14)
    # capacidad calorifica
    cw = Decimal(1700)
    #densidad
    densw = Decimal(600)
    # longitud
    xw = Decimal(0.011)

    def __getattr__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        self.__dict__[key] = value
