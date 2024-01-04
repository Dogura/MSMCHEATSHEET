import sympy as simp
import random
from matplotlib import pyplot as plt
import numpy



def postup2():
    #Definování symbolů
    x = simp.Symbol("x")
    y = simp.Symbol("y")

    #Definice základní funkce
    fun = (1-x-y)

    eq1 = simp.integrate(fun, (x, 0, 1-y)) #integrace od 0 do 1-y podle x
    eq2 = simp.integrate(eq1, (y, 0, 1))    #integrace od 0 do 1 polde y
    # Na papíře jsem použi obracený postup při integraci integruji nejdříve od 0 do 1 podley a následně od 0 do 1-x podle x

    # Vypočtení a začlenění koeficientu
    c = 1 / eq2
    print("c is ")
    print(c)
    eq1 = c*(fun)

    # Vypočtení maxima pro následné použití v zamýtací metodě
    max =  eq1.subs([(x,0),(y,0)])
    pts_y = []
    pts_x = []
    pts_ex = []
    pts_n = []
    pts_ey = []
    pts_varx = []
    pts_vary = []
    pts_cov = []
    tmpx=0
    tmpy=0
    n=0

    #generování vzorků
    for i in range(10000):
        xx = random.randint(0, 100000) / 100000.0
        yy = random.randint(0, 100000) / 100000.0
        z = (random.randint(0, 10000) / 10000.0) *max

        #Podmínky pro zamýtnutí/přijmutí vzorku
        if xx+yy <1:
            if z <= eq1.subs([(x,xx),(y,yy)]):
                n+=1
                pts_x.append(xx)
                pts_y.append(yy)
                tmpx += xx
                tmpy += yy
                pts_ex.append(float(tmpx/n))
                pts_ey.append(float(tmpy/n))
                pts_n.append(n)
                pts_varx.append(numpy.var(pts_x))
                pts_vary.append(numpy.var(pts_y))
                tmp_cov = numpy.cov(pts_x,pts_y)
                pts_cov.append(tmp_cov[0][1])


    # Vykreslení platných vzorů
    plt.scatter(pts_x, pts_y, c="blue")
    plt.title("Prostor Omega")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
    plt.scatter(pts_n, pts_ex, c="blue")
    plt.title("Vývoj Ex")
    plt.xlabel("n")
    plt.ylabel("Ex")
    plt.show()
    plt.scatter(pts_n,pts_ey, c="blue")
    plt.title("Vývoj Ey")
    plt.xlabel("n")
    plt.ylabel("Ey")
    plt.show()
    plt.scatter(pts_n,pts_varx, c="blue")
    plt.title("Vývoj var(x)")
    plt.xlabel("n")
    plt.ylabel("Var(x)")
    plt.show()
    plt.scatter(pts_n,pts_vary, c="blue")
    plt.title("Vývoj var(y)")
    plt.xlabel("n")
    plt.ylabel("Var(y)")
    plt.show()
    plt.scatter(pts_n,pts_cov, c="blue")
    plt.title("Vývoj cov(x,y)")
    plt.xlabel("n")
    plt.ylabel("Cov(x,y)")
    plt.show()
    print("teoretická střední hodnota x je 0.25 a vypočtená na vygenerovaných datech je " + str(sum(pts_x) / len(pts_x)))
    print("teoretická střední hodnota y je 0.25 a vypočtená na vygenerovaných datech je " + str(sum(pts_y) / len(pts_y)))
    print("var matice na vygenerovaných datech:")
    print((numpy.cov(pts_x,pts_y)))
    print("var matice teoreticky vypočtená:")
    print([[0.0375,-0.0125],[-0.0125,0.0375]])
    plt.show()

    # Konvergence výsledků je podle mého pozorování nejrychlejší v případě středníhodnoty a následně covariance s rozptyly


if __name__ == '__main__':
    postup2()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
