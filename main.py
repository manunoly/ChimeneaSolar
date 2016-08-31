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
rangoTg = 5
rangoSuperiorTg = Tg + rangoTg
resultado = []
To = Tg.__int__() + rangoTg.__int__()
rangoTo = 50
incremento = 0.05
fijoTo = False

def matar_procesos(pid):
    parent = psutil.Process(pid)
    children = parent.get_children(recursive=True)

    for child in children:
        print(child)
        child.kill()
    psutil.wait_procs(children, timeout=5)


for i in range(To + 1, To + rangoTo):
    piscina.append(Process(target=TareaCalcular(i, cola, fijoTo, incremento, rangoSuperiorTg, clima, pared, vidrio).run))

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
    if not cola.empty():
        valorC = cola.get()
        if valorC[0]:
            valorF = valorC
            matar_procesos(os.getpid())
            break
        else:
            resultado.append(valorC)
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
for valor in resultado:
    if abs(valor[1]) < abs(valorFinal):
        valorFinal = valor[1]
        datosF = valor

print("To " + str(datosF[2]))
print("Tg " + str(datosF[3]))
print("Tf " + str(datosF[4]))
print("Valor de aproximación " + str(datosF[1]))
