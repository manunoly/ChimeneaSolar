__author__ = 'manuel'
from decimal import *


class ParedPropiedades:
    getcontext().prec = 10
    ## variables de la pared
    kp = Decimal(1.4)  # conductividad termica
    cpp = Decimal(837)    # calor especifico pared especifico
    densp = Decimal(2220)
    alphap = Decimal(0.82) ## absortividad
    ep  = Decimal(0.95)  ## emisividad
    diff  = Decimal(7.53) * Decimal(10) ** Decimal(-7)  ## difusividad terminca  -- calculable
    x = Decimal(0.15) # distancia entre las divisiones de la pared
    # numero de biot a
    a = (alphap * Decimal(60)) / (Decimal(0.015) ** Decimal(2)) # conducti -- calculable
    estabilidad  = (diff * Decimal(3600)) / x # estabilidad  -- calculable
    l  = Decimal(3)  ## altura de la pared
    W = Decimal(0.2)
    # area de outlet inlet
    Ao = Decimal(0.19)
    Ai = Decimal(0.039)
    Si = Decimal(0.75)
    Ad = Decimal(1) # Ancho del ducto

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
