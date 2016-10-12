__author__ = 'manuel'

from procesos import Procesos
import time, os
from multiprocessing import Queue

cola = Queue()

procesos = Procesos()
piscina = procesos.iniciarProcesos(cola)

def esperar(piscina):
    timeEnd = 0
    while piscina:
        time.sleep(5)
        procesos.terminarProcesos(piscina)
        timeEnd = timeEnd + 5
        if timeEnd > 350:
            print("Tiempo límite exedido de 350 segundos, Fuerzo el cierre!!")
            procesos.terminarProcesos(piscina)
            idProceso = os.getpid()
            procesos.matarProcesos(idProceso)
            break

esperar(piscina)

def getMejores():
    menores = []
    while not cola.empty():
        valor = cola.get()
        if abs(valor[1]) < 1:
                menores.append(valor)
    return menores

menores = getMejores()
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

    print(flujoMasico[0][2])
    nuevasTemp = procesos.calcularSegundaFase(flujoMasico[0][2][2], flujoMasico[0][2][3], flujoMasico[0][2][4], flujoMasico[0][2][6], flujoMasico[0][2][7], flujoMasico[0][2][8])
    print(nuevasTemp)