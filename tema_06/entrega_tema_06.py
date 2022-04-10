# Ecuaciones Diferenciales Ordinarias (ODE) - Tema 6
# José Pazos Pérez - G3
# Ejercicios

# --------------------------------------------------
# Importaciones
# --------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from typing import List, Callable
from functools import wraps

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
#     - t_total : Tiempo total de la simulación
#     - dt : Paso de tiempo
# --------------------------------------------------

def ode(metodo):
    @wraps(metodo)
    def wrapper(f : List[Callable[..., float]], x0 : List[float], t_total : float, dt : float):
        assert len(x0) == len(f), "La cantidad de variables debe coincidir con la cantidad de ecuaciones"
        # Lista de valores de tiempo
        t = [0.0]
        t_restante = t_total
        # Lista de valores de cada variable en cada paso de tiempo
        x = [[x_] for x_ in x0]
        # Iteraciones de integración
        i = 0
        while t_restante > 0:
            i += 1
            t.append(t[i-1] + dt)
            t_restante -= dt
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
#       Utiliza matplotlib para representar diferentes gráficas
#       Además, añade deslizadores para personalizar la simulación desde la propia ventana
# --------------------------------------------------

# Implementación de variables estáticas a nivel decorador para compartir los ejes entre distintas funciones de ploteado
def static_vars(func, **kwargs):
    for k in kwargs:
        setattr(func, k, kwargs[k])
    return func

# Función decorador para facilitar la representación gráfica de nuestras soluciones
# Toma como parámetros el color y el nombre del método usado
def plot_ode(func, color: str, label: str):
    @wraps(func)
    def wrapper(f : List[Callable[..., float]], x0 : List[float], n : int, dt : float):
        assert plot_ode.dim == len(f), "La dimension indicada en iniciar_plot() ha de coincidir con la dimension del sistema representado"
        assert plot_ode.dim > 0 and plot_ode.dim <= 3, "Solo se puede hacer una representación para 1, 2 o 3 variables"

        # Crear sliders
        if len(plot_ode.metodos) == 0:
            ax_slider_dt = plt.axes((0.25, 0.05, 0.5, 0.03))
            plot_ode.slider_dt = Slider(ax_slider_dt, "dt", dt * 0.1, dt * 4, dt)
        
        # Añadir método
        plot_ode.metodos.append(func)

        # Cáclulo de los valores de utilizando el método apropiado (euler, rk2, rk4)
        x, t = func(f, x0, n, dt)

        # Plot principal (ax)
        # ---
        # 1D
        if len(x) == 1:
            line, = plot_ode.ax.plot(t, x[0], color=color, label=label)
            plot_ode.lines.append([line])
            plot_ode.ax.set_xlabel("t")
            plot_ode.ax.set_ylabel("x")
        # 2D
        elif len(x) == 2:
            line, = plot_ode.ax.plot(*x, color=color, label=label)
            plot_ode.lines.append([line])
            plot_ode.ax.set_xlabel("x")
            plot_ode.ax.set_ylabel("y")
        # 3D
        else:
            line, = plot_ode.ax.plot3D(*x, color=color, label=label)
            plot_ode.lines.append([line])

        # Plots auxiliares (ax_t)
        # ---
        for i in range(len(plot_ode.ax_t)):
            aux_line, = plot_ode.ax_t[i].plot(t, x[i], color=color)
            plot_ode.lines[-1].append(aux_line)
            plot_ode.ax_t[i].set_ylabel(["x", "y", "z"][i])
            if i == len(plot_ode.ax_t) - 1:
                plot_ode.ax_t[i].set_xlabel("t")

        # Actualizar al cambiar el slider
        def update(dt_):
            for i in range(len(plot_ode.metodos)):
                x, t = plot_ode.metodos[i](f, x0, n, dt_)
                # Plot principal
                if len(x) == 1:
                    plot_ode.lines[i][0].set_data(t, x[0])
                elif len(x) == 2:
                    plot_ode.lines[i][0].set_data(*x)
                else:
                    plot_ode.lines[i][0].set_data_3d(*x)
                for j in range(1, len(plot_ode.lines[i])):
                    plot_ode.lines[i][j].set_data(t, x[j-1])
        plot_ode.slider_dt.on_changed(update)
    return wrapper

# Llamar antes de iniciar una nueva gráfica, crea los ejes apropiados compartidos entre las distintas funciones
# 'dim' es la dimensión del sistema que queremos representar (1, 2 o 3)
def iniciar_plot(dim: int, title: str, xlim: List[float] = [], ylim: List[float] = []):
    assert dim > 0 and dim <= 3, "Solo se puede hacer una representación para 1, 2 o 3 variables"

    # Crear figura
    fig = plt.figure()
    fig.suptitle(title)

    # Hacer espacio para los sliders
    plt.subplots_adjust(bottom=0.25)

    # Crear axes
    ax : plt.Axes
    ax_t : List[plt.Axes] = []

    if dim == 2:
        ax = fig.add_subplot(1, 2, 1)
        ax_t.append(fig.add_subplot(2, 2, 2))
        ax_t.append(fig.add_subplot(2, 2, 4))
    elif dim == 3:
        ax = fig.add_subplot(1, 3, (1, 2), projection='3d')
        ax_t.append(fig.add_subplot(3, 3, 3))
        ax_t.append(fig.add_subplot(3, 3, 6))
        ax_t.append(fig.add_subplot(3, 3, 9))
    else:
        ax = fig.add_subplot(1, 1, 1)

    # Limites de los ejes
    if len(xlim) == 2:
        ax.set_xlim(xlim)
    if len(ylim) == 2:
        ax.set_ylim(ylim)
    
    # Configurar variables estáticas
    static_vars(plot_ode, dim=dim, fig=fig, ax=ax, ax_t=ax_t, lines=[], metodos=[])

# Mostrar el gráfico actual con leyenda
def mostrar_plot():
    plot_ode.fig.legend()
    plt.show()

# Aplicamos como decorador
plot_euler = plot_ode(ode_euler, "tomato", "euler")
plot_rk2 = plot_ode(ode_rk2, "gold", "runge kutta 2")
plot_rk4 = plot_ode(ode_rk4, "royalblue", "runge kutta 4")

#%%
# --------------------------------------------------
# Ejercicio 1
#       Ecuación logística, describe la dinámica de poblaciones : dP/dt = r * P * (1 - P/k)
#       r : Tasa de natalidad
#       k : Recursos de los que dispone la población
# --------------------------------------------------

# Condiciones iniciales
P0 = 1

# Funciones
r = 0.5
k = 100000
f = lambda P, t: r * P * (1 - P/k)

# Tiempo
dt = 0.5
t = 50

# Representación
iniciar_plot(1, "Ejercicio 1")
plot_euler([f], [P0], t, dt)
plot_rk2([f], [P0], t, dt)
plot_rk4([f], [P0], t, dt)
mostrar_plot()

#%%
# --------------------------------------------------
# Ejercicio 2
#       Oscilador armónico : x'' + w0**2 * x = 0
# --------------------------------------------------

# Condiciones iniciales
x0 = 1
w0 = 1

# Funciones
f = lambda x, y, t: y
g = lambda x, y, t: -w0**2 * x

# Tiempo
dt = 0.3
t = 10

# Representación
iniciar_plot(2, "Ejercicio 2", [-3, 3], [-3, 3])
plot_euler([f, g], [x0, w0], t, dt)
plot_rk2([f, g], [x0, w0], t, dt)
plot_rk4([f, g], [x0, w0], t, dt)
mostrar_plot()

#%%
# --------------------------------------------------
# Ejercicio 3
#       Oscilador armónico amortiguado y forzado : x'' + b * x' + w0**2 * x = F * cos(wt)
# --------------------------------------------------

from numpy import cos

# Condiciones iniciales
x0 = 1
w0 = 1

# Funciones
b = 1
F = 0.3
w = 1
f = lambda x, y, t: y
g = lambda x, y, t: -w0**2 * x - b*y + F*cos(w * t)

# Tiempo
dt = 0.3
t = 15

# Representación
iniciar_plot(2, "Ejercicio 3", [-1, 2], [-1.5, 1.5])
plot_euler([f, g], [x0, w0], t, dt)
plot_rk2([f, g], [x0, w0], t, dt)
plot_rk4([f, g], [x0, w0], t, dt)
mostrar_plot()

#%%
# --------------------------------------------------
# Ejercicio 4
#       Sistema de 3 ecuaciones diferenciales
#       dx/dt = sigma * (Y-X)
#       dy/dt = r*X - Y - X*Z
#       dz/dt = X*Y - b*Z
# --------------------------------------------------

# Condiciones iniciales
x0 = 0
y0 = 1
z0 = 0

# Funciones
sigma = 3
r = 26.5
b = 1

f = lambda x, y, z, t: sigma * (y - x)
g = lambda x, y, z, t: r * x - y - x * z
h = lambda x, y, z, t: x * y - b * z

# Tiempo
dt = 0.03
t = 30

# Representación
iniciar_plot(3, "Ejercicio 4")
plot_euler([f, g, h], [x0, y0, z0], t, dt)
plot_rk2([f, g, h], [x0, y0, z0], t, dt)
plot_rk4([f, g, h], [x0, y0, z0], t, dt)
mostrar_plot()