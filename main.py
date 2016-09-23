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
    if timeEnd > 250:
        print("Tiempo límite exedido de 150 segundos, Fuerzo el cierre!!")
        procesos.terminarProcesos()
        procesos.matar_procesos(os.getpid())
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
        if abs(valor[1]) < 0.1:
            menores.append(valor)

if('datosF' in locals()):
    print("Cantidad de Vueltas " + str(datosF[0]))
    print("La mejor Temp To " + str(datosF[2]))
    print("La mejor Temp Tg " + str(datosF[3]))
    print("La mejor Temp Tf " + str(datosF[4]))
    # aproximado, hw, sw, hrwg
    print("Valor de aproximación " + str(datosF[1]))
else:
    print("No existen resultados aceptables para mostrar")
    exit()
if menores.__len__() >= 1:
    print("Se encontraron " + str(menores.__len__()) + " valores menores a 1")
    for menor in menores:
        print(str(menor[1]) + "   " + str(menor[2]) + "   " + str(menor[3]) + "   " + str(menor[4]))

#vueltas, menorValor, To, Tg , Tf,round(aproximado, 5), hw, sw, hrwg, hg
procesos.calcularFlujoMasico(menores)