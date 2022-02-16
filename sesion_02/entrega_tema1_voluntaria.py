# Resolución de ecuacións non lineais - Tema 1
# Entrega voluntaria (Exercicio 4)
# Dada a función f(x) = x^2 - 3x + e^x - 2 = 0, encontrar as raíces no intervalo [-2, 4] utilizando a regula falsi

# Importacións
import numpy as np

# Función f(x)
f = lambda x: x**2 - 3*x + np.exp(x) - 2

### ---

# Creación de n subintervalos, devolve unha tupla (i, di)
# i : array cos n subintervalos entre a e b
# di : tamaño dun subintervalo
subintervalos = lambda a, b, n : (np.linspace(a, b, n+1), (b - a) / (n+1))

# Comprobar se dous valores teñen signo distinto, devolve un bool
signo_distinto = lambda x, y: x * y < 0

# Buscar as raíces da función no conxunto de subintervalos i
# Devolve unha lista cos valores do punto inicial de cada subintervalo que conteña ó menos unha raíz (o punto máis negativo)
ceros = lambda i : i[:-1][signo_distinto(f(i)[:-1], f(i)[1:])]

### ---

# Transformar un mapa a un array de numpy
arr = lambda x : np.array(list(x))

# Dado un intervalo (a, b) de lonxitude d, que ten un punto c pertencente a el
# O parámetro i é unha tupla (a, d)
# Escoller o subintervalo no que existe unha raíz (asumindo que existe unha raíz en (a, b))
# Devolve unha tupla (a_, d_) onde a_ é o punto inicial e d_ é o tamaño do subintervalo que contén a raíz
escoller_intervalo = lambda i, c : (i[0], c-i[0]) if signo_distinto(f(i[0]), f(c)) else (c, i[1]-(c-i[0]))

# Encontrar os ceros dunha función
# ceros_iniciais: lista cos valores iniciais dos subintervalos
# d_inicial: tamaño do subintervalo inicial
# funcion_c: función que devolve o punto c en cada subintervalo
# precision: valor de no que se considera que unha raíz está a 0
# Devolve unha lista de tuplas (a, d), onde a é o punto inicial e d é o tamaño do subintervalo que contén a raíz
def encontrar_ceros(ceros_iniciais, d_inicial, funcion_c, precision):
    I = arr(map(lambda a : (a, d_inicial), ceros_iniciais)) # Lista de subintervalos que conteñen raíces inicialmente e os seus tamaños (a, d)
    ceros = [] # Lista de ceros final

    while len(I) > 0:
        # Calcular punto c en cada subintervalo
        C = map(funcion_c, I)

        # Actualizar a lista de subintervalos
        I = arr(map(escoller_intervalo, I, C))

        # Comprobar se o intervalo cumpre a precisión establecida e engadir a lista de ceros
        P = arr(map(lambda i : abs(f(i[0])) < precision, I))
        ceros += [i[0] for i in I[P]]
        I = I[~P]

        # Contar iteraciones
        encontrar_ceros.iteracions += 1

    return ceros

encontrar_ceros.iteracions = 0

### ---

# Precisión deseada
precision = 1e-10

# Funcion punto falsi
# i : intervalo no que aplicar a regula falsi, (a, d)
punto_falsi = lambda x: x[0] - (f(x[0]) * (x[1] / (f(x[0]+x[1]) - f(x[0]))))

# Divisións iniciais
i, di = subintervalos(-2, 4, 20)

# Lista de subintervalos que conteñen raíces
r = ceros(i)

# Ceros regula falsi
ceros_falsi = encontrar_ceros(r, di, punto_falsi, precision)

# Información
print("Regula Falsi, intervalo ({:.2f}, {:.2f}), precisión {:.0e}, iteracions {}".format(i[0], i[-1], precision, encontrar_ceros.iteracions))
for a in ceros_falsi:
    print(" > Cero estimado en {:.6f}, cun valor de {:.2e}".format(a, f(a)))

### ---

# Nota: con este mesmo código pode resolverse o exercicio 3, simplemente cambiando a funcion punto_falsi polo punto medio

"""
punto_biseccion = lambda x: x[0] + (x[1] / 2)
ceros_biseccion = encontrar_ceros(r, di, punto_biseccion, precision)
print("Bisección, intervalo ({:.2f}, {:.2f}), precisión {:.0e}, iteracions {}".format(i[0], i[-1], precision, encontrar_ceros.iteracions))
for a in ceros_biseccion:
    print(" > Cero estimado en {:.6f}, cun valor de {:.2e}".format(a, f(a)))
"""

# Se executamos ambos códigos, vemos que pese a chegar ó mesmo resultado, o método Regula Falsi ten moitas menos iteracións que o método bisección
# O método Regula Falsi porén é moito máis eficiente para atopar raíces de funcións non lineares

"""
Regula Falsi, intervalo (-2.00, 4.00), precisión 1e-10, iteracions 12
 > Cero estimado en -0.390272, cun valor de 0.00e+00
 > Cero estimado en 1.446239, cun valor de -5.38e-11
Bisección, intervalo (-2.00, 4.00), precisión 1e-10, iteracions 45
 > Cero estimado en -0.390272, cun valor de 7.36e-11
 > Cero estimado en 1.446239, cun valor de -6.21e-11
"""