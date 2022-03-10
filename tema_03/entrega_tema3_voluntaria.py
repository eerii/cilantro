# Derivación numérica - Tema 3
# Entrega voluntaria (Exercicio 5)
# José Pazos Pérez

import numpy as np
import matplotlib.pyplot as plt

### -----------------------------------------

# Diferencias hacia adelante (ec. 3)
# E(h) = -h/2 * f''(x0)
def diferencia_hacia_adelante(f, x0, h):
    return (f(x0 + h) - f(x0))/h

# Diferencias hacia atrás (ec. 7)
# E(h) = h/2 * f''(x0)
def diferencia_hacia_atras(f, x0, h):
    return (f(x0) - f(x0 - h))/h

# Diferencias centradas (ec. 10)
# E(h) = h**2/6 * f'''(x0)
def diferencia_centrada(f, x0, h):
    return (f(x0 + h) - f(x0 - h))/(2*h)

### -----------------------------------------

# Función definida no exercicio e a súa derivada para comprobar o valor real
f = lambda x : x**5 - 3*x**4 - 11*x**3 + 19*x**2 + 10*x - 24

# Parámetros do exercicio
h = 0.25

### -----------------------------------------

# Representación da función e das tres derivadas que calculamos
def representar_funcion(ab, nome):
    # Función
    x = np.linspace(ab[0], ab[1], 100)
    y = f(x)
    plt.plot(x, y, color="royalblue", label="$f(x)$")

    # Eje x
    x0 = np.linspace(ab[0], ab[1], 10)
    y0 = np.zeros(10)
    plt.plot(x0, y0, color="slategray")

    # Derivación centrada
    y_dc = diferencia_centrada(f, x, h)
    plt.plot(x, y_dc, color="orange", label="d. centrada (10)")

    # Derivación hacia adelante
    y_ad = diferencia_hacia_adelante(f, x, h)
    plt.plot(x, y_ad, color="tomato", label="d. adelante (3)")

    # Derivación hacia atrás
    y_at = diferencia_hacia_atras(f, x, h)
    plt.plot(x, y_at, color="gold", label="d. atrás (7)")

    plt.title(nome)
    plt.legend()
    plt.show()

# Representamos a función nos tres intervalos
representar_funcion((-2.5, 2.5), "Figura a")
representar_funcion((-1.5, 1.5), "Figura b")
representar_funcion((-1.0, 1.0), "Figura c")