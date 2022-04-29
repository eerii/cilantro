# Control 2 - Ejercicio 2 - Ecuación Difusión 1D
# José Pazos Pérez - G3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler("color", ["royalblue", "mediumseagreen", "gold", "orange", "tomato", "hotpink", "mediumorchid"])

# Parámetros do problema
it = 2000
N = 20
dt = 0.001
dx = 0.1
a = 1
s = (a*dt)/dx**2

# Distribución inicial de temperatura
T = np.zeros(N+1) # Cero graos en todo
T[9:11] = 10   # Porción no centro con 10 graos
T[N] = 5 # Foco da dereita fixo a 5 graos

# Almacenamos varios valores temporais de T
# Neste caso, T[0] é o valor actual e T[1] o valor anterior
T = np.vstack([T]*2)

# Iteracións temporais
for i in range(it):
    # Actalizamos os valores intermedios (sen cambiar as condicións de frontera) co esquema de integración
    # O rango 1:N é o centrado en x, 0:N-1 é i-1 e 2:N+1 é i+1
    T[0, 1:N] = (2*s/3) * (T[1, 0:N-1] - 2*T[1, 1:N] + T[1, 2:N+1]) + (4/3) * T[0, 1:N] - (1/3) * T[1, 1:N]
    
    # Condición de frontera para o foco esquerdo de fluxo nulo
    T[0, 0] = T[0, 1]
    
    # Actualizamos o valor anterior
    T[1] = T[0].copy()
    
    # Imprimimos o resultado cada 20 iteracións nunha soa imaxe para poder ver a evolución
    if i % 30 == 0:
        plt.plot(np.linspace(0, N*dx, N+1), T[0])
        
# Amosamos a imaxe final
plt.show()