__author__ = 'manuel'
from decimal import *


class ChimeneaSolar:
    ## Constante
    getcontext().prec = 10

    def __init__(self, clima, pared, vidrio):
        self.__vidrioP = vidrio
        self.__paredP = pared
        self.__climaP = clima

    #aberturas de ingreso y salida del aire
    ancho = Decimal(0)
    largo = Decimal(0)

    def calcular(self,To,Tg,Tf):
        SteffanBoltzmann = Decimal(0.0000000567)
        sw = 0
        hw = 0
        hrwg = 0
        #temp pared del extremo inicial, puede ser una constante o toca investigar como hacer su calculo inicial. la T1 va variando con el tiempo.
        #valor inicial
        T1 = Decimal(308)
        #temp pared otro extremo puede ser una constante o toca investigar como hacer su calculo inicial. la T15 va variando con el tiempo. 308 valor inicial luego se calcula
        T15 = Decimal(308.0)
        #valor cuando varia la temperatura, seria en la proxima hora.
        #T15 = ((((k / x)*(T1 - T15[0])) - (hwind * (T15[0] - Ta[0]))))
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
        hrwg =  round(SteffanBoltzmann * (((Tg ** Decimal(2) + To ** Decimal(2))* (Tg + To))/((Decimal(1)/self.__vidrioP.ev)+(Decimal(1)/self.__paredP.ep)- Decimal(1))),5)
        hrgs = round((SteffanBoltzmann * self.__vidrioP.ev) * (Tg + self.__climaP.Ts) * (Tg ** Decimal(2) + self.__climaP.Ts ** Decimal(2)),5)
        #hrws = (SteffanBoltzmann * self.__paredP.ep) * (T15 + self.__climaP.Ts) * (T15 ** 2 + self.__climaP.Ts ** 2)

        #vamos a calcular las propiedades del vidrio - aire
        tmva = (Tg + Tf)/Decimal(2)
        ufva = (Decimal(1.846) + (Decimal(0.00472) * (tmva - Decimal(300)))) * Decimal(10) ** Decimal(-5)
        densva = (Decimal(1.1614) - (Decimal(0.00353) * (tmva - Decimal(300))))
        condva = (Decimal(0.0263) + (Decimal(0.000074) * (tmva - Decimal(300))))
        cpva = (Decimal(1.007) + (Decimal(0.00004) * (tmva - Decimal(300)))) * Decimal(10) ** Decimal(3)
        betava = Decimal(1)/tmva

        deltava = Decimal(abs(Tg - Tf))
        prva = (ufva * cpva) / condva
        vfva = ufva / densva
        grva = (Decimal(9.8) * betava * deltava * (self.__paredP.l ** Decimal(3))) / (vfva ** Decimal(2))
        rava = prva * grva
        if rava < Decimal(10) ** Decimal(9):
            nusseltva = Decimal(0.68) + (Decimal(0.67) * rava ** (Decimal(1)/Decimal(4))) / (Decimal(1) + (Decimal(0.492) / prva) ** (Decimal(9) / Decimal(16))) ** (Decimal(4) /Decimal(9))
        else:
            nusseltva = (Decimal(0.825) + (Decimal(0.387) * (rava ** (Decimal(1)/Decimal(6)))) / (Decimal(1) + (Decimal(0.492) / prva) **(Decimal(9)/Decimal(16))) **(Decimal(8) / Decimal(27))) ** Decimal(2)

        hg = (nusseltva * condva) / self.__paredP.l

        # vamos a calcular las propiedades de la pared - aire
        tmpa = (Tf + To) / Decimal(2)
        ufpa = (Decimal(1.846) + (Decimal(0.00472) * (tmpa - Decimal(300)))) * Decimal(10) ** Decimal(-5)
        denspa = (Decimal(1.1614) - (Decimal(0.00353) * (tmpa - Decimal(300))))
        condpa = (Decimal(0.0263) + (Decimal(0.000074) * (tmpa - Decimal(300))))
        cppa = (Decimal(1.007) + (Decimal(0.00004) * (tmpa - Decimal(300)))) * Decimal(10) ** Decimal(3)
        betapa = Decimal(1)/tmpa
        deltapa = Decimal(abs(To - Tf))
        prpa = (ufpa * cppa) / condpa
        vfpa = ufpa / denspa
        grpa = (Decimal(9.8) * betapa * deltapa * (self.__paredP.l ** Decimal(3))) / (vfpa ** Decimal(2))
        rapa = prpa * grpa
        if rapa < Decimal(10) ** Decimal(9):
            nusseltpa = Decimal(0.68) + (Decimal(0.67) * rapa ** (Decimal(1)/Decimal(4))) / (Decimal(1) + (Decimal(0.492) / prpa) ** (Decimal(9) / Decimal(16))) ** (Decimal(4) / Decimal(9))
        else:
            nusseltpa = (Decimal(0.825) + (Decimal(0.387) * (rapa ** (Decimal(1)/Decimal(6)))) / (Decimal(1) + (Decimal(0.492) / prpa) **(Decimal(9)/Decimal(16))) **(Decimal(8) / Decimal(27))) ** Decimal(2)

        hw = (nusseltpa * condpa) / self.__paredP.l

        #hay q variar To, Tg, Tf para que aproximado de 0
        # variar To, comenzar con temp ambiental y variar 50 mas
        # variar Tg comenzar con temp ambiental  y variar 2 mas
        # variar Tf comenzar con Tg y terminar con To pq siempre tiene q estar en este rango.

        aproximado = Decimal(sg + (hg * (Tf - Tg)) + (hrwg * (To - Tg)) - (self.__climaP.hwind * (Tg - self.__climaP.Ta)) - (hrgs * (Tg - self.__climaP.Ts)))
        data = [round(aproximado, 5), hw, sw, hrwg, denspa]
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



