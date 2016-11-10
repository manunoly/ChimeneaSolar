__author__ = 'manuel'

from pip._vendor.distlib.compat import raw_input
import csv
from procesos import Procesos
#from decimal import *
from multiprocessing import Queue
import datetime
salida = []
salida.append([])
salida.append([])

exit()
fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
file ="./" + fecha + "_salidaSimulacion.csv"
with open(file, "w") as text_file:
    for content in salida:
        text_file.write(format(content))
        text_file.write(format("\n"))

exit()
def entero(maximo):
    try:
        mode=int(raw_input('Input:'))
        if mode >= maximo:
            raise ValueError
        return mode
    except ValueError:
        print ("Por favor seleccione un valor válido")
        entero(maximo)

def mostrarValoresMenores(menores, climaObj = None):
    print("#  -  Valor FlujoMasico - To")
    i = 0
    #flujoMasicoO, valorRotacion, [vueltas, menorValor, To, Tg , Tf,round(aproximado, 5), hw, sw, hrwg, hg]
    for menor in menores:
        print("Seleccione este valor tecleando " + str(i))
        print(str(menor[menor.__len__() - 1]) + " FM - " + str(menor[3]) + "FM aprox a 0 " + str(menor[0]) + " ApFM a 0 - " + str(menor[0]) + " ValorVariacionFM - " + str(menor[1]) + " To - " + str(menor[2][2]) + " Tg - " + str(menor[2][3]) + " Tf - " + str(menor[2][4]) + " Aprox a 0 - " + str(menor[2][1]))
        if climaObj is not None:
            print(climaObj.Ta)
        i = i +1
# try:
cola = Queue()
procesos = Procesos()
climaObj = procesos.getClimaObjeto()
piscina = procesos.iniciarProcesos(cola)
procesos.esperar(piscina)
menores = procesos.getMejores(cola,None,20)

if menores.__len__() >= 1:
    # print("Se encontraron " + str(menores.__len__()) + " valores de aproximación menores a 1 en la vuelta 0")
    flujoMasico = procesos.calcularFlujoMasico(menores, True)
else:
    print("No existen valores de aproximación menores a 1 en la vuelta 0")
    exit()

# mostrarValoresMenores(flujoMasico, climaObj)
# seleccion = entero(flujoMasico.__len__())
seleccion = 0
print("Vuelta 0  To " + str(flujoMasico[seleccion][2][2]) + " Tg " + str(flujoMasico[seleccion][2][3]) + " Tf " + str(flujoMasico[seleccion][2][4]))
salida = ["Vuelta,Ta,To;Tg;Tf;T1;T15;velocidadViento,radicacion,FM;AproximacionFMa0;variacionFM;Aproximacion0"]
salida.append("0;" + str(climaObj.Ta) + ';' + str(flujoMasico[seleccion][2][2]) + ';' + str(flujoMasico[seleccion][2][3]) + ';' + str(flujoMasico[seleccion][2][4]) + ';'
              + str(climaObj.T1) + ';' + str(climaObj.T15) + ';' + str(climaObj.velocidadViento) + ';' + str(climaObj.radicacion) + ';'
              + str(flujoMasico[seleccion][3]) + ';' + str(flujoMasico[seleccion][0]) + ';' + str(flujoMasico[seleccion][1]) + ';' + str(flujoMasico[seleccion][2][1]))
dia = climaObj.tamb.__len__()
vuelta = 1
while vuelta < 7:
    nuevasTemp = procesos.calcularSegundaFase(flujoMasico[seleccion][2][2], flujoMasico[seleccion][2][3], flujoMasico[seleccion][2][4], flujoMasico[seleccion][2][6], flujoMasico[seleccion][2][7], flujoMasico[seleccion][2][8], vuelta)
    piscina = procesos.iniciarProcesoSegundaFase(cola, nuevasTemp[0])
    procesos.esperar(piscina)
    menores = procesos.getMejores(cola)

    if menores.__len__() >= 1:
        # seleccion = 0
        # mostrarValoresMenores(flujoMasico, climaObj)
        # seleccion = entero(flujoMasico.__len__())
        flujoMasico = procesos.calcularFlujoMasico(menores)
        flujoMasico = procesos.getOptimos(flujoMasico, vuelta, salida)
        # mostrarValoresMenores(flujoMasico,climaObj)
        if flujoMasico is None:
            print("Sin Resultados del Flujo Masico en la vuelta" + str(vuelta))
        print("Vuelta " + str(vuelta) + " Ta " + str(climaObj.Ta) + " To " + str(flujoMasico[seleccion][2][2]) + " Tg " + str(flujoMasico[seleccion][2][3]) + " Tf " + str(flujoMasico[seleccion][2][4]) + " Ap " + str(flujoMasico[seleccion][2][1]))
        salida.append(str(vuelta) + ";" + str(climaObj.Ta) + ';' + str(flujoMasico[seleccion][2][2]) + ';' + str(flujoMasico[seleccion][2][3]) + ';' + str(flujoMasico[seleccion][2][4]) + ';'
              + str(climaObj.T1) + ';' + str(climaObj.T15) + ';' + str(climaObj.velocidadViento) + ';' + str(climaObj.radicacion) + ';'
              + str(flujoMasico[seleccion][3]) + ';' + str(flujoMasico[seleccion][0]) + ';' + str(flujoMasico[seleccion][1]) + ';' + str(flujoMasico[seleccion][2][1]))
    else:
        print("No existen valores de aproximación en la vuelta " + str(vuelta))
        break
    vuelta = vuelta + 1

# except Exception:
#     pass

fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
file ="./" + fecha + "_salidaSimulacion.csv"
with open(file, "w") as text_file:
    for content in salida:
        text_file.write(format(content))
        text_file.write(format("\n"))
