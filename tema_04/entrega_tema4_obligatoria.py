# Integración numérica - Tema 4
# Entrega obligatoria (Exercicio 1)
# José Pazos Pérez

import numpy as np

### -----------------------------------------

# Integración pola regra do trapecio da función f no intervalo (a, b) con n subintervalos
def integrar_trapecio(f, a, b, n):
    trapecio = lambda f, a, b: (b - a)/2 * (f(a) + f(b)) # Aplicación da regra nun subintervalo
    h = (b - a) / n
    i = [trapecio(f, a_, a_ + h) for a_ in np.linspace(a, b, n, endpoint=False)]
    return sum(i)

# Integración con precisión
# Devolve o resultado da integral pola regra do trapecio con unha precisión p
# Para unha mellor optimización, salta de valores multiplicando por 'step', e calcula dous valores contiguos para comprobar a precisión
def integrar_precision(f, a, b, p, n=1, step=10):
    i0 = integrar_trapecio(f, a, b, n)
    i1 = integrar_trapecio(f, a, b, n+1)
    if (abs(i0 - i1) > p):
        return integrar_precision(f, a, b, p, n=n*step)
    return i0
# Nota: sobre el diseño del programa
# Esta función podría definirse tomando el resultado de la ejecución anterior en vez de calculando dos veces el mismo resultado, por exemplo:
# def integrar_precision(f, a, b, p, n=1, i=0, step=10):
#    i0 = integrar_trapecio(f, a, b, n)
#    if (abs(i0 - i) > p):
#        return integrar_precision(f, a, b, p, n=n*step, i=i0)
#    return i0


### -----------------------------------------

# Función dada polo exercicio
f = lambda x: x**3 - 3*x**2 - x + 3
a, b = 0, 1.35
p = 1e-5

# Cálculo da integral
i = integrar_precision(f, a, b, p)

print("i = {:.5f}, intervalo({:.2f}, {:.2f}), precisión {:.0e}".format(i, a, b, p))