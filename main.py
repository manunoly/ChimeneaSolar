__author__ = 'manuel'

from procesos import Procesos
import time, os
from multiprocessing import Queue

cola = Queue()
timeEnd = 0
procesos = Procesos()
piscina = procesos.iniciarProcesos(cola)

while piscina:
    time.sleep(2)
    procesos.terminarProcesos(piscina)
    timeEnd = timeEnd + 2
    if timeEnd > 150:
        print("Tiempo límite exedido de 150 segundos, Fuerzo el cierre!!")
        procesos.terminarProcesos(piscina)
        idProceso = os.getpid()
        procesos.matar_procesos(idProceso)
        break

valorFinal = 100.0
menores = []
cantV = 0

while not cola.empty():
    valor = cola.get()
    cantV = cantV + valor[0]
    if abs(valor[1]) < abs(valorFinal):
        valorFinal = valor[1]
        datosF = valor
    if abs(valor[1]) < 1:
            menores.append(valor)

if('datosF' in locals()):
    print("Cantidad de Vueltas " + str(datosF[0]) + " La mejor Temp To " + str(datosF[2]) + " La mejor Temp Tg " + str(datosF[3]) + " La mejor Temp Tf " + str(datosF[4]))
    # aproximado, hw, sw, hrwg
    print("Valor de aproximación " + str(round(datosF[1],7)))
else:
    print("No existen resultados aceptables para mostrar")
    exit()
if menores.__len__() > 1:
    print("Se encontraron " + str(menores.__len__()) + " valores de aproximación menores a 1")
    for menor in menores:
        print(str(menor[1]) + "   " + str(menor[2]) + "   " + str(menor[3]) + "   " + str(menor[4]))

#vueltas, menorValor, To, Tg , Tf,round(aproximado, 5), hw, sw, hrwg, hg
flujoMasico = procesos.calcularFlujoMasico(menores)
if flujoMasico is None:
    print("Sin Resultados del Flujo Masico")
    exit()
else:
    print(flujoMasico)
    print(flujoMasico[2])
    exit()
    To = flujoMasico[0]
    nuevosV = procesos.calcularSegundaFase(flujoMasico[2][2], flujoMasico[2][3], flujoMasico[2][4])
    print(nuevosV)