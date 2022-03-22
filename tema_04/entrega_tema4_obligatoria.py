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
def integrar_precision(f, a, b, p, n=1, step=2):
    i0 = integrar_trapecio(f, a, b, n)
    i1 = integrar_trapecio(f, a, b, n+1)
    if (abs(i0 - i1) > p):
        return integrar_precision(f, a, b, p, n=n*step)
    return i0
# Nota: ver apéndice 1

### -----------------------------------------

# Función dada polo exercicio
f = lambda x: x**3 - 3*x**2 - x + 3
a, b = 0, 1.35
p = 1e-5

# Cálculo da integral
i = integrar_precision(f, a, b, p)

# Imprimir o resultado (nota: a última cifra decimal non é significativa)
print("i = {:.5f}, intervalo({:.2f}, {:.2f}), precisión {:.0e}".format(i, a, b, p))

### -----------------------------------------

# APENDICE 1 : Definición da función integrar
# Esta función podría definirse tomando o resultado da execución anterior en vez de calcular dúas veces o mesmo resultado, por exemplo:
'''
def integrar_precision_alt(f, a, b, p, n=1, i=0, step=10):
   i0 = integrar_trapecio(f, a, b, n, step)
   if (abs(i0 - i) > p):
       return integrar_precision(f, a, b, p, n=n*step, i=i0)
   return i0
'''
# Sen embargo, utilizando o método time.time() para medir a súa execución, vemos que o método tomando dous valores consecutivos
# é moito máis rápido, especialmente para precisións moi altas
'''
def timer(f, s, *args):
    t = time.time()
    f(*args)
    print("{}: {:f}s".format(s, time.time() - t))

for p in (1e-2, 1e-5, 1e-8, 1e-10):
    timer(integrar_precision,     "Consecutivo *10, {:.1e}".format(p), f, a, b, p, 1, 10)
    timer(integrar_precision,     " Consecutivo *4, {:.1e}".format(p), f, a, b, p, 1, 4)
    timer(integrar_precision,     " Consecutivo *2, {:.1e}".format(p), f, a, b, p, 1, 2)
    timer(integrar_precision_alt, "   Anterior *10, {:.1e}".format(p), f, a, b, p, 1, 10)
    timer(integrar_precision_alt, "    Anterior *4, {:.1e}".format(p), f, a, b, p, 1, 4)
    timer(integrar_precision_alt, "    Anterior *2, {:.1e}".format(p), f, a, b, p, 1, 2)

>>>
Consecutivo *10, 1.0e-02: 0.000387s
 Consecutivo *4, 1.0e-02: 0.000243s
 Consecutivo *2, 1.0e-02: 0.000428s
   Anterior *10, 1.0e-02: 0.000510s
    Anterior *4, 1.0e-02: 0.002002s
    Anterior *2, 1.0e-02: 0.001209s

Consecutivo *10, 1.0e-05: 0.001390s
 Consecutivo *4, 1.0e-05: 0.003362s
 Consecutivo *2, 1.0e-05: 0.002372s
   Anterior *10, 1.0e-05: 0.045147s
    Anterior *4, 1.0e-05: 0.015456s
    Anterior *2, 1.0e-05: 0.008168s

Consecutivo *10, 1.0e-08: 0.007056s
 Consecutivo *4, 1.0e-08: 0.029920s
 Consecutivo *2, 1.0e-08: 0.014657s
   Anterior *10, 1.0e-08: 0.393512s
    Anterior *4, 1.0e-08: 1.444697s
    Anterior *2, 1.0e-08: 0.677471s

Consecutivo *10, 1.0e-10: 0.067878s
 Consecutivo *4, 1.0e-10: 0.026921s
 Consecutivo *2, 1.0e-10: 0.013621s
   Anterior *10, 1.0e-10: 3.343851s
    Anterior *4, 1.0e-10: 13.421079s
    Anterior *2, 1.0e-10: 6.943275s
'''

### -----------------------------------------

# APENDICE 2: Representación gráfica
# Podemos facer unha representación gráfica dos trapecios que calculamos utlizando matplotlib
'''
def representar_integral(f, a, b, n):
    fig, ax = plt.subplots()
    h = (b - a) / n

    # Función
    x = np.linspace(a, b, 100)
    ax.plot(x, f(x), color="royalblue")
    
    # Trapecios
    colors = ("lavender", "oldlace")
    i = 0
    for a_ in np.linspace(a, b, n, endpoint=False):
        trapecio = Polygon([(a_, 0), (a_, f(a_)), (a_ + h, f(a_ + h)), (a_ + h, 0)], facecolor=colors[i%2], edgecolor='0.5')
        ax.add_patch(trapecio)
        i += 1
'''