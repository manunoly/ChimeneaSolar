__author__ = 'manuel'
from decimal import *
getcontext().prec = 6

class VidrioPropiedades:


    #propiedades del vidrio
    T = float(0.84) #transmitancia
    absortancia = float(0) # absortancia
    ev = float(0.8) #Emisividad
    alphav = float(0.006)


    #propiedades vidrio - aire

    ufva = float(0) #viscocidad cinematica del vidrio-aire
    densva = float(0) # densidad del vidrio aire
    condva = float(0) # conductividad del vidrio aire
    cpva = float(0)  # calor especifico
    betava = float(0)
    deltava = float(0)
    prva = float(0)
    vfva  = float(0)
    grva = float(0)
    rava = float(0)
    nusseltva  = float(0)
    hg = float(0)
    tmva = float(0) #temp media