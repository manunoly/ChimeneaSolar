__author__ = 'manuel'
from decimal import *
getcontext().prec = 5

class TareaCalcular:

    def __init__(self, cid, cola, fijoTo, incremento, rangoSuperiorTg, clima, pared, vidrio, variacionProceso, chimenea):
        self.__cid=cid
        self.__cola = cola
        self.__fijoTo = fijoTo
        self.__incremento = incremento
        self.__rangoSuperiorTg = rangoSuperiorTg
        self.__clima = clima
        self.__pared = pared
        self.__vidrio = vidrio
        self.variacionProceso = variacionProceso
        self.__chimenea = chimenea
        # print("HIJO {0} - Nace".format(self.__cid))

    # def __del__(self):
    #     print("HIJO {0} - Muere".format(self.__cid))

    def convergen(self, convergeB, temp):
        self.__cola.put([convergeB, temp[0], temp[1], temp[2], temp[3], temp[4]])

    def run(self):
        getcontext().prec = 10
        menorValor = 100.0
        temperaturas = []

        if not self.__fijoTo:
            vueltas = 0
            vueltasTo = 0
            vueltasTg = 0
            To = self.__cid
            # rangoInferiorTo = To - self.variacionProceso
            total = 0

            # while To > rangoInferiorTo:
            #     # vueltasTo = vueltasTo + 1
            Tg = Decimal(self.__clima.Ta)
            while Tg <= self.__rangoSuperiorTg:
                # print("Tg " + str(Tg))
                Tf = Tg
                # vueltasTg = vueltasTg + Tg
                # vueltas = vueltas + 1
                while Tf <= To:
                    a = self.__chimenea.calcular(Decimal(To), Decimal(Tg), Decimal(Tf))
                    vueltas = vueltas + 1
                    if abs(a[0]) < menorValor:
                        menorValor = abs(a[0])
                        temperaturas = [vueltas, a[0], To, Tg , Tf, a[0], a[1], a[2], a[3], a[4]]
                    Tf = Tf + self.__incremento
                Tg = Tg + self.__incremento
            # To = To - self.__incremento
                    # temperaturas = [menorValor, To, Tg , Tf, a]
            # print("__to " + str(To))
            # print("__sumaTg " + str(vueltasTg))
            # print("__vueltasTg " + str(vueltas))
            # temperaturas = [vueltasTg, To, Tg , Tf, a]

            # print(str(self.__cid) + " Rango Inferior " + str(rangoInferiorTo) +" Vueltas  " + str(vueltas) + " Valores Finale To " + str(vueltasTo) + " Tg " + str(vueltasTg) + " Tf " + str(vueltas))

            if menorValor != 100.0:
                self.__cola.put(temperaturas)
                # self.convergen(False, temperaturas)

