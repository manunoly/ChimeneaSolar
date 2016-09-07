__author__ = 'manuel'
from chimeneaSolar import ChimeneaSolar
from decimal import *

class TareaCalcular:

    def __init__(self, cid, cola, fijoTo, incremento, rangoSuperiorTg, clima, pared, vidrio, variacionProceso):
        self.__cid=cid
        self.__cola = cola
        self.__fijoTo = fijoTo
        self.__incremento = incremento
        self.__rangoSuperiorTg = rangoSuperiorTg
        self.__clima = clima
        self.__pared = pared
        self.__vidrio = vidrio
        self.variacionProceso = variacionProceso
        # print("HIJO {0} - Nace".format(self.__cid))

    # def __del__(self):
    #     print("HIJO {0} - Muere".format(self.__cid))

    def convergen(self, convergeB, temp):
        self.__cola.put([convergeB, temp[0], temp[1], temp[2], temp[3], temp[4]])

    def run(self):
        getcontext().prec = 6
        menorValor = 100.0
        chimenea = ChimeneaSolar(self.__clima, self.__pared, self.__vidrio)
        temperaturas = []

        if not self.__fijoTo:
            vueltas = 0
            vueltasTo = 0
            vueltasTg = 0
            To = self.__cid
            rangoInferiorTo = To - self.variacionProceso

            while To > rangoInferiorTo:
                # print("To " + str(To))
                # vueltasTo = vueltasTo + 1

                Tg = self.__clima.Ta
                while Tg <= self.__rangoSuperiorTg:
                    Tf = Tg
                    # vueltasTg = vueltasTg + 1
                    # print("__tg " + str(Tg))
                    while Tf <= To:
                        # print("_____tf " + str(Tf))
                        vueltas = vueltas + 1
                        a = chimenea.calcular(To, Tg, Tf)
                        if abs(a[0]) < menorValor:
                            menorValor = a[0]
                            temperaturas = [menorValor, To, Tg , Tf, a]
                        Tf = Tf + self.__incremento
                    Tg = Tg + self.__incremento
                To = To - self.__incremento
            # print(str(self.__cid) + " Rango Inferior " + str(rangoInferiorTo) +" Vueltas  " + str(vueltas) + " Valores Finale To " + str(vueltasTo) + " Tg " + str(vueltasTg) + " Tf " + str(vueltas))

            if menorValor != 100.0:
                self.__cola.put([vueltas, temperaturas[0], temperaturas[1], temperaturas[2], temperaturas[3], temperaturas[4]])
                # self.convergen(False, temperaturas)

