# Control 1 - Ejercicio 2 - Método de Runge Kutta 4
# José Pazos Pérez - G3

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Callable

# --------------------------------------------
# Runge Kutta 4
# --------------------------------------------

Funcion = Callable[..., float]

def ode(func):
    def wrapper(f : List[Funcion], x0 : List[float], n : int, dt : float):
        x = [[x_] for x_ in x0]
        t = np.linspace(0, n * dt, n)
        for i in range(1, n):
            resultado = func(f, [x_[i-1] for x_ in x], t[i], dt)
            [x[i].append(resultado[i]) for i in range(len(x))]
        return x
    return wrapper

@ode
def runge_kutta_4(f : List[Funcion], x : List[float], t : float, dt : float):
    k1 = [dt * fi(t, *x) for fi in f]
    k2 = [dt * fi(t + dt*0.5, *[x[i] + k1[i]*0.5 for i in range(len(x))]) for fi in f]
    k3 = [dt * fi(t + dt*0.5, *[x[i] + k2[i]*0.5 for i in range(len(x))]) for fi in f]
    k4 = [dt * fi(t + dt, *[x[i] + k3[i] for i in range(len(x))]) for fi in f]
    return [x[i] + k1[i]/6 + k2[i]/3 + k3[i]/3 + k4[i]/6 for i in range(len(x))]

# --------------------------------------------
# Datos
# --------------------------------------------

a = 1
b = 0.3
d = 0.1
dt = 0.01

du = lambda t, u, v: (u * (1-u)) - (a*u*v)/(u+d)
dv = lambda t, u, v: b * u * (1 - v/u)

u0 = 0.8
v0 = 0.3

n = 10000

# --------------------------------------------
# Cálculo y representación
# --------------------------------------------

u, v = runge_kutta_4((du, dv), (u0, v0), n, dt)
    
plt.plot(u, v, color="royalblue")
plt.show()