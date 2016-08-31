__author__ = 'manuel'

class ParedPropiedades:

    ## variables de la pared
    k = 1.63  # conductividad termica
    cpp = 1090.0    # calor especifico pared especifico
    densp = 2400.0
    alphap = .82 ## absortividad
    ep  = .95  ## emisividad
    diff  = 6.23 * 10 ** -7  ## difusividad terminca  -- calculable
    x = .12 # distancia entre las divisiones de la pared
    # numero de biot a
    a = (alphap * 60) / (0.015 ** 2) # conducti -- calculable
    estabilidad  = (diff * 3600) / x # estabilidad  -- calculable
    l  = 2.0  ## altura de la pared


    # propiedades pared - aire
    ufpa = .0 #viscocidad cinematica de la pared-aire
    denspa = .0 ## densidad
    condpa =.0
    cppa = .0 # calor especifico pared aire
    betapa =.0
    deltapa =.0
    prpa =.0
    vfpa = .0
    grpa = .0
    rapa = .0
    nusseltpa = .0
    hw = .0
    tmpa = .0 #temp media

    def __getattr__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        self.__dict__[key] = value
