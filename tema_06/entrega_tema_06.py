# Ecuaciones Diferenciales Ordinarias (ODE) - Tema 6
# José Pazos Pérez - G3
# Ejercicios

# --------------------------------------------------
# Importaciones
# --------------------------------------------------
import matplotlib.pyplot as plt
from typing import List, Callable
import functools

# --------------------------------------------------
# Esquemas de integración
#     - Euler : Error dt**2
#     - Runge-Kutta 2º orden : Error dt**3
#     - Runge-Kutta 4º orden : Error dt**5
# Parámetros
#     - f : Lista de funciones pendiente para cada variable
#     - x : Lista de valores actuales de cada variable
#     - t : Tiempo actual
#     - dt : Paso de tiempo
# --------------------------------------------------

# Método de Euler
def euler(f : List[Callable[..., float]], x : List[float], t : float, dt : float):
    return [x[i] + dt * f[i](*x, t) for i in range(len(x))]

# Método de Runge-Kutta 2º orden
def runge_kutta_2(f : List[Callable[..., float]], x : List[float], t : float, dt : float):
    r = range(len(x))
    k1 = [dt * fi(*x, t) for fi in f]
    k2 = [dt * fi(*[x[i] + k1[i]*0.5 for i in r], t + dt*0.5) for fi in f]
    return [x[i] + k2[i] for i in r]

# Método de Runge-Kutta 4º orden
def runge_kutta_4(f : List[Callable[..., float]], x : List[float], t : float, dt : float):
    r = range(len(x))
    k1 = [dt * fi(*x, t) for fi in f]
    k2 = [dt * fi(*[x[i] + k1[i]*0.5 for i in r], t + dt*0.5) for fi in f]
    k3 = [dt * fi(*[x[i] + k2[i]*0.5 for i in r], t + dt*0.5) for fi in f]
    k4 = [dt * fi(*[x[i] + k3[i] for i in r], t + dt) for fi in f]
    return [x[i] + k1[i]/6 + k2[i]/3 + k3[i]/3 + k4[i]/6 for i in r]

# --------------------------------------------------
# Resolver un sistema de n ecuaciones diferenciales
# Parámetros
#     - f : Lista de funciones pendiente para cada variable
#     - x0 : Lista de valores iniciales de cada variable
#     - n : Número de pasos deseado
#     - dt : Paso de tiempo
# --------------------------------------------------

def ode(metodo):
    @functools.wraps(metodo)
    def wrapper(f : List[Callable[..., float]], x0 : List[float], n : int, dt : float):
        assert len(x0) == len(f), "La cantidad de variables debe coincidir con la cantidad de ecuaciones"
        # Lista de valores de tiempo
        t = [t_ * dt for t_ in range(n)]
        # Lista de valores de cada variable en cada paso de tiempo
        x = [[x_] for x_ in x0]
        # Iteraciones de integración
        for i in range(1, n):
            resultado = metodo(f, [x_[i-1] for x_ in x], t[i], dt)
            [x[i].append(resultado[i]) for i in range(len(f))]
        return x, t
    return wrapper

# Aplicamos el decorador de manera no destructiva
ode_euler = ode(euler)
ode_rk2 = ode(runge_kutta_2)
ode_rk4 = ode(runge_kutta_4)

# --------------------------------------------------
# Representación gráfica con matplotlib
# --------------------------------------------------

# Implementación de variables estáticas a nivel decorador para compartir los ejes entre distintas funciones de ploteado
def static_vars(func, **kwargs):
    for k in kwargs:
        setattr(func, k, kwargs[k])
    return func

# Función decorador para facilitar la representación gráfica de nuestras soluciones
# Toma como parámetros el color y el nombre del método usado
def plot_ode(func, color: str, label: str):
    @functools.wraps(func)
    def wrapper(f : List[Callable[..., float]], x0 : List[float], n : int, dt : float):
        assert plot_ode.dim == len(f), "La dimension indicada en iniciar_plot() ha de coincidir con la dimension del sistema representado"
        assert plot_ode.dim > 0 and plot_ode.dim <= 3, "Solo se puede hacer una representación para 1, 2 o 3 variables"

        # Cáclulo de los valores de utilizando el método apropiado (euler, rk2, rk4)
        x, t = func(f, x0, n, dt)

        # Plot principal (ax)
        # ---
        # 1D
        if (len(x) == 1):
            plot_ode.ax.plot(t, x[0], color=color, label=label)
            plot_ode.ax.set_xlabel("t")
            plot_ode.ax.set_ylabel("x")
        # 2D
        if (len(x) == 2):
            plot_ode.ax.plot(*x, color=color, label=label)
            plot_ode.ax.set_xlabel("x")
            plot_ode.ax.set_ylabel("y")
        # 3D
        if (len(x) == 3):
            plot_ode.ax.plot(*x, color=color, label=label)

        # Plots auxiliares (ax_t)
        # ---
        for i in range(len(plot_ode.ax_t)):
            plot_ode.ax_t[i].plot(t, x[i], color=color, label=label)
            plot_ode.ax_t[i].set_ylabel(["x", "y", "z"][i])
            if i == len(plot_ode.ax_t) - 1:
                plot_ode.ax_t[i].set_xlabel("t")

        # Otros parámetros
        plt.legend()
    return wrapper

# Llamar antes de iniciar una nueva gráfica, crea los ejes apropiados compartidos entre las distintas funciones
# 'dim' es la dimensión del sistema que queremos representar (1, 2 o 3)
def iniciar_plot(dim: int, title: str):
    fig = plt.figure()
    fig.suptitle(title)
    plt.subplots_adjust(bottom=0.25)
    if dim == 1:
        ax = fig.add_subplot(1, 1, 1)
        static_vars(plot_ode, dim=dim, ax=ax, ax_t=[])
    if dim == 2:
        ax = fig.add_subplot(1, 2, 1)
        ax_tx = fig.add_subplot(2, 2, 2)
        ax_ty = fig.add_subplot(2, 2, 4)
        static_vars(plot_ode, dim=dim, ax=ax, ax_t=[ax_tx, ax_ty])
    if dim == 3:
        ax = fig.add_subplot(1, 3, (1, 2), projection='3d')
        ax_tx = fig.add_subplot(3, 3, 3)
        ax_ty = fig.add_subplot(3, 3, 6)
        ax_tz = fig.add_subplot(3, 3, 9)
        static_vars(plot_ode, dim=dim, ax=ax, ax_t=[ax_tx, ax_ty, ax_tz])

# Aplicamos como decorador
plot_euler = plot_ode(ode_euler, "tomato", "euler")
plot_rk2 = plot_ode(ode_rk2, "gold", "runge kutta 2")
plot_rk4 = plot_ode(ode_rk4, "royalblue", "runge kutta 4")




# --------------------------------------------------
# Ejercicios
# --------------------------------------------------

f = lambda P, t, r, k: r * P * (1 - P/k) 

r = 0.5
k = 10
f_ = lambda P, t: f(P, t, r, k)

dt = 0.5
n = 100
P0 = 0.0001

iniciar_plot(1, "Ejercicio 1")
plot_euler([f_], [P0], n, dt)
plot_rk2([f_], [P0], n, dt)
plot_rk4([f_], [P0], n, dt)

plt.show()

x0 = [0.0, 1.0, 0.0]
dt = 0.028
n = 10000

sigma = 3
r = 26.5
b = 1

f = lambda x, y, z, t: sigma * (y - x)
g = lambda x, y, z, t: r * x - y - x * z
h = lambda x, y, z, t: x * y - b * z

iniciar_plot(3, "Ejercicio 2")
plot_euler([f, g, h], x0, n, dt)
plot_rk2([f, g, h], x0, n, dt)
plot_rk4([f, g, h], x0, n, dt)

#plt.show()