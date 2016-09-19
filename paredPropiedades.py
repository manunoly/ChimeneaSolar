__author__ = 'manuel'
from decimal import *
getcontext().prec = 6

class ParedPropiedades:

    ## variables de la pared
    k = float(1.63)  # conductividad termica
    cpp = float(1090)    # calor especifico pared especifico
    densp = float(2400)
    alphap = float(0.82) ## absortividad
    ep  = float(0.95)  ## emisividad
    diff  = float(6.23) * float(10) ** float(-7)  ## difusividad terminca  -- calculable
    x = float(0.12) # distancia entre las divisiones de la pared
    # numero de biot a
    a = (alphap * float(60)) / (float(0.015) ** float(2)) # conducti -- calculable
    estabilidad  = (diff * float(3600)) / x # estabilidad  -- calculable
    l  = float(2)  ## altura de la pared


    # propiedades pared - aire
    ufpa = float(0) #viscocidad cinematica de la pared-aire
    denspa = float(0) ## densidad
    condpa = float(0)
    cppa = float(0) # calor especifico pared aire
    betapa = float(0)
    deltapa = float(0)
    prpa = float(0)
    vfpa = float(0)
    grpa = float(0)
    rapa = float(0)
    nusseltpa = float(0)
    hw = float(0)
    tmpa = float(0) #temp media

    def __getattr__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        self.__dict__[key] = value
