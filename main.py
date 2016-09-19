__author__ = 'manuel'

from multiprocessing import Process, Queue
import os, psutil, time
from tareaCalcularProcesos import TareaCalcular
from clima import ClimaPropiedades
from paredPropiedades import ParedPropiedades
from vidrioPropiedades import VidrioPropiedades
from chimeneaSolar import ChimeneaSolar
from decimal import *


getcontext().prec = 10

cola = Queue()
colaT = Queue()
piscina = []
clima = ClimaPropiedades()
pared = ParedPropiedades()
vidrio = VidrioPropiedades
chimenea = ChimeneaSolar(clima, pared, vidrio)

Tg = Decimal(clima.Ta)
rangoTg = Decimal(3)
rangoSuperiorTg = Tg + rangoTg
resultado = []
To = rangoSuperiorTg
rangoTo = Decimal(10)
incremento = Decimal(0.02)
fijoTo = False
cant = 0
variacionProceso = incremento

def matar_procesos(pid):
    parent = psutil.Process(pid)
    children = parent.get_children(recursive=True)

    for child in children:
        print(child)
        child.kill()
    psutil.wait_procs(children, timeout=5)
i = To
limite = Decimal(To + rangoTo)

while (limite >= i):
    piscina.append(Process(target=TareaCalcular(limite, cola, fijoTo, incremento, rangoSuperiorTg, clima, pared, vidrio, variacionProceso, chimenea).run))
    # print("proceso " + str(i))
    piscina[piscina.__len__() - 1].start()
    limite = limite - variacionProceso
    cant = cant + 1
print("Creados " + str(cant) + " procesos")

# for proceso in piscina:
#     proceso.start()

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
    time.sleep(2)
    timeEnd = timeEnd + 2
    if timeEnd > 450:
        print("Tiempo límite exedido de 150 segundos, Fuerzo el cierre!!")
        terminarProcesos()
        matar_procesos(os.getpid())
        break

# print("PADRE: todos los hijos han terminado, cierro")
valorFinal = 100.0
menores = []
cantV = 0
cantV1 = 0
hilos = 0
while not cola.empty():
    valor = cola.get()
    if abs(valor[1]) < 1:
        menores.append(valor)
    if abs(valor[1]) < abs(valorFinal):
        valorFinal = valor[1]
        datosF = valor
if('datosF' in locals()):
    print("La mejor Temp To " + str(datosF[2]))
    print("La mejor Temp Tg " + str(datosF[3]))
    print("La mejor Temp Tf " + str(datosF[4]))
    # aproximado, hw, sw, hrwg
    print("Valor de aproximación " + str(datosF[1]))
else:
    print("No existen resultados aceptables para mostrar")
    exit()

for menor in menores:
    print(str(menor[0]) + "   " + str(menor[2]) + "   " + str(menor[3]) + "   " + str(menor[4]))

tiempoActual = 3600
# To1 = (sw -(hw *(To -Tf) - (hrwg * (To - Tg)) - ((kp / x) * (To - T1))) * ((2 * 3600) / (cpp * densp * x))) + To
# T11 = (((pared.diff * tiempoActual) / x ** 2 ) * (T15 + To - (2 * T1))) + T1
# T15_1 = ((((pared.k / pared.x) * (T1 - T15)) - (clima.hwind * (clima.T15 - clima.Ta)) - (hrws * (clima.T15 - clima.Ts))) * ((2 * tiempoActual) / (pared.densp * pared.cpp * pared.x))) + T15
