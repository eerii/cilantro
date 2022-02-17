# Resolución de ecuacións non lineais - Tema 1
# Entrega obligatoria (Exercicio 1)
# Dada a función f(x) = x^2 - 3x + e^x - 2 = 0, encontrar as raíces no intervalo [-2, 4]

# Importacións
import numpy as np

# Función f(x)
f = lambda x: x**2 - 3*x + np.exp(x) - 2

# Creación de n subintervalos, devolve unha tupla (i, di)
# i : array cos n subintervalos entre a e b
# di : tamaño dun subintervalo
subintervalos = lambda a, b, n : (np.linspace(a, b, n+1), (b - a) / (n+1))

# Comprobar se dous valores teñen signo distinto, devolve un bool
signo_distinto = lambda x, y: x * y < 0

# Buscar as raíces da función no conxunto de subintervalos i
# Devolve unha lista cos valores do punto inicial de cada subintervalo que conteña ó menos unha raíz (o punto máis negativo)
ceros = lambda i : i[:-1][signo_distinto(f(i)[:-1], f(i)[1:])]

# Divisións
i, di = subintervalos(-2, 4, 20)

# Valores de f en cada división
fa = f(i)

# Lista de subintervalos que conteñen raíces
c = ceros(i)

# Información sobre as raíces
print("Ceros detectados en ({:.1f}, {:.1f}): {}".format(i[0], i[-1], len(c)))
for a in c:
    print(" > ({:.2f}, {:.2f})".format(a, a+di))