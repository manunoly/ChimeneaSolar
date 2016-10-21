__author__ = 'manuel'

from procesos import Procesos
from decimal import *
from multiprocessing import Queue
from tareaCalcularProcesos2 import TareaCalcularSegundaFase

cola = Queue()
procesos = Procesos()
piscina = procesos.iniciarProcesos(cola)
procesos.esperar(piscina)
menores = procesos.getMejores(cola)
if menores.__len__() >= 1:
    print("Se encontraron " + str(menores.__len__()) + " valores de aproximación menores a 1 en la vuelta 0")
    flujoMasico = procesos.calcularFlujoMasico(menores)
else:
    print("No existen valores de aproximación menores a 1 en la vuelta 0")
    exit()
dia = 24
vuelta = 1
# rangoTo = Decimal(5)
while vuelta < dia:
    nuevasTemp = procesos.calcularSegundaFase(flujoMasico[0][2][2], flujoMasico[0][2][3], flujoMasico[0][2][4], flujoMasico[0][2][6], flujoMasico[0][2][7], flujoMasico[0][2][8])
    print("Calculando la vuelta " + str(vuelta) + " con To " + str(nuevasTemp[0]))
    piscina = procesos.iniciarProcesoSegundaFase(cola, nuevasTemp[0])
    procesos.esperar(piscina)
    menores = procesos.getMejores(cola)
    if menores.__len__() >= 1:
        print("Se encontraron " + str(menores.__len__()) + " valores de aproximación menores a 1 en la vuelta " + str(vuelta))
    else:
        print("No existen valores de aproximación menores a 1 en la vuelta " + str(vuelta))
        exit()

    flujoMasico = procesos.calcularFlujoMasico(menores)
    if flujoMasico is None:
        print("Sin Resultados del Flujo Masico")
    exit()

    vuelta = vuelta + 1