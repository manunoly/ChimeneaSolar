__author__ = 'manuel'
from decimal import *
getcontext().prec = 6

class ClimaPropiedades:

    #variables del clima

    Ta = Decimal(295) #Temp Ambiental
    velocidadViento = Decimal(1) #V
    radicacion = Decimal(0) #rad vertical -- ver con geovanna como se calcula la radiacion vertical, se debe ir variando segun las horas del dia.

    T1 = Decimal(0)
    T15 = Decimal(0)

    # Temperatura del cielo
    Ts = Decimal(0.0552) * (Ta ** Decimal(1.5))

    # la velocidad del viento va variando a cada hora segun condiciones climaticas
    hwind = Decimal(5.7) + (Decimal(3.8) * velocidadViento)

    def __getattr__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        self.__dict__[key] = value