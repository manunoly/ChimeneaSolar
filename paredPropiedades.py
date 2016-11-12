__author__ = 'manuel'
from decimal import *
getcontext().prec = 10

class ParedPropiedades:

    ## variables de la pared
    kp = Decimal(1.63)  # conductividad termica
    cpp = Decimal(1090)    # calor especifico pared especifico
    densp = Decimal(2400)
    alphap = Decimal(0.82) ## absortividad
    ep  = Decimal(0.95)  ## emisividad
    diff  = Decimal(6.23) * Decimal(10) ** Decimal(-7)  ## difusividad terminca  -- calculable
    x = Decimal(0.12) # distancia entre las divisiones de la pared
    # numero de biot a
    a = (alphap * Decimal(60)) / (Decimal(0.015) ** Decimal(2)) # conducti -- calculable
    estabilidad  = (diff * Decimal(3600)) / x # estabilidad  -- calculable
    l  = Decimal(2)  ## altura de la pared
    W = Decimal(0.145)
    # area de outlet inlet
    Ao = Decimal(0.025)
    Ai = Decimal(0.025)

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
