__author__ = 'manuel'


class ChimeneaSolar:
    ## Constante
    SteffanBoltzmann = 0.0000000567
    #temp pared del extremo inicial, puede ser una constante o toca investigar como hacer su calculo inicial. la T1 va variando con el tiempo.
    #valor inicial
    T1 = 308.0
    #temp pared otro extremo puede ser una constante o toca investigar como hacer su calculo inicial. la T15 va variando con el tiempo. 308 valor inicial luego se calcula
    T15 = 308.0
    #valor cuando varia la temperatura, seria en la proxima hora.
    #T15 = ((((k / x)*(T1 - T15[0])) - (hwind * (T15[0] - Ta[0]))))

    def __init__(self, clima, pared, vidrio):

        self.__vidrioP = vidrio
        self.__paredP = pared
        self.__climaP = clima

    #aberturas de ingreso y salida del aire
    ancho = .0
    largo = .0

    def calcular(self,To,Tg,Tf):


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
        hrwg =  self.SteffanBoltzmann * (((Tg ** 2 + To ** 2)* (Tg + To))/((1/self.__vidrioP.ev)+(1/self.__paredP.ep)-1))
        hrgs = (self.SteffanBoltzmann * self.__vidrioP.ev) * (Tg + self.__climaP.Ts) * (Tg ** 2 + self.__climaP.Ts ** 2)
        #hrws = (self.SteffanBoltzmann * self.__paredP.ep) * (T15 + self.__climaP.Ts) * (T15 ** 2 + self.__climaP.Ts ** 2)

        #vamos a calcular las propiedades del vidrio - aire
        tmva = (Tg + Tf)/2
        ufva = (1.846 + (0.00472 * (tmva - 300))) * 10 ** -5
        densva = (1.1614 - (0.00353 * (tmva - 300)))
        condva = (0.0263 + (0.000074 * (tmva - 300)))
        cpva = (1.007 + (0.00004 * (tmva -300))) * 10 ** 3
        betava = 1.0/tmva

        deltava = abs(Tg - Tf)
        prva = (ufva * cpva) / condva
        vfva = ufva / densva
        grva = (9.8 * betava * deltava * (self.__paredP.l ** 3)) / (vfva ** 2)
        rava = prva * grva
        if rava < 10 ** 9:
            nusseltva = 0.68 + (0.67 * rava ** (1.0/4)) / (1 + (0.492 / prva) ** (9.0 / 16)) ** (4.0 /9)
        else:
            nusseltva = (0.825 + (0.387 * (rava ** (1/6))) / (1 + (0.492 / prva) **(9.0/16)) **(8.0 /27)) ** 2

        hg = (nusseltva * condva) / self.__paredP.l

        # vamos a calcular las propiedades de la pared - aire
        tmpa = (Tf + To) / 2
        ufpa = (1.846 + (0.00472 * (tmpa - 300))) * 10 ** -5
        denspa = (1.1614 - (0.00353 * (tmpa - 300)))
        condpa = (0.0263 + (0.000074 * (tmpa - 300)))
        cppa = (1.007 + (0.00004 * (tmpa -300))) * 10 ** 3
        betapa = 1.0/tmpa
        deltapa = abs(To - Tf)
        prpa = (ufpa * cppa) / condpa
        vfpa = ufpa / denspa
        grpa = (9.8 * betapa * deltapa * (self.__paredP.l ** 3)) / (vfpa ** 2)
        rapa = prpa * grpa
        if rapa < 10 ** 9:
            nusseltpa = 0.68 + (0.67 * rapa ** (1.0/4)) / (1 + (0.492 / prpa) ** (9.0 / 16)) ** (4.0 /9)
        else:
            nusseltpa = (0.825 + (0.387 * (rapa ** (1/6))) / (1 + (0.492 / prpa) **(9.0/16)) **(8.0 /27)) ** 2

        hw = (nusseltpa * condpa) / self.__paredP.l

        #hay q variar To, Tg, Tf para que aproximado de 0
        # variar To, comenzar con temp ambiental y variar 50 mas
        # variar Tg comenzar con temp ambiental  y variar 2 mas
        # variar Tf comenzar con Tg y terminar con To pq siempre tiene q estar en este rango.

        aproximado = sg + (hg * (Tf - Tg)) + (hrwg * (To - Tg)) - (self.__climaP.hwind * (Tg - self.__climaP.Ta)) - (hrgs * (Tg - self.__climaP.Ts))
        data = [aproximado, hw, sw, hrwg]
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



