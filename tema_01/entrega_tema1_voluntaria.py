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

# Atopar os ceros dunha función
# ceros_iniciais: lista cos valores iniciais dos subintervalos
# d_inicial: tamaño do subintervalo inicial
# funcion_c: función que devolve o punto c en cada subintervalo
# precision: valor de no que se considera que unha raíz está a 0
# Devolve unha lista de tuplas (a, d), onde a é o punto inicial e d é o tamaño do subintervalo que contén a raíz
def atopar_ceros(ceros_iniciais, d_inicial, funcion_c, precision):
    I = arr(map(lambda a : (a, d_inicial), ceros_iniciais)) # Lista de subintervalos que conteñen raíces inicialmente e os seus tamaños (a, d)
    ceros = [] # Lista de ceros final
    atopar_ceros.iteracions = 0

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
        atopar_ceros.iteracions += 1

    return ceros

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
ceros_falsi = atopar_ceros(r, di, punto_falsi, precision)

# Información
print("Regula Falsi, intervalo ({:.2f}, {:.2f}), precisión {:.0e}, iteracions {}".format(i[0], i[-1], precision, atopar_ceros.iteracions))
for a in ceros_falsi:
    print(" > Cero estimado en {:.6f}, cun valor de {:.2e}".format(a, f(a)))

### ---

# Nota: con este mesmo código pode resolverse o exercicio 3, simplemente cambiando a funcion punto_falsi polo punto medio

"""
punto_biseccion = lambda x: x[0] + (x[1] / 2)
ceros_biseccion = atopar_ceros(r, di, punto_biseccion, precision)
print("Bisección, intervalo ({:.2f}, {:.2f}), precisión {:.0e}, iteracions {}".format(i[0], i[-1], precision, atopar_ceros.iteracions))
for a in ceros_biseccion:
    print(" > Cero estimado en {:.6f}, cun valor de {:.2e}".format(a, f(a)))
"""

# Se executamos ambos códigos, vemos que pese a chegar ó mesmo resultado, o método Regula Falsi ten moitas menos iteracións que o método bisección
# O método Regula Falsi porén é moito máis eficiente para atopar raíces de funcións non lineares

"""
Regula Falsi, intervalo (-2.00, 4.00), precisión 1e-10, iteracions 12
 > Cero estimado en -0.390272, cun valor de 0.00e+00
 > Cero estimado en 1.446239, cun valor de -5.38e-11
Bisección, intervalo (-2.00, 4.00), precisión 1e-10, iteracions 33
 > Cero estimado en -0.390272, cun valor de 7.36e-11
 > Cero estimado en 1.446239, cun valor de -6.21e-11
"""

# Tamén podemos observar que cantos mais intervalos inciais utilizemos, as iteracións tenden a disminuir
# De todas maneiras, esta disminución non é continua, xa que algunhas distribucións de intervalos son máis propensas a atopar ceros rápidos
# Ademáis, canto máis se aumenta o número de intervalos, menos disminúen as iteracións, polo que tampouco é bo poñer moitos ó principio

"""
for j in range(4, 150):
    i, di = subintervalos(-2, 4, j)
    r = ceros(i)
    atopar_ceros.iteracions = 0
    ceros_falsi = atopar_ceros(r, di, punto_falsi, precision)
    print("s {} - i {}".format(j, atopar_ceros.iteracions))
"""

"""
s 4 - i 27 , s 5 - i 19 , s 6 - i 23 , s 7 - i 23 , s 8 - i 13 , s 9 - i 19 , s 10 - i 19 , s 11 - i 15 , s 12 - i 13 , s 13 - i 15 ,
s 14 - i 17 , s 15 - i 10 , s 16 - i 13 , s 17 - i 14 , s 18 - i 15 , s 19 - i 9 , s 20 - i 12 , s 21 - i 14 , s 22 - i 14 , s 23 - i 11 ,
s 24 - i 12 , s 25 - i 13 , s 26 - i 5 , s 27 - i 10 , s 28 - i 12 , s 29 - i 13 , s 30 - i 10 , s 31 - i 11 , s 32 - i 11 , s 33 - i 12 ,
s 34 - i 8 , s 35 - i 10 , s 36 - i 11 , s 37 - i 12 , s 38 - i 8 , s 39 - i 10 , s 40 - i 11 , s 41 - i 8 , s 42 - i 9 , s 43 - i 10 ,
s 44 - i 11 , s 45 - i 7 , s 46 - i 9 , s 47 - i 11 , s 48 - i 11 , s 49 - i 8 , s 50 - i 9 , s 51 - i 10 , s 52 - i 10 , s 53 - i 8 ,
s 54 - i 10 , s 55 - i 11 , s 56 - i 8 , s 57 - i 8 , s 58 - i 9 , s 59 - i 10 , s 60 - i 7 , s 61 - i 9 , s 62 - i 10 , s 63 - i 11 ,
s 64 - i 8 , s 65 - i 9 , s 66 - i 10 , s 67 - i 9 , s 68 - i 8 , s 69 - i 10 , s 70 - i 10 , s 71 - i 6 , s 72 - i 8 , s 73 - i 9 ,
s 74 - i 10 , s 75 - i 7 , s 76 - i 8 , s 77 - i 9 , s 78 - i 9 , s 79 - i 7 , s 80 - i 8 , s 81 - i 9 , s 82 - i 7 , s 83 - i 8 ,
s 84 - i 9 , s 85 - i 9 , s 86 - i 6 , s 87 - i 8 , s 88 - i 9 , s 89 - i 9 , s 90 - i 7 , s 91 - i 8 , s 92 - i 9 , s 93 - i 9 ,
s 94 - i 7 , s 95 - i 8 , s 96 - i 9 , s 97 - i 5 , s 98 - i 7 , s 99 - i 9 , s 100 - i 9 , s 101 - i 6 , s 102 - i 8 , s 103 - i 8 ,
s 104 - i 9 , s 105 - i 7 , s 106 - i 8 , s 107 - i 8 , s 108 - i 8 , s 109 - i 7 , s 110 - i 8 , s 111 - i 9 , s 112 - i 6 , s 113 - i 7 ,
s 114 - i 8 , s 115 - i 8 , s 116 - i 6 , s 117 - i 8 , s 118 - i 8 , s 119 - i 9 , s 120 - i 7 , s 121 - i 8 , s 122 - i 8 , s 123 - i 5 ,
s 124 - i 7 , s 125 - i 8 , s 126 - i 8 , s 127 - i 6 , s 128 - i 7 , s 129 - i 8 , s 130 - i 8 , s 131 - i 6 , s 132 - i 8 , s 133 - i 8 ,
s 134 - i 8 , s 135 - i 7 , s 136 - i 8 , s 137 - i 8 , s 138 - i 6 , s 139 - i 7 , s 140 - i 8 , s 141 - i 8 , s 142 - i 6 , s 143 - i 7 ,
s 144 - i 8 , s 145 - i 8 , s 146 - i 6 , s 147 - i 7 , s 148 - i 8 , s 149 - i 8
"""