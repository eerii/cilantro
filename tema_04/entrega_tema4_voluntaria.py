# Integración numérica - Tema 4
# Entrega voluntaria (Exercicio 6)
# José Pazos Pérez

import numpy as np
import pandas as pd

### -----------------------------------------

# Integración pola regra de simpson 1/3 composta da función f no intervalo (a, b) con n subintervalos
def integrar_simpson_comp(f, a, b, n):
    h = (b-a)/(2*n)
    i0 = (h/3) * (f(a) + f(b))
    i1 = ((2*h)/3) * sum([f(a + (2*k)*h) for k in range(1, n)])
    i2 = ((4*h)/3) * sum([f(a + (2*k-1)*h) for k in range(1, n+1)])
    return (i0 + i1 + i2)

# Integración con precisión
# Devolve o resultado da integral pola regra de simpson con unha precisión p
# Para unha mellor optimización, salta de valores multiplicando por 'step', e calcula dous valores contiguos para comprobar a precisión
def integrar_precision(f, a, b, p, n=1, step=2):
    i0 = integrar_simpson_comp(f, a, b, n)
    i1 = integrar_simpson_comp(f, a, b, n+1)
    if (abs(i0 - i1) > p):
        return integrar_precision(f, a, b, p, n=n*step)
    return i0

# Integral da función x**a * np.exp(x) utilizando unha relación de recurrencia
def integral_recurrencia(i, n, a):
    if (n < a):
        return integral_recurrencia(np.e - (n+1) * i, n+1, a)
    return i

### -----------------------------------------

# Función dada polo exercicio
f = lambda x, a: x**a * np.exp(x)
i0, i1 = 0, 1
p = 1e-5

# Cálculo da integral pola regra de simpson para a = 0, 1, 2, 3, 4, 5, 6
i_simpson = []
for a in range(7):
    f_ = lambda x: f(x, a)
    i_simpson.append(integrar_precision(f_, i0, i1, p))

# Cálculo da integral por recurrencia
i_recurrencia = []
for a in range(7):
    i_recurrencia.append(integral_recurrencia(np.e - 1, 0, a))

# Errores
error_absoluto = [abs(i_simpson[a] - i_recurrencia[a]) for a in range(7)]
error_relativo = [error_absoluto[a] / i_recurrencia[a] for a in range(7)]

# Imprimir os resultados
d = pd.DataFrame({
    "Simpson 1/3 comp.": ["{:.5f}".format(i) for i in i_simpson], 
    "Recurrencia": ["{:.5f}".format(i) for i in i_recurrencia],
    "Erro abs.": ["{:.5f}".format(e) for e in error_absoluto],
    "Erro rel.": ["{:.3f}%".format(e * 100) for e in error_relativo]
})
print(d)

### -----------------------------------------

# APENDICE 1: Representación gráfica
# Podemos facer unha representación gráfica das áreas que calculamos utlizando matplotlib

'''
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def representar_integral_simpson(f, a, b, n):
    fig, ax = plt.subplots()
    h = (b - a) / n

    # Función
    x = np.linspace(a, b, 100)
    ax.plot(x, f(x), color="royalblue")

    # Polinomio Simpson
    S = lambda x1, x2, x3, x: f(x1) * (((x-x2)*(x-x3)) / ((x1-x2)*(x1-x3))) + f(x2) * (((x-x1)*(x-x3)) / ((x2-x1)*(x2-x3))) + f(x3) * (((x-x1)*(x-x2)) / ((x3-x1)*(x3-x2)))

    # Trapecios
    colors = ("lavender", "oldlace")
    i = 0
    for a_ in np.linspace(a, b, n, endpoint=False):
        b_ = a_ + h
        c_ = (b_ + a_) / 2
        m = 5
        curva_x = np.linspace(a_, b_, m)
        curva_y = S(a_, b_, c_, curva_x)
        curva = [(a_, 0)] + [(curva_x[i], curva_y[i]) for i in range(m)] + [(b_, 0)]
        poly = Polygon(curva, facecolor=colors[i%2], edgecolor='0.5')
        ax.add_patch(poly)
        i += 1
    
    plt.show()

def integrar_precision_representacion(f, a, b, p, n=1, step=2):
    i0 = integrar_simpson_comp(f, a, b, n)
    i1 = integrar_simpson_comp(f, a, b, n+1)
    if (abs(i0 - i1) > p):
        return integrar_precision_representacion(f, a, b, p, n=n*step)
    representar_integral_simpson(f, a, b, n)
    return i0

for a in range(7):
    f_ = lambda x: f(x, a)
    integrar_precision_representacion(f_, i0, i1, p)
'''