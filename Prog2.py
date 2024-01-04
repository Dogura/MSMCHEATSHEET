# This is a sample Python script.
import numpy
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.linalg import sqrtm
from scipy.stats import chi2
import random


# Nastaveni
alpha = 0.05
# stupeň volnosti = degree of freedom
df = 2

#vypočtení první transformace
def computeTransform(data, covMat, mean):

    # Pro tansformaci je použit vzorec: Z = invMat( sqrt(covMat) ) * ((jeden prvek z dat) - střední hodota)
    deltas = []
    deltas.append([])
    deltas.append([])

    # Výpočet druhé části vzorce: ((jeden prvek z dat) - střední hodota)
    for i in range(len(data)):
        deltas[0].append(data[i][0]- mean[0])
        deltas[1].append(data[i][1]- mean[1])

    # Dopočítání Z pomocí dosazení do vzorce
    Z = np.matmul(np.linalg.inv(sqrtm(covMat)), deltas)
    return Z


def transformBack(covMat, x, y, mean):

    # Pro zpětnou transformaci kružnice je použit vzorec: z =sqrt(covMat) * [𝑥,𝑦]+mean
    data = []
    data.append([])
    data.append([])

    # Nasycení polí
    for i in range(len(x)):
        data[0].append(x[i])
        data[1].append(y[i])

    # Vypočtení první části vzorce: sqrt(covMat) * [𝑥,𝑦]
    result = np.matmul(sqrtm(covMat),data)

    # Přičtení odchylek
    for i in range(len(x)):
        result[0][i] = result[0][i]+mean[0]
        result[1][i] = result[1][i] + mean[1]
    return result

    pass


def print_hi(name):


    # read iris
    fname = "iris.data"
    fil = open(fname)
    lines = fil.readlines()
    iris = {}

    # Načtení dat ze souboru a rozdělení jich do slovníku podle zařazené třídy
    for lin in lines:
        pars = lin.split(",")
        name = pars[-1].replace("\n", "")
        if name == "":
            continue
        if name not in iris.keys():
            iris[name] = []
            iris[name].append([])
            iris[name].append([])
            iris[name].append([])
            iris[name].append([])
        for i in range(len(pars) - 1):
            iris[name][i].append(float(pars[i]))

    # Vykreslení 2 dimenzí pro všechny body
    for k in iris.keys():
        plt.scatter(iris[k][0], iris[k][1])
    plt.show()

    # Vybrání pouze Iris setozy
    data = [iris['Iris-setosa'][0], iris['Iris-setosa'][1]]
    data = np.array(data)

    # Vypočtení cov matice
    covMat = np.cov(data)

    # Nutná úprava dat pro další výpočty
    data = data.T

    # Vypočtení střední hodnoty
    mean = np.mean(data,axis=0)
    print(mean)
    print(covMat)

    # Vypčtení transoframce
    tr_x = computeTransform(data,covMat,mean)
    plt.scatter(tr_x[0],tr_x[1])

    # Vykreslení kružnice v transoformovaných datech
    # Polomer = np.sqrt(chi2.ppf(1 - alpha, df))
    x = []
    y = []
    for i in range(0, 500):
        angle = random.uniform(0, 1) * (np.pi * 2)
        r = np.sqrt(chi2.ppf(1 - alpha, df))
        x.append(r*math.cos(angle))
        y.append(r*math.sin(angle))
    plt.scatter(x, y, color='red')
    plt.show()

    # Zpětná transformace dat ( kružnice )
    trb = transformBack(covMat,x,y,mean)

    # Vykreslení transformované kružnice na netransformovaná data
    plt.scatter(iris['Iris-setosa'][0], iris['Iris-setosa'][1], color='blue')
    plt.scatter(trb[0], trb[1], color='red')
    plt.show()





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
