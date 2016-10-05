__author__ = 'manuel'
#moviendo a parte el manejador de los procesos.

from multiprocessing import Process, Queue
import psutil
from tareaCalcularProcesos import TareaCalcular
from clima import ClimaPropiedades
from paredPropiedades import ParedPropiedades
from vidrioPropiedades import VidrioPropiedades
from chimeneaSolar import ChimeneaSolar
from decimal import *

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

    def matar_procesos(self, pid):
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

    def iniciarProcesos(self, cola, incremento = None, To = None,  Tg = None, rangoTg = None, rangoTo = None):
        piscina = []
        if cola is None:
            cola = Queue
        if Tg is None:
            Tg = Decimal(self.clima.Ta)
        if rangoTg is None:
            rangoTg = Decimal(2)
        rangoSuperiorTg = Tg + rangoTg
        resultado = []
        if To is None:
            To = rangoSuperiorTg
        if rangoTo is None:
            rangoTo = Decimal(12)
        if incremento is None:
            incremento = Decimal(0.1)
        fijoTo = False
        cant = 0
        variacionProceso = incremento
        i = To
        limite = Decimal(To + rangoTo)

        while (limite >= i):
            piscina.append(Process(target=TareaCalcular(limite, cola, fijoTo, incremento, rangoSuperiorTg, self.clima, self.pared, self.vidrio, variacionProceso, self.chimenea).run))
            # print("proceso " + str(i))
            piscina[piscina.__len__() - 1].start()
            limite = limite - variacionProceso
            cant = cant + 1
        print("Creados " + str(cant) + " procesos")
        return piscina

    def calcularFlujoMasico(self,datosM):
        #vueltas, menorValor, To, Tg , Tf,round(aproximado, 5), hw, sw, hrwg, hg
        print("Calculando Flujo Masico, probando " + str(datosM.__len__()))
        valores = []
        for datos in datosM:
            hw = Decimal(datos[6])
            To = Decimal(datos[2])
            Tf = Decimal(datos[4])
            hg = Decimal(datos[9])
            Tg = Decimal(datos[3])
            mejorFlujoMasico = 0
            flujoMasicoO = 10
            valorVariar = Decimal(1)
            flujoMasicoT = 30
            while valorVariar < 31:
                flujoMasico = (hw * (To - Tf)) - (hg * (Tf - Tg)) - (valorVariar * (Tf - Decimal(self.clima.Ta)))
                if abs(flujoMasico) < flujoMasicoT:
                    flujoMasicoT = abs(flujoMasico)
                    flujoMasicoO = flujoMasico
                    mejorFlujoMasico = valorVariar
                valorVariar = valorVariar + Decimal(0.5)
            if(flujoMasicoO != 10):
                valores.append([flujoMasicoO, mejorFlujoMasico, datos])
        valoresM = sorted(valores, key = lambda x: abs(x[0]))

        if valoresM.__len__() >= 1:
            mejores = valoresM[0]
            Tf = Decimal(mejores[2][4])
            Cf = (Decimal(1.007) + Decimal(0.00004) * (Decimal(Tf) - Decimal(300))) * Decimal(10) ** Decimal(3)
            print(Cf)
            flujoMasicoFinal = (Decimal(mejorFlujoMasico) * Decimal(0.75) * Decimal(self.pared.W) * Decimal(self.pared.l)) / Decimal(Cf)
            mejores.append(flujoMasicoFinal)
            return mejores
        return None

    def calcularSegundaFase(self, To, Tg, Tf):
        tiempoActual = 3600
        # de donde sale la variable kp
        To1 = (self.chimenea.sw -(self.chimenea.hw *(To -Tf) - (self.chimenea.hrwg * (To - Tg)) - ((self.pared.kp / self.pared.x) * (To - self.clima.T1))) * ((2 * 3600) / (self.pared.cpp * self.pared.densp * self.pared.x))) + To
        T11 = (((self.pared.diff * tiempoActual) / self.pared.x ** 2 ) * (self.clima.T15 + To - (2 * self.clima.T1))) + self.clima.T1
        T15_1 = ((((self.pared.k / self.pared.x) * (self.clima.T1 - self.clima.T15)) - (self.clima.hwind * (self.clima.T15 - self.clima.Ta)) - (self.chimenea.hrws * (self.clima.T15 - self.clima.Ts))) * ((2 * tiempoActual) / (self.pared.densp * self.pared.cpp * self.pared.x))) + self.clima.T15
        temp = [To1, T11, T15_1]
        return temp

