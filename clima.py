__author__ = 'manuel'


class ClimaPropiedades:

    #variables del clima

    Ta = 295.0 #Temp Ambiental
    velocidadViento = 1.0 #V
    radicacion = .0 #rad vertical -- ver con geovanna como se calcula la radiacion vertical, se debe ir variando segun las horas del dia.

    T1 = .0
    T15 = .0

    # Temperatura del cielo
    Ts = 0.0552 * (Ta ** 1.5)

    # la velocidad del viento va variando a cada hora segun condiciones climaticas
    hwind = 5.7 + (3.8 * velocidadViento)

    def __getattr__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        self.__dict__[key] = value