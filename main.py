__author__ = 'manuel'

from pip._vendor.distlib.compat import raw_input
from procesos import Procesos
from decimal import *
from multiprocessing import Queue
import datetime
getcontext().prec = 10
import matplotlib.pyplot as plt


def entero(maximo):
    try:
        mode=int(raw_input('Input:'))
        if mode >= maximo:
            raise ValueError
        return mode
    except ValueError:
        print ("Por favor seleccione un valor válido")
        entero(maximo)

def mostrarValoresMenores(menores, climaObj = None, limite = 100):
    print("#  -  Valor FlujoMasico - To")
    i = 0
    #flujoMasicoO, valorRotacion, [vueltas, menorValor, To, Tg , Tf,round(aproximado, 5), hw, sw, hrwg, hg]
    for menor in menores:
        print("Seleccione este valor tecleando " + str(i))
        print(str(menor[menor.__len__() - 1]) + " FM - " + str(menor[3]) + " To - " + str(menor[2][2]) + " Tg - " + str(menor[2][3]) + " Tf - " + str(menor[2][4]) + " Aprox a 0 - " + str(menor[2][1]))
        if climaObj is not None:
            print(climaObj.Ta)
        if i > limite:
            break
        i = i +1
# try:
cola = Queue()
procesos = Procesos()
climaObj = procesos.getClimaObjeto()

# plt.plot(climaObj.tamb)
# plt.ylabel('Temperaturas')
# plt.yscale('linear')
# plt.show()
# exit()

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
salida = []
salida.append([])
salida[0] = ["Vuelta;Ta;To;Tg;Tf;T1;T15;velocidadViento;radicacion;FM;AproximacionFMa0;variacionFM;Aproximacion0;VelocidadV;Tf-o;velTf"]
salida.append([])
Tfo = procesos.calcularTempFluidoSalida(flujoMasico[seleccion][2][3])
velocidadVientoFluido = procesos.calcularVelocidadFluido(Tfo)
salida[1] = [0, climaObj.Ta, flujoMasico[seleccion][2][2], flujoMasico[seleccion][2][3], flujoMasico[seleccion][2][4], climaObj.T1, climaObj.T15, climaObj.velocidadViento, climaObj.radicacion, flujoMasico[seleccion][3], flujoMasico[seleccion][0], flujoMasico[seleccion][1], flujoMasico[seleccion][2][1], climaObj.velocidadViento, Tfo, velocidadVientoFluido]
dia = climaObj.tamb.__len__()
vuelta = 1
nuevasTemperaturas = []
while vuelta < dia:
    nuevasTemp = procesos.calcularSegundaFase(flujoMasico[seleccion][2][2], flujoMasico[seleccion][2][3], flujoMasico[seleccion][2][4], flujoMasico[seleccion][2][6], flujoMasico[seleccion][2][7], flujoMasico[seleccion][2][8], vuelta)
    nuevasTemperaturas.append(nuevasTemp)
    print(nuevasTemp)
    piscina = procesos.iniciarProcesoSegundaFase(cola, nuevasTemp[0])
    procesos.esperar(piscina)
    menores = procesos.getMejores(cola)

    if menores.__len__() >= 1:
        # seleccion = 0
        # mostrarValoresMenores(flujoMasico, climaObj)
        # seleccion = entero(flujoMasico.__len__())
        flujoMasico = procesos.calcularFlujoMasico(menores)
        flujoMasico = procesos.getOptimos(flujoMasico, vuelta, salida)
        Tfo = procesos.calcularTempFluidoSalida(flujoMasico[seleccion][2][3])
        velocidadVientoFluido = procesos.calcularVelocidadFluido(Tfo)
        # mostrarValoresMenores(flujoMasico,climaObj, 3)
        vuelta = vuelta + 1
        salida.append([])
        print("Vuelta " + str(vuelta) + " Ta " + str(climaObj.Ta) + " To " + str(flujoMasico[seleccion][2][2]) + " Tg " + str(flujoMasico[seleccion][2][3]) + " Tf " + str(flujoMasico[seleccion][2][4]) + " Ap " + str(flujoMasico[seleccion][2][1]) + " Tfo " + str(Tfo) + " VelFluio " + str(velocidadVientoFluido))
        salida[vuelta] = [vuelta, climaObj.Ta, flujoMasico[seleccion][2][2], flujoMasico[seleccion][2][3], flujoMasico[seleccion][2][4], climaObj.T1, climaObj.T15, climaObj.velocidadViento, climaObj.radicacion, flujoMasico[seleccion][3], flujoMasico[seleccion][0], flujoMasico[seleccion][1], flujoMasico[seleccion][2][1], climaObj.velocidadViento, Tfo, velocidadVientoFluido]
    else:
        print("No existen valores de aproximación en la vuelta " + str(vuelta))
        break

# except Exception:
#     pass
[print(temp) for temp in nuevasTemperaturas]

fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
file ="./" + fecha + "_salidaSimulacion.csv"
with open(file, "w") as text_file:
    for content in salida:
        text_file.write(format(';'.join(str(e) for e in content)))
        text_file.write(format("\n"))
