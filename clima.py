__author__ = 'manuel'
from decimal import *

class ClimaPropiedades:
    getcontext().prec = 10
    #variables del clima
    # rh = []
    # velV = []
    # rad = []
    # tamb = []
    # humedadRelativa = 0
    Ta = Decimal(295) #Temp Ambiental
    velocidadViento = Decimal(1) #V
    radicacion = Decimal(0) #rad vertical -- ver con geovanna como se calcula la radiacion vertical, se debe ir variando segun las horas del dia.
    # velV=[1,1.25,1,0.5,0.25,1.9,2,1.9,0.5,1.9,2,2.5,4.5,5.5,6.5,6,5,4,2.5,1.5,1.5,1,1,0.5,1.5,2.5,2,2,2.5,3,2,1,1,4,3,2,3.5,6.5,8,6.5,5.5,3.5,3.5,1,0.5,1.5,1.5,2.5]
    # rad=[0,0,0,0,0,0,0,30,50,90,130,150,240,345,420,440,230,110,70,30,0,0,0,0,0,0,0,0,0,0,0,30,70,120,170,280,400,280,150,110,70,30,0,0,0,0,0,0]
    # tamb=[295,294.5,294.5,295,295,294,295,297,300,305,307,309,309,309,310,311,310,307,306,301,299,299,299,299,298,298,298,298,297,298,303,307,310,310,311,312,313,312,311,310,308,306,303,301,300,300,299,299]
    # tamb = list(map(Decimal,['295.4','295','294.8','294.5','294.9','294','295.5','299','303','306','308','308.5','309','309','311','311','311','309','306.5','305','301','299','299','298','297.5','296.8','298.1','298','298','297','299','303','306','308.7','309','310','311','312','312','311','310.5','310','308','306','302','301','300.5','299.5','299.5']))
    # rad = list(map(Decimal,['0','0','0','0','0','0','30','100','140','200','290','410','435','440','400','320','200','110','60','15','0','0','0','0','0','0','0','0','0','0','40','80','110','150','290','380','430','420','380','290','200','90','50','10','0','0','0','0','0']))
    # velV = list(map(Decimal,['1','1.5','0.9','0.5','0.3','1.2','1.1','1.4','0.6','2','1.9','4.1','5','5.7','6.4','6.5','6','5','3.7','2.5','1.5','1.5','1','1','1','1.5','2.5','2','2','2.5','3','1','1','1.5','4','3','2','4','8','7','5.5','5.5','3.7','3','1','0.5','1.2','1.5','2.3']))
    tamb = list(map(Decimal,['298','298','300','299','299','298','298','298','297','297','299','301','303','304','305','306','300','299','298','298','298','298','298','298','298']))
    rad= list(map(Decimal,['0','0','0','0','0','0','0','0','0','25','75','72','75','135','135','135','75','60','50','0','0','0','0','0','0']))
    velV= list(map(Decimal,['0.65','0.7','0.9','1.15','1.25','1.2','1.15','0.9','0.95','0.95','1','0.95','1.1','1.6','1.8','1.5','1.35','0.9','0.8','0.6','0.6','0','0','0','0']))
    T1 = Decimal(310)
    T15 = Decimal(303)
    tiempoActual = Decimal(0)
    # Temperatura del cielo
    Ts = Decimal(0.0552) * (Ta ** Decimal(1.5))
    cd = Decimal(0.57) # coeficiente de descarga
    gravedad = Decimal(9.8)

    # la velocidad del viento va variando a cada hora segun condiciones climaticas
    hwind = Decimal(5.7) + (Decimal(3.8) * velocidadViento)

    def __init__(self, fichero = '/home/manuesl/PycharmProjects/chimeneaSolar/epw.epw', posTamb = 6, posRad = 13, posVelV = 21, posRH = 8, inicio = 32, fin = 56, lineasUtilizar= None, delimitador=','):
        try:
            data = open(fichero,'r')
            texto = enumerate(data)
            for i, linea in texto:
                if i >= inicio:
                    datosP = linea.split(delimitador)
                    self.tamb.append(Decimal(datosP[posTamb]) + 273)
                    self.velV.append(Decimal(datosP[posVelV]))
                    self.rad.append(Decimal(datosP[posRad]))
                    self.rh.append(Decimal(datosP[posRH]))
                if i > fin:
                    break
        except Exception:
            pass

        self.actualizarDatosHora()
        # print(self.rad.__len__())
        # print(self.tamb.__len__())
        # print(self.velV.__len__())
        # exit()
    def __getattr__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def actualizarDatosHora(self, hora = None):
        if hora is None:
            hora = 0
        self.Ta = self.tamb[hora]
        # self.humedadRelativa = Decimal(self.rh[hora])
        self.radicacion = self.rad[hora]
        self.velocidadViento = self.velV[hora]
        self.Ts = Decimal(0.0552) * (self.Ta ** Decimal(1.5))
        self.hwind = Decimal(5.7) + (Decimal(3.8) * self.velocidadViento)
