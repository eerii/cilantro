# Números aleatorios - Tema 5
# Entrega obligatoria (Exercicio 1)
# José Pazos Pérez

import random as r
import numpy as np
import matplotlib.pyplot as plt

### -----------------------------------------

# Función paso: devolve ou 1 ou -1 de maneira aleatoria
paso = lambda : 1 if r.random() < 0.5 else -1
# Número de pasos
n = 3000
# Número de simulacións (para facer varios random walks e ver os resultados)
runs = 1

for i in range(runs):
    # Calculamos unha lista de pasos aleatorios
    pasos = [paso() for i in range(n)]
    # Sumamos o resultado para obter o camiño recorrido
    walk = np.cumsum(pasos)
    # Imprimimos o camiño
    plt.plot(walk)

plt.show()