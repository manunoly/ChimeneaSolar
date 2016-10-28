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
import time, os

getcontext().prec = 10

class Procesos:

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
        self.incremento = Decimal(0.1)

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
            rangoTg = Decimal(2)
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
        limite = i + 15

        while (limite >= i):
            piscina.append(Process(target=TareaCalcular(limite, cola, incremento, rangoSuperiorTg, rangoInferiorTg, self.clima, self.pared, self.vidrio, variacionProceso, self.chimenea).primeraVuelta))
            # print("proceso " + str(i))
            piscina[piscina.__len__() - 1].start()
            limite = limite - variacionProceso
            cant = cant + 1
        print("Creados " + str(cant) + " procesos")
        return piscina

    def calcularFlujoMasico(self,datosM, orderFM = False):
        #vueltas, menorValor, To, Tg , Tf,round(aproximado, 5), hw, sw, hrwg, hg
        # print("Calculando Flujo Masico, probando " + str(datosM.__len__()))
        valores = []
        for datos in datosM:
            hw = Decimal(datos[6])
            To = Decimal(datos[2])
            Tf = Decimal(datos[4])
            hg = Decimal(datos[9])
            Tg = Decimal(datos[3])
            valorRotacion = 0
            flujoMasicoO = 10
            valorVariar = Decimal(10)
            flujoMasicoT = 100
            while valorVariar < 70:
                flujoMasico = (hw * (To - Tf)) - (hg * (Tf - Tg)) - (valorVariar * (Tf - Decimal(self.clima.Ta)))
                if abs(flujoMasico) < flujoMasicoT:
                    flujoMasicoT = abs(flujoMasico)
                    flujoMasicoO = flujoMasico
                    valorRotacion = valorVariar
                valorVariar = valorVariar + Decimal(0.5)
            if(flujoMasicoO != 10):
                valores.append([flujoMasicoO, valorRotacion, datos])
        # valoresM = sorted(valores, key = lambda x: abs(x[0]))

        if valores.__len__() >= 1:
            for mejores in valores:
                mejorFlujoMasico = mejores[1]
                Tf = Decimal(mejores[2][4])
                Cf = (Decimal(1.007) + Decimal(0.00004) * (Decimal(Tf) - Decimal(300))) * Decimal(10) ** Decimal(3)
                flujoMasicoFinal = (Decimal(mejorFlujoMasico) * Decimal(0.75) * Decimal(self.pared.W) * Decimal(self.pared.l)) / Decimal(Cf)
                mejores.append(flujoMasicoFinal)
            if (orderFM):
                valoresFM = sorted(valores, key = lambda x: x[x.__len__() -1], reverse=True)
            else:
                valoresFM = valores
            return valoresFM
        return None

    def esperar(self,piscina):
        timeEnd = 0
        while piscina:
            time.sleep(5)
            self.terminarProcesos(piscina)
            timeEnd = timeEnd + 5
            if timeEnd > 600:
                print("Tiempo límite exedido de 600 segundos, Fuerzo el cierre!!")
                self.terminarProcesos(piscina)
                idProceso = os.getpid()
                self.matarProcesos(idProceso)
                break

    def getMejores(self, cola, comparar = None, cantidad = 5):
        if comparar is None:
            comparar = 1
        menores = []
        while not cola.empty():
            valor = cola.get()
            # if abs(valor[1]) < comparar:
            menores.append(valor)
        menores = sorted(menores, key = lambda x: abs(x[1]))
        return menores[:cantidad]

    def getClimaObjeto(self):
            return self.clima

    def calcularSegundaFase(self, To, Tg, Tf, hw, sw, hrwg, vuelta):
        tiempoActual = 3600
        hrws = (Decimal(0.0000000567) * self.pared.ep) * (self.clima.T15 + self.clima.Ts) * (self.clima.T15 ** 2 + self.clima.Ts ** 2)
        # de donde sale la variable kp
        To1 = ((sw -(hw *(To - Tf)) - (hrwg * (To - Tg)) - ((self.pared.kp / self.pared.x) * (To - self.clima.T1))) * ((2 * 3600) / (self.pared.cpp * self.pared.densp * self.pared.x))) + To
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