__author__ = 'manuel'
from decimal import *
getcontext().prec = 6

class ClimaPropiedades:

    #variables del clima

    Ta = float(294) #Temp Ambiental
    velocidadViento = float(1) #V
    radicacion = float(0) #rad vertical -- ver con geovanna como se calcula la radiacion vertical, se debe ir variando segun las horas del dia.

    T1 = float(0)
    T15 = float(0)

    # Temperatura del cielo
    Ts = float(0.0552) * (Ta ** float(1.5))

    # la velocidad del viento va variando a cada hora segun condiciones climaticas
    hwind = float(5.7) + (float(3.8) * velocidadViento)

    def __getattr__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        self.__dict__[key] = value