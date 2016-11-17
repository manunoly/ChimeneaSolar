__author__ = 'manuel'
from decimal import *


class VidrioPropiedades:

    getcontext().prec = 10
    #propiedades del vidrio
    T = Decimal(0.84) #transmitancia
    absortancia = Decimal(0) # absortancia
    ev = Decimal(0.8) #Emisividad
    alphav = Decimal(0.006)


    #propiedades vidrio - aire

    ufva = Decimal(0) #viscocidad cinematica del vidrio-aire
    densva = Decimal(0) # densidad del vidrio aire
    condva = Decimal(0) # conductividad del vidrio aire
    cpva = Decimal(0)  # calor especifico
    betava = Decimal(0)
    deltava = Decimal(0)
    prva = Decimal(0)
    vfva  = Decimal(0)
    grva = Decimal(0)
    rava = Decimal(0)
    nusseltva  = Decimal(0)
    hg = Decimal(0)
    tmva = Decimal(0) #temp media