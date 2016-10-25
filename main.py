from pip._vendor.distlib.compat import raw_input

__author__ = 'manuel'

from procesos import Procesos
from decimal import *
from multiprocessing import Queue
from tareaCalcularProcesos2 import TareaCalcularSegundaFase

def entero(maximo):
    try:
        mode=int(raw_input('Input:'))
        if mode >= maximo:
            raise ValueError
        return mode
    except ValueError:
        print ("Por favor seleccione un valor válido")
        entero(maximo)

def mostrarValoresMenores(menores):
    print("#  -  Valor FlujoMasico - To")
    i = 0
    #flujoMasicoO, valorRotacion, [vueltas, menorValor, To, Tg , Tf,round(aproximado, 5), hw, sw, hrwg, hg]
    for menor in menores:
        print("Seleccione este valor tecleando " + str(i))
        print("FM - " + str(menor[3]) + " ApFM a 0 - " + str(menor[0]) + " ValorVariacionFM - " + str(menor[1]) + " To - " + str(menor[2][2]) + " Tg - " + str(menor[2][3]) + " Tf - " + str(menor[2][4]) + " Aprox a 0 - " + str(menor[2][1]))
        i = i +1

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
mostrarValoresMenores(flujoMasico)
seleccion = entero(flujoMasico.__len__())
print("Vuelta 0  To " + str(flujoMasico[seleccion][2][2]) + " Tg " + str(flujoMasico[seleccion][2][3]) + " Tf " + str(flujoMasico[seleccion][2][4]))
dia = 24
vuelta = 1
# rangoTo = Decimal(5)
while vuelta < dia:
    nuevasTemp = procesos.calcularSegundaFase(flujoMasico[seleccion][2][2], flujoMasico[seleccion][2][3], flujoMasico[seleccion][2][4], flujoMasico[seleccion][2][6], flujoMasico[seleccion][2][7], flujoMasico[seleccion][2][8], vuelta)
    print(nuevasTemp)
    piscina = procesos.iniciarProcesoSegundaFase(cola, nuevasTemp[0])
    procesos.esperar(piscina)
    menores = procesos.getMejores(cola)

    if menores.__len__() >= 1:
        seleccion = 0
        flujoMasico = procesos.calcularFlujoMasico(menores)
        if flujoMasico is None:
            print("Sin Resultados del Flujo Masico en la vuelta" + str(vuelta))
            exit()
        print("Vuelta " + str(vuelta) + " To " + str(flujoMasico[seleccion][2][2]) + " Tg " + str(flujoMasico[seleccion][2][3]) + " Tf " + str(flujoMasico[seleccion][2][4]) + " Ap " + str(flujoMasico[seleccion][2][1]))
    else:
        print("No existen valores de aproximación menores a 1 en la vuelta " + str(vuelta))
        exit()
    vuelta = vuelta + 1


