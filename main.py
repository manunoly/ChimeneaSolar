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
    print("Se encontraron " + str(menores.__len__()) + " valores de aproximación menores a 1")
    # for menor in menores:
    #     print(str(menor[1]) + "   " + str(menor[2]) + "   " + str(menor[3]) + "   " + str(menor[4]))
else:
    print("No existen resultados aceptables para mostrar")
    exit()

#vueltas, menorValor, To, Tg , Tf,round(aproximado, 5), hw, sw, hrwg, hg
flujoMasico = procesos.calcularFlujoMasico(menores)
if flujoMasico is None:
    print("Sin Resultados del Flujo Masico")
    exit()
else:
    # for valoresFM  in flujoMasico:
        #[primerCalculoAproximacion, M(valor de vaciacion), [vueltas, menorValor, To, Tg , Tf,round(aproximado, 5), hw, sw, hrwg, hrgs], flujoMasico]
        # print("valor FM" + str(flujoMasico[flujoMasico.__len__() - 1]) + " Valores To, Tg , Tf ")
    flujoMasico[0][2]
    nuevasTemp = procesos.calcularSegundaFase(flujoMasico[0][2][2], flujoMasico[0][2][3], flujoMasico[0][2][4], flujoMasico[0][2][6], flujoMasico[0][2][7], flujoMasico[0][2][8])
    rangoTo = round(flujoMasico[0][2][2] - flujoMasico[0][2][3] - 2, 0)
    print(type(rangoTo))
    print(rangoTo)
    if rangoTo < 5:
        rangoTo = 5
    elif rangoTo > 10:
        rangoTo = 10
    print(rangoTo)
    piscina = procesos.iniciarProcesos(cola, None, nuevasTemp[0], nuevasTemp[1], None, Decimal(rangoTo))

    procesos.esperar(piscina)
    menores = procesos.getMejores(cola)
    if menores.__len__() >= 1:
        print("Se encontraron " + str(menores.__len__()) + " valores de aproximación menores a 1")
        # for menor in menores:
        #     print(str(menor[1]) + "   " + str(menor[2]) + "   " + str(menor[3]) + "   " + str(menor[4]))
    else:
        print("No existen resultados aceptables para mostrar")
        exit()