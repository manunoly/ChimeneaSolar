__author__ = 'manuel'
from decimal import *
getcontext().prec = 10
import sys

class TareaCalcularSegundaFase:

    def __init__(self, To, Tg, cola, incremento, chimenea):
        self.__To = To
        self.__Tg = Tg
        self.__cola = cola
        self.__incremento = incremento
        self.__chimenea = chimenea

    def calcularSegundaFase(self):
        Tf = self.__Tg
        menorValor = 100
        if (self.__Tg <= self.__To):
            while Tf <= self.__To:
                a = self.__chimenea.calcular(self.__To, self.__Tg, Tf)
                if abs(a[0]) < menorValor:
                    menorValor = abs(a[0])
                    temperaturas = [0, a[0], self.__To, self.__Tg, Tf, a[0], a[1], a[2], a[3], a[4]]
                Tf = Tf + self.__incremento
        else:
            Tf = self.__To
            while Tf <= self.__Tg:
                a = self.__chimenea.calcular(self.__To, self.__Tg, Tf)
                if abs(a[0]) < menorValor:
                    menorValor = abs(a[0])
                    temperaturas = [0, a[0], self.__To, self.__Tg, Tf, a[0], a[1], a[2], a[3], a[4]]
                Tf = Tf + self.__incremento

        if menorValor < 100.0:
            self.__cola.put(temperaturas)
        # def __del__(self):
        #     print("HIJO {0} - Muere".format(self.__Tg))
