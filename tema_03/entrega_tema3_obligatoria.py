# Derivación numérica - Tema 3
# Entrega obligatoria (Exercicio 1)
# José Pazos Pérez

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
f = lambda x : -0.1*x**4 - 0.15*x**3 - 0.5*x**2 - 0.25*x + 1.2
f_ = lambda x : -0.4*x**3 - 0.45*x**2 - 1*x + - 0.25

# Erro do valor da aproximación (v) e o valor real da derivada
erro = lambda v, x0 : abs(f_(x0) - v)

# Parámetros do exercicio
x0 = 0.5
h = 0.25

### -----------------------------------------

# Cálculo da derivada polos tres métodos
d_1 = diferencia_hacia_adelante(f, x0, h)
d_2 = diferencia_hacia_atras(f, x0, h)
d_3 = diferencia_centrada(f, x0, h)

print("ec. 3:  {:.4f}, erro: {:.4f}".format(d_1, erro(d_1, x0)))
print("ec. 7:  {:.4f}, erro: {:.4f}".format(d_2, erro(d_2, x0)))
print("ec. 10: {:.4f}, erro: {:.4f}".format(d_3, erro(d_3, x0)))