__author__ = 'manuel'

from multiprocessing import Process, Queue
import os, psutil, time
from tareaCalcularProcesos import TareaCalcular
from clima import ClimaPropiedades
from paredPropiedades import ParedPropiedades
from vidrioPropiedades import VidrioPropiedades

cola = Queue()
piscina = []
clima = ClimaPropiedades()
pared = ParedPropiedades()
vidrio = VidrioPropiedades
Tg = clima.Ta
rangoTg = 2.0
rangoSuperiorTg = Tg + rangoTg
resultado = []
To = Tg + rangoTg
rangoTo = 15.0
incremento = 0.02
fijoTo = False

def matar_procesos(pid):
    parent = psutil.Process(pid)
    children = parent.get_children(recursive=True)

    for child in children:
        print(child)
        child.kill()
    psutil.wait_procs(children, timeout=5)
cant = 0
i = To + 0.2
limite = To + rangoTo
while (i <= limite):
    piscina.append(Process(target=TareaCalcular(i, cola, fijoTo, incremento, rangoSuperiorTg, clima, pared, vidrio).run))
    # print("proceso" + str(i))
    i = i + 0.2
    cant = cant + 1
print("Creados " + str(cant) + " procesos")

for proceso in piscina:
    proceso.start()

def terminarProcesos():
    for proceso in piscina:
        if not proceso.is_alive():
            proceso.join()
            piscina.remove(proceso)
            del(proceso)

timeEnd = 0
while piscina:
    terminarProcesos()
    # Para no saturar, dormimos al padre durante 1 segundo
    #print("esperando a que los procesos hagan su trabajo")
    time.sleep(1)
    timeEnd = timeEnd + 1
    if timeEnd > 150:
        print("Tiempo límite exedido de 180 segundos, Fuerzo el cierre!!")
        terminarProcesos()
        time.sleep(1)
        matar_procesos(os.getpid())
        break

print("PADRE: todos los hijos han terminado, cierro")
valorFinal = 100.0
while not cola.empty():
    valor = cola.get()
    if abs(valor[1]) < 1:
        print(valor)
    if abs(valor[1]) < abs(valorFinal):
        valorFinal = valor[1]
        datosF = valor

print("La mejor Temp To " + str(datosF[2]))
print("La mejor Temp Tg " + str(datosF[3]))
print("La mejor Temp Tf " + str(datosF[4]))
# aproximado, hw, sw, hrwg
print("Valor de aproximación " + str(datosF[1]))

tiempoActual = 3600
# To1 = (sw -(hw *(To -Tf) - (hrwg * (To - Tg)) - ((kp / x) * (To - T1))) * ((2 * 3600) / (cpp * densp * x))) + To
# T11 = (((pared.diff * tiempoActual) / x ** 2 ) * (T15 + To - (2 * T1))) + T1
# T15_1 = ((((pared.k / pared.x) * (T1 - T15)) - (clima.hwind * (clima.T15 - clima.Ta)) - (hrws * (clima.T15 - clima.Ts))) * ((2 * tiempoActual) / (pared.densp * pared.cpp * pared.x))) + T15
