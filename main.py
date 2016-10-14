__author__ = 'manuel'

from procesos import Procesos
from decimal import *
from multiprocessing import Queue

cola = Queue()

procesos = Procesos()
piscina = procesos.iniciarProcesos(cola)
procesos.esperar(piscina)
menores = procesos.getMejores(cola)
if menores.__len__() >= 1:
    print("Se encontraron " + str(menores.__len__()) + " valores de aproximación menores a 1 en la vuelta ")
else:
    print("No existen resultados aceptables para mostrar")
    exit()


#vueltas, menorValor, To, Tg , Tf,round(aproximado, 5), hw, sw, hrwg, hg
dia = 24
vuelta = 2
rangoTo = Decimal(5)
while vuelta <= dia:
    flujoMasico = procesos.calcularFlujoMasico(menores)
    if flujoMasico is None:
        print("Sin Resultados del Flujo Masico")
        exit()
    else:
        nuevasTemp = procesos.calcularSegundaFase(flujoMasico[0][2][2], flujoMasico[0][2][3], flujoMasico[0][2][4], flujoMasico[0][2][6], flujoMasico[0][2][7], flujoMasico[0][2][8])
        print(nuevasTemp)
        piscina = procesos.iniciarProcesos(cola, None, nuevasTemp[0], nuevasTemp[1], None, rangoTo)

        procesos.esperar(piscina)
        menores = procesos.getMejores(cola)
        if menores.__len__() >= 1:
            print("Se encontraron " + str(menores.__len__()) + " valores de aproximación menores a 1 " + str(vuelta))
        else:
            print("No existen resultados aceptables para mostrar")
            exit()