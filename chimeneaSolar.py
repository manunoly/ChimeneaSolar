__author__ = 'manuel'
from decimal import *


class ChimeneaSolar:
    ## Constante
    getcontext().prec = 10
    SteffanBoltzmann = float(0.0000000567)
    #temp pared del extremo inicial, puede ser una constante o toca investigar como hacer su calculo inicial. la T1 va variando con el tiempo.
    #valor inicial
    T1 = float(308)
    #temp pared otro extremo puede ser una constante o toca investigar como hacer su calculo inicial. la T15 va variando con el tiempo. 308 valor inicial luego se calcula
    T15 = float(308.0)
    #valor cuando varia la temperatura, seria en la proxima hora.
    #T15 = ((((k / x)*(T1 - T15[0])) - (hwind * (T15[0] - Ta[0]))))

    def __init__(self, clima, pared, vidrio):
        self.__vidrioP = vidrio
        self.__paredP = pared
        self.__climaP = clima

    #aberturas de ingreso y salida del aire
    ancho = float(0)
    largo = float(0)

    def calcular(self,To,Tg,Tf):
        #
        # data = [To + Tg + Tf, 1, 2, 3]
        # return data
        # Calculo de Sw calor de radiacion
        sw = self.__vidrioP.T * self.__paredP.alphap * self.__climaP.radicacion
        # Calcular Sg calor de radiacion en el vidrio
        # la radiacion va variando a cada hora segun condiciones climaticas
        sg = self.__vidrioP.alphav * self.__climaP.radicacion
        # hwind coeficiente de transferencia de calor por conveccion del viento externo       #la Tg Tf To temp deben ir variando dentro de las siguientes formulas
        #con el valor inicial de las var anteriores calcular
        # hrwg  coeficiente de radiacion entre la pared y el vidrio
        # hrgs  coeficiente de radiacion entre el vidrio y el ambiente
        # hrws  coeficiente de radiacion entre la pared y el ambiente
        hrwg =  round(self.SteffanBoltzmann * (((Tg ** float(2) + To ** float(2))* (Tg + To))/((float(1)/self.__vidrioP.ev)+(float(1)/self.__paredP.ep)- float(1))),5)
        hrgs = round(self.SteffanBoltzmann * self.__vidrioP.ev) * (Tg + self.__climaP.Ts) * (Tg ** float(2) + self.__climaP.Ts ** float(2))
        #hrws = (self.SteffanBoltzmann * self.__paredP.ep) * (T15 + self.__climaP.Ts) * (T15 ** 2 + self.__climaP.Ts ** 2)

        #vamos a calcular las propiedades del vidrio - aire
        tmva = (Tg + Tf)/float(2)
        ufva = (float(1.846) + (float(0.00472) * (tmva - float(300)))) * float(10) ** float(-5)
        densva = (float(1.1614) - (float(0.00353) * (tmva - float(300))))
        condva = (float(0.0263) + (float(0.000074) * (tmva - float(300))))
        cpva = (float(1.007) + (float(0.00004) * (tmva - float(300)))) * float(10) ** float(3)
        betava = float(1)/tmva

        deltava = float(abs(Tg - Tf))
        prva = (ufva * cpva) / condva
        vfva = ufva / densva
        grva = (float(9.8) * betava * deltava * (self.__paredP.l ** float(3))) / (vfva ** float(2))
        rava = prva * grva
        if rava < float(10) ** float(9):
            nusseltva = float(0.68) + (float(0.67) * rava ** (float(1)/float(4))) / (float(1) + (float(0.492) / prva) ** (float(9) / float(16))) ** (float(4) /float(9))
        else:
            nusseltva = (float(0.825) + (float(0.387) * (rava ** (float(1)/float(6)))) / (float(1) + (float(0.492) / prva) **(float(9)/float(16))) **(float(8) / float(27))) ** float(2)

        hg = (nusseltva * condva) / self.__paredP.l

        # vamos a calcular las propiedades de la pared - aire
        tmpa = (Tf + To) / float(2)
        ufpa = (float(1.846) + (float(0.00472) * (tmpa - float(300)))) * float(10) ** float(-5)
        denspa = (float(1.1614) - (float(0.00353) * (tmpa - float(300))))
        condpa = (float(0.0263) + (float(0.000074) * (tmpa - float(300))))
        cppa = (float(1.007) + (float(0.00004) * (tmpa - float(300)))) * float(10) ** float(3)
        betapa = float(1)/tmpa
        deltapa = float(abs(To - Tf))
        prpa = (ufpa * cppa) / condpa
        vfpa = ufpa / denspa
        grpa = (float(9.8) * betapa * deltapa * (self.__paredP.l ** float(3))) / (vfpa ** float(2))
        rapa = prpa * grpa
        if rapa < float(10) ** float(9):
            nusseltpa = float(0.68) + (float(0.67) * rapa ** (float(1)/float(4))) / (float(1) + (float(0.492) / prpa) ** (float(9) / float(16))) ** (float(4) / float(9))
        else:
            nusseltpa = (float(0.825) + (float(0.387) * (rapa ** (float(1)/float(6)))) / (float(1) + (float(0.492) / prpa) **(float(9)/float(16))) **(float(8) / float(27))) ** float(2)

        hw = (nusseltpa * condpa) / self.__paredP.l

        #hay q variar To, Tg, Tf para que aproximado de 0
        # variar To, comenzar con temp ambiental y variar 50 mas
        # variar Tg comenzar con temp ambiental  y variar 2 mas
        # variar Tf comenzar con Tg y terminar con To pq siempre tiene q estar en este rango.

        aproximado = float(sg + (hg * (Tf - Tg)) + (hrwg * (To - Tg)) - (self.__climaP.hwind * (Tg - self.__climaP.Ta)) - (hrgs * (Tg - self.__climaP.Ts)))
        data = [round(aproximado, 5), hw, sw, hrwg]
        return data
        # return aproximado
    #
    # hw    coeficiente de conveccion de la pared y el aire
    # hg    coeficiente de conveccion del vidrio y el aire
        # para calcular hg hay q calcular primero la Tm temperetura media y luego las propiedades del aire y luego se calcula el Ra(Raile)
        # Si Ra tiene un valor se utiliza formula X si otro valor se utiliza formula y
        # se calcula Nu (nusel)
        #con este Nu es que se calcula finalmente hg y hw


    #luego utilizar la ecuacion de Tg (valance de energia en el vidrio) que es la que se debe igualar variando las temperaturas,  debo quedarme con la temperatura que logre igualar

    #toca calcular por cada hora del dia, para la proxima hora se utiliza To y solo se varian Tf y Tg lo cual daria en calcular en nuevos valores para Tf y Tg y seguir para la proxima hora

    #definir los puntos de division de la pared, Delta x no puede ser mayor que 0.25, si deseo lo puedo dividir en menos puntos de lo que en principio puede darme la cantidad de ranuras siempre que el espacio no sea mayor de 0.25



