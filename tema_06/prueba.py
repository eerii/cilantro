import numpy as np
import matplotlib.pyplot as plt

def euler(i, f, x, t, dt):
    return x[i] + dt * f[i](*x, t)

def x_medio(x, k):
    return [x[i] + 0.5*k[i] for i in range(len(x))]

def k_n(n, f, x, t, dt):
    if n == 0:
        return []
    k = [[dt * fi(*x, t) for fi in f]]
    for i in range(1, n):
        k.append([dt * fi(*x_medio(x, k[i-1]), t + 0.5*dt) for fi in f])
    return k

def runge_kutta_2(i, f, x, t, dt, k1):
    k2 = dt * f[i](*x_medio(x, k1), t + 0.5*dt)
    return x[i] + k2

def runge_kutta_4(i, f, x, t, dt, k1, k2, k3):
    k4 = dt * f[i](*[x[j] + k3[j] for j in range(len(x))], t + dt)
    return x[i] + k1[i]/6 + k2[i]/3 + k3[i]/3 + k4/6

def ode(f : list, x0 : list, dt : float, n : int, metodo, orden):
    t = np.linspace(0, (n-1) * dt, n)
    x = [[x_] for x_ in x0]
    for i in range(1, n):
        xi = [x[j][i-1] for j in range(len(x))]
        k = k_n(orden-1, f, xi, t[i], dt)
        for j in range(len(x)):
            x[j].append(metodo(j, f, xi, t[i], dt, *k))
    return (*x, t)

def plot_ode(f, x0, dt, n, metodo, orden, color, label):
    resultado = ode(f, x0, dt, n, metodo, orden)
    x, t = resultado[:-1], resultado[-1]

    # 2D
    if len(x) == 2:
        plt.plot(*x, color=color, label=label)
    # 3D
    elif len(x) == 3:
        plot_ode.ax.plot3D(*x, color=color, label=label)
    else:
        print("Solo se puede hacer un gráfico de 2 o 3 dimensiones")

plot_ode.ax = plt.axes(projection='3d')



x0 = (0, 1, 0)
dt = 0.028
n = 10000

sigma = 3
r = 26.5
b = 1

f = lambda x, y, z, t: sigma * (y - x)
g = lambda x, y, z, t: r * x - y - x * z
h = lambda x, y, z, t: x * y - b * z



plot_ode((f, g, h), x0, dt, n, euler, 1, "gold", "euler")
plot_ode((f, g, h), x0, dt, n, runge_kutta_2, 2, "tomato", "kutta 2")
plot_ode((f, g, h), x0, dt, n, runge_kutta_4, 4, "royalblue", "kutta 4")

plt.legend()
plt.show()