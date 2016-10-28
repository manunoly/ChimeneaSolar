__author__ = 'manuel'
from decimal import *
getcontext().prec = 10

class ClimaPropiedades:

    #variables del clima

    Ta = Decimal(295) #Temp Ambiental
    velocidadViento = Decimal(1) #V
    radicacion = Decimal(0) #rad vertical -- ver con geovanna como se calcula la radiacion vertical, se debe ir variando segun las horas del dia.
    velV=[1,1.25,1,0.5,0.25,1.9,2,1.9,0.5,1.9,2,2.5,4.5,5.5,6.5,6,5,4,2.5,1.5,1.5,1,1,0.5,1.5,2.5,2,2,2.5,3,2,1,1,4,3,2,3.5,6.5,8,6.5,5.5,3.5,3.5,1,0.5,1.5,1.5,2.5]
    rad=[0,0,0,0,0,0,0,30,50,90,130,150,240,345,420,440,230,110,70,30,0,0,0,0,0,0,0,0,0,0,0,30,70,110,150,260,380,260,150,110,70,30,0,0,0,0,0,0]
    tamb=[295,294.5,294.5,295,295,294,295,297,300,305,307,309,309,309,310,311,310,307,306,301,299,299,299,299,298,298,298,298,297,298,303,306,309,310,311,312,312,311,311,310,308,306,303,301,300,300,299,299]
    T1 = Decimal(306)
    T15 = Decimal(304)
    tiempoActual = Decimal(0)
    # Temperatura del cielo
    Ts = Decimal(0.0552) * (Ta ** Decimal(1.5))

    # la velocidad del viento va variando a cada hora segun condiciones climaticas
    hwind = Decimal(5.7) + (Decimal(3.8) * velocidadViento)

    def __getattr__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def actualizarDatosHora(self, hora = None):
        if hora is None:
            hora = 0
        self.Ta = Decimal(self.tamb[hora])
        self.radicacion = Decimal(self.rad[hora])
        self.velocidadViento = Decimal(self.velV[hora])
        self.Ts = Decimal(0.0552) * (self.Ta ** Decimal(1.5))
        self.hwind = Decimal(5.7) + (Decimal(3.8) * self.velocidadViento)