__author__ = 'manuel'
#moviendo a parte el manejador de los procesos.

from multiprocessing import Process, Queue
import psutil
from tareaCalcularProcesos import TareaCalcular
from clima import ClimaPropiedades
from paredPropiedades import ParedPropiedades
from vidrioPropiedades import VidrioPropiedades
from chimeneaSolar import ChimeneaSolar
from tareaCalcularProcesos2 import TareaCalcularSegundaFase
from decimal import *
import time, os, math


class Procesos:
    getcontext().prec = 10

    def __init__(self, clima = None, pared = None, vidrio = None, chimenea = None):
        if clima is None:
            clima = ClimaPropiedades()
        self.clima = clima
        if pared is None:
            pared = ParedPropiedades()
        self.pared = pared
        if vidrio is None:
            vidrio = VidrioPropiedades
        self.vidrio = vidrio
        if chimenea is None:
            chimenea = ChimeneaSolar(clima, pared, vidrio)
        self.chimenea = chimenea
        self.incremento = Decimal(0.05)

    def matarProcesos(self, pid):
        parent = psutil.Process(pid)
        children = parent.get_children(recursive=True)

        for child in children:
            print(child)
            child.kill()
        psutil.wait_procs(children, timeout=5)

    def terminarProcesos(self, piscina):
        for proceso in piscina:
            if not proceso.is_alive():
                proceso.join()
                piscina.remove(proceso)
                del(proceso)

    def iniciarProcesos(self, cola, incremento = None, To = None,  Tg = None, rangoTg = None):
        piscina = []
        primeraVuelta = False
        if Tg is None:
            Tg = self.clima.Ta
        if rangoTg is None:
            rangoTg = Decimal(8)
        rangoSuperiorTg = Tg + rangoTg
        rangoInferiorTg = Tg
        resultado = []
        if incremento is None:
            incremento = self.incremento
        if To is None:
            To = rangoSuperiorTg
            primeraVuelta = True
        fijoTo = False
        cant = 0
        variacionProceso = incremento
        i = Tg + Decimal(2)
        limite = i + 12
        while (limite >= i):
            # if (limite > divideProcesos):
            #     rangoInferiorTgTmp = rangoInferiorTg
            #     rangoSuperiorTgTmp = limite
            #     print("divideProcesos " + str(limite))
            #     while rangoInferiorTgTmp <= rangoSuperiorTgTmp:
            #         piscina.append(Process(target=TareaCalcularSegundaFase(limite, rangoInferiorTgTmp, cola, incremento, self.chimenea).calcularSegundaFase))
            #         piscina[piscina.__len__() - 1].start()
            #         rangoInferiorTgTmp = rangoInferiorTgTmp + incremento
            #         cant = cant + 1
            # else:
            #     print("NO__divideProcesos " + str(limite))
            piscina.append(Process(target=TareaCalcular(limite, cola, incremento, rangoSuperiorTg, rangoInferiorTg, self.clima, self.pared, self.vidrio, variacionProceso, self.chimenea).primeraVuelta))
            piscina[piscina.__len__() - 1].start()
            cant = cant + 1
            limite = limite - variacionProceso

        print("Creados " + str(cant) + " procesos")
        return piscina

    def calcularTempFluidoSalida(self,Tf):
        return (Tf - (1-self.pared.Si) * self.clima.Ta) / self.pared.Si

    def calcularVelocidadFluido(self, Tfo):
        tmp = Tfo - self.clima.Ta
        if tmp > 1:
            return Decimal(math.sqrt(self.clima.cd * self.pared.Ao * (2 * (Tfo - self.clima.Ta) / self.clima.Ta) * self.clima.gravedad * self.pared.l)) * (1 / Decimal(math.sqrt(1 + (self.pared.Ai / self.pared.Ao) ** 2))) / (self.pared.W * self.pared.Ad)
        else:
            return 0

    def calcularFlujoMasico(self,datosM, orderFM = False):
        #vueltas, menorValor, To, Tg , Tf,round(aproximado, 5), hw, sw, hrwg, hg
        # print("Calculando Flujo Masico, probando " + str(datosM.__len__()))
        valores = []
        for datos in datosM:
            denspa = Decimal(datos[9])
            Tf = Decimal(datos[4])
            restaTemp = Decimal(Tf - self.clima.Ta)
            if restaTemp > 0:
                flujoMasicoFinal = self.clima.cd * ((denspa * self.pared.Ao) / Decimal(math.sqrt(1 + self.pared.Ao/self.pared.Ai)) * Decimal(math.sqrt((2 * self.clima.gravedad * self.pared.l * restaTemp) / self.clima.Ta)))
            else:
                flujoMasicoFinal = 0
            valores.append([0, 0, datos,flujoMasicoFinal])
        # return valores
        return sorted(valores, key = lambda x: x[x.__len__() - 1], reverse=True)

        #antigua formula de flujo masico no a utilizar
        valores = []
        for datos in datosM:
            hw = Decimal(datos[6])
            To = Decimal(datos[2])
            Tf = Decimal(datos[4])
            hg = Decimal(datos[9])
            Tg = Decimal(datos[3])
            valorRotacion = 0
            flujoMasicoAproximacion = 1000
            valorVariar = Decimal(10)
            flujoMasicoT = 1000
            while valorVariar < 100:
                flujoMasico = (hw * (To - Tf)) - (hg * (Tf - Tg)) - (valorVariar * (Tf - Decimal(self.clima.Ta)))
                if abs(flujoMasico) < flujoMasicoT:
                    flujoMasicoT = abs(flujoMasico)
                    flujoMasicoAproximacion = flujoMasico
                    valorRotacion = valorVariar
                valorVariar = valorVariar + Decimal(1)

            valores.append([flujoMasicoAproximacion, valorRotacion, datos])
        valoresM = sorted(valores, key = lambda x: abs(x[0]))

        if valoresM.__len__() >= 1:
            for mejores in valores:
                mejorFlujoMasico = mejores[1]
                Tf = Decimal(mejores[2][4])
                Cf = (Decimal(1.007) + Decimal(0.00004) * (Decimal(Tf) - Decimal(300))) * Decimal(10) ** Decimal(3)
                flujoMasicoFinal = (Decimal(mejorFlujoMasico) * Decimal(0.75) * Decimal(self.pared.W) * Decimal(self.pared.l)) / Decimal(Cf)
                mejores.append(Decimal(flujoMasicoFinal))
            return valoresM
        return None

    def esperar(self,piscina):
        timeEnd = 0
        while piscina:
            time.sleep(10)
            self.terminarProcesos(piscina)
            timeEnd = timeEnd + 10
            if timeEnd > 1900:
                print("Tiempo límite exedido de 600 segundos, Fuerzo el cierre!!")
                self.terminarProcesos(piscina)
                idProceso = os.getpid()
                self.matarProcesos(idProceso)
                break

    def getMejores(self, cola, comparar = None, cantidad = 10):
        if comparar is None:
            comparar = 1
        menores = []
        while not cola.empty():
            valor = cola.get()
            # if abs(valor[1]) < comparar:
            menores.append(valor)
        menores = sorted(menores, key = lambda x: abs(x[1]))
        return menores[:cantidad]

    def getOptimos(self, valores = None, vuelta = 0, resultados = []):
        #flujoMasicoApromado0, valorRotacion, [vueltas, menorValor, To, Tg , Tf,round(aproximado, 5), hw, sw, hrwg, hg], FM
        # resultados = "Vuelta,Ta,To;Tg;Tf;T1;T15;velocidadViento,radicacion,FM;AproximacionFMa0;variacionFM;Aproximacion0"
        if vuelta > 0:
            # print(self.clima.Ta)
            # print(self.clima.tamb[vuelta])
            # print(resultados[vuelta])
            for valor in valores:
                valor.append(0)
                # if self.clima.rad[vuelta - 1] >= self.clima.rad[vuelta - 1]:
                # #si T0 es mayor a Ta
                # if valor[2][2] > self.clima.Ta:
                #     valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                #si Tg es mayor a Ta
                if valor[2][3] > self.clima.Ta:
                    valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                #si Tf es mayor a Ta
                if valor[2][4] > self.clima.Ta:
                    valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                # condicion si hay radiacion deberia subir Tg y Tf
                if self.clima.radicacion > 0:
                    if resultados[vuelta][3] < valor[2][3]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                    if resultados[vuelta][4] < valor[2][4]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                #
                # condicion para Tg y Tf si baja la temperatura y la radiacion
                if self.clima.tamb[vuelta - 1] > self.clima.Ta and self.clima.rad[vuelta - 1] > self.clima.radicacion:
                    if resultados[vuelta][3] > valor[2][3]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 2
                    if resultados[vuelta][4] > valor[2][4]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 2
                # condicion para Tg y Tf si sube la temperatura y la radiacion
                elif self.clima.tamb[vuelta - 1] < self.clima.Ta and self.clima.rad[vuelta - 1] < self.clima.radicacion:
                    if resultados[vuelta][3] < valor[2][3]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 2
                    if resultados[vuelta][4] < valor[2][4]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 2

                # condicion para Tg y Tf si baja la temperatura
                if self.clima.tamb[vuelta - 1] > self.clima.Ta:
                    if resultados[vuelta][3] > valor[2][3]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                    if resultados[vuelta][4] > valor[2][4]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                # condicion para Tg y Tf si baja la temperatura
                elif self.clima.tamb[vuelta - 1] < self.clima.Ta:
                    if resultados[vuelta][3] < valor[2][3]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                    if resultados[vuelta][4] < valor[2][4]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1

                # condicion para Tg y Tf si baja la radiacion
                if self.clima.rad[vuelta - 1] > self.clima.radicacion:
                    if resultados[vuelta][3] > valor[2][3]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                    if resultados[vuelta][4] > valor[2][4]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                # condicion para Tg y Tf si sube la temperatura y la radiacion
                elif self.clima.rad[vuelta - 1] < self.clima.radicacion:
                    if resultados[vuelta][3] < valor[2][3]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                    if resultados[vuelta][4] < valor[2][4]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1

                # # To
                # if valor[2][2] >  self.clima.Ta - 3 or valor[2][2] <  self.clima.Ta + 15:
                #     valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                #Tg
                if valor[2][3] >  self.clima.Ta - 1 or valor[2][3] <  self.clima.Ta + 3:
                    valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                #Tf
                if valor[2][4] >  self.clima.Ta - 1 or valor[2][4] <  self.clima.Ta + 5:
                    valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                TfDif = abs(valor[2][4] - resultados[vuelta][4])
                if TfDif < 2:
                    valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                #aproximacion a 0 de las temperaturas
                if abs(valor[2][5]) < 2:
                    valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                # puntos para el valor de aproximacion a 0 del FM
                # if valor[0] < 2:
                #     valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                # elif valor[0] < 6:
                #     valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 0.5
                # elif valor[0] < 20:
                #     valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 0.1
                # puntos para el valor de variacion de FM
                # if valor[1] > 40:
                #     valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 2
                # el
                if valor[1] > 10:
                    valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 0.5

                #si aumenta o disminuye la velocidad del viento seria logico variara el Tf
                if(self.clima.velocidadViento > self.clima.velV[vuelta]):
                    if valor[2][4] < resultados[vuelta][4]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1
                elif valor[2][4] > resultados[vuelta][4]:
                        valor[valor.__len__() - 1] = valor[valor.__len__() - 1] + 1

            return sorted(valores, key = lambda x: x[x.__len__() - 1], reverse=True)

    def getClimaObjeto(self):
            return self.clima

    def calcularSegundaFase(self, To, Tg, Tf, hw, sw, hrwg, vuelta):
        tiempoActual = 3600
        hrws = (Decimal(0.0000000567) * self.pared.ep) * (self.clima.T15 + self.clima.Ts) * (self.clima.T15 ** 2 + self.clima.Ts ** 2)
        # de donde sale la variable kp
        # To1 = ((sw -(hw *(To - Tf)) - (hrwg * (To - Tg)) - ((self.pared.kp / self.pared.x) * (To - self.clima.T1))) * ((2 * 3600) / (self.pared.cpp * self.pared.densp * self.pared.x))) + To
        To1 = ((sw -(hw *(To - Tf)) - (hrwg * (To - Tg)) - ((self.pared.km / self.pared.xm) * (To - self.clima.T1))) * ((2 * 3600) / (self.pared.cm * self.pared.densm * self.pared.xm))) + To

        T11 = (((self.pared.diff * tiempoActual) / self.pared.x ** 2 ) * (self.clima.T15 + To - (2 * self.clima.T1))) + self.clima.T1
        T15_1 = ((((self.pared.kp / self.pared.x) * (self.clima.T1 - self.clima.T15)) - (self.clima.hwind * (self.clima.T15 - self.clima.Ta)) - (hrws * (self.clima.T15 - self.clima.Ts))) * ((2 * tiempoActual) / (self.pared.densp * self.pared.cpp * self.pared.x))) + self.clima.T15
        # self.clima.Ta = self.clima.Ta - 1
        self.clima.actualizarDatosHora(vuelta)
        self.clima.T15 = T15_1
        self.clima.T1 = T11
        temp = [To1, T11, T15_1]
        return temp

    def iniciarProcesoSegundaFase(self,cola, To):
        piscina = []
        # i = self.clima.Ta - Decimal(2)
        i = self.clima.Ta - Decimal(10)
        limite = self.clima.Ta + Decimal(10)
        cant = 0
        while (limite >= i):
            piscina.append(Process(target=TareaCalcularSegundaFase(To, limite, cola, self.incremento, self.chimenea).calcularSegundaFase))
            # print("proceso " + str(i))
            piscina[piscina.__len__() - 1].start()
            limite = limite - self.incremento
            cant = cant + 1
        # print("Creados " + str(cant) + " procesos")
        return piscina