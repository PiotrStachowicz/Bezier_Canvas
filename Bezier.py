from scipy.special import comb
import numpy as np
import math
nodes = 1000


#  Używam tutaj węzłów czebyszewa bo chcę minimalizować ilość punktów "nodes" z przyczyn optymalizacyjnych
#  (różnicę między węzłami a równomiernym rozkładem można zobaczyć w programie rozciągając mocno któryś z punktów i klikając m)
def chebyshev_nodes(a, b, dots):
    return [0.5 * (a + b) + (0.5 * (b - a) * math.cos((((2 * k) - 1) / (2 * dots)) * math.pi)) for k in range(1, dots + 1)]


CH = chebyshev_nodes(0, 1, nodes)
NP = np.linspace(0, 1, nodes)


def BezierCurve(control_points, weights, mode=True):
    def Berstein(i, n, t):
        if i < 0 or i > n:
            return 0
        return comb(n, i) * pow(t, i) * pow(1 - t, n - i)

    def Curve(n, t):
        licznik_x = sum(weights[i] * control_points[i][0] * Berstein(i, n, t) for i in range(n + 1))
        licznik_y = sum(weights[i] * control_points[i][1] * Berstein(i, n, t) for i in range(n + 1))
        mianownik = sum(weights[i] * Berstein(i, n, t) for i in range(n + 1))
        return [licznik_x / mianownik, licznik_y / mianownik]

    N = len(control_points) - 1
    if mode:
        T = CH
    else:
        T = NP

    p_array = [Curve(N, ti) for ti in T]
    return p_array


def Distance(_handle_, point2):
    return np.sqrt((_handle_.OwnerPoint.x - point2[0]) ** 2 + (_handle_.OwnerPoint.y - point2[1]) ** 2)


def DistanceXY(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def DistanceX(_handle_, point2):
    return abs(_handle_.OwnerPoint.x - point2[0])
