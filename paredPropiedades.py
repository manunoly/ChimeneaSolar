__author__ = 'manuel'
from decimal import *


class ParedPropiedades:
    getcontext().prec = 10
    ## variables de la pared
    kp = Decimal(0.87)  # conductividad termica
    cpp = Decimal(1330)    # calor especifico pared especifico
    densp = Decimal(1800)
    alphap = Decimal(0.82) ## absortividad
    ep  = Decimal(0.95)  ## emisividad
    diff  = Decimal(6.23) * Decimal(10) ** Decimal(-7)  ## difusividad terminca  -- calculable
    x = Decimal(0.50) # distancia entre las divisiones de la pared
    # numero de biot a
    a = (alphap * Decimal(60)) / (Decimal(0.015) ** Decimal(2)) # conducti -- calculable
    estabilidad  = (diff * Decimal(3600)) / x # estabilidad  -- calculable
    l  = Decimal(3)  ## altura de la pared
    W = Decimal(0.2) # ancho del canal.
    # area de outlet inlet
    Ao = Decimal(0.01)
    Ai = Decimal(0.01)
    Si = Decimal(0.75)
    Ad = Decimal(1.5) # Ancho del ducto

    # propiedades capa metalica
    cm = Decimal(442)
    km = Decimal(42.3)
    densm = Decimal(7848.57)
    xm = Decimal(0.99)

    # propiedades pared - aire
    ufpa = Decimal(0) #viscocidad cinematica de la pared-aire
    denspa = Decimal(0) ## densidad
    condpa = Decimal(0)
    cppa = Decimal(0) # calor especifico pared aire
    betapa = Decimal(0)
    deltapa = Decimal(0)
    prpa = Decimal(0)
    vfpa = Decimal(0)
    grpa = Decimal(0)
    rapa = Decimal(0)
    nusseltpa = Decimal(0)
    hw = Decimal(0)
    tmpa = Decimal(0) #temp media

    def __getattr__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        self.__dict__[key] = value
