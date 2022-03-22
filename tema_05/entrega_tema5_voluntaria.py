# Números aleatorios - Tema 5
# Entrega voluntaria (Exercicio 6)
# José Pazos Pérez

import random as r
import numpy as np
import time

### -----------------------------------------

# En este exercicio o problema principal é que conforme o número de iteracións aumenta,
# o tempo de computo aumenta moito (parece que é de complexidade O(N))
# Por este motivo intentei implementar catro solucións distintas:
# - Simple (sin arrays): Tempo para 10^8: ~150s
# - Arrays grandes: Tempo para 10^8: ~12s
# - Arrays con bloques de memoria: Tempo para 10^8: ~5s
# - Arrays + JIT: Tempo para 10^8: ~1s
# * tempos medidos no meu ordenador, poden variar máis a relación entre eles debería ser similar
# A que se pide no exercicio é a solución 1, máis quería experimentar a intentar optimizala o máximo posible

### -----------------------------------------

# Pedir por entrada o método desexado
solucion = 0
print("---\nSelección de método:\n(Consulta máis información sobre os métodos no arquivo do programa)\n---")
print("1. Simple (sin arrays, ~150s para 10^8)")
print("2. Arrays grandes (~12s para 10^8)")
print("3. Bloques de memoria (~5s para 10^8)")
print("4. Compilador JIT (~1s para 10^8)")
print("---\n")
while solucion == 0:
    try:
        solucion = int(input("Seleccione o método desexado: "))
        if (solucion < 1 or solucion > 4):
            print("Introduce un número do 1 ó 4")
            solucion = 0
    except:
        print("Introduce un número válido")
    print("---\n")

### -----------------------------------------

# Datos
R = 1.5
R2 = R**2
V_real = 4/3 * np.pi * R**3
N = np.logspace(2, 8, num=7, base=10, dtype=int)

### -----------------------------------------

# Temporizador para calcular o tempo de cada iteración
def timer(f, *args):
    t = time.time()
    r = f(*args)
    return r, time.time() - t

### -----------------------------------------
# 1 SOLUCIÓN SIMPLE -------------------------

if solucion == 1:

    # Función que comproba se un punto está dentro ou fora da esfera
    f = lambda x, y, z, R: 0 if x**2 + y**2 + z**2 > R2 else 1

    # Calcula tres puntos aleatorios e utilizando a función f obtén o valor aproximado do ratio de puntos dentro e fora da esfera
    media = lambda n, R: 1/n * sum(f(r.uniform(-R, R), r.uniform(-R, R), r.uniform(-R, R), R) for i in range(n))

    # Cálculo do volume da esfera
    for n in N:
        V, t = timer(lambda : (2*R)**3 * media(n, R))
        print("n = {:.0e}, V = {:.6f}, err = {:.2e}, t = {:.4f} s".format(n, V, abs(V - V_real), t))

### -----------------------------------------
# 2 SOLUCIÓN ARRAYS GRANDES -----------------

if solucion == 2:
    print("IMPORTANTE: Este método require ó menos 2,4GB de memoria RAM")
    print("Se o seu ordenador non ten memoria RAM suficiente, podes utilizar o método 3, que arregla os problemas que ten este")
    entrada = input("Presione enter para parar o programa ou escriba 'y' para seguir: ")
    if (not (entrada == "y" or entrada == "Y")):
        exit()

    import sys

    # Función equivalente a "media" mais utilizando arrays
    # Utilizando o módulo random de numpy xera arrays con números aleatorios (xr)
    # Logo, suma os tres valores ó cadrado de x, y e z de cada elemento
    # Finalmente compara con R2 e obten a suma de valores dentro da esfera, ó que aplica a fórmula anterior para calcular o volume
    def volume(n):
        xr = np.random.rand(int(n), 3) * 2*R - R
        i = np.count_nonzero(np.sum(xr**2, axis=1) < R2)
        return (2*R)**3 * (i/n), sys.getsizeof(xr)

    # Cálculo do volume da esfera
    for n in N:
        (V, size), t = timer(volume, n)
        print("n = {:.0e}, V = {:.6f}, err = {:.2e}, t = {:.4f} s, memoria = {:.2f} MB".format(n, V, abs(V - V_real), t, size * 1e-6))

    # Podemos observar que para 10^8 hai unha mellora de unha orde de magnitude no tempo que tarda
    # Sen embargo, utiliza 2.4GB de memoria RAM para almacear todolos valores aleatorios
    # O seguinte método utiliza bloques de memoria para solventar este problema

### -----------------------------------------
# 3 SOLUCIÓN BLOQUES MEMORIA ----------------

if solucion == 3:
    import sys    
    
    # Cálculo dos bloques de memoria e do número de floats que caben nel
    # Probando diferentes valores, 1 MB parece o máis eficiente tanto en uso mínimo de RAM como en velocidade
    block_size = 2**20 # Bloques de 1 MB de RAM
    float_size = sys.getsizeof(float(0.0))
    block_n = int(block_size / float_size)

    # Moi similar á función volume anterior, só que esta vez comproba se o array resultante terá máis tamaño que o bloque que asignamos
    # Se é así, fai B arrays có tamaño indicado, e crea arrays de números aleatorios neles
    # Logo, suma todolos resultados. É un método híbrido entre os dous primeiros, con mellor rendimento que ambos
    def volume_con_bloques(n):
        I = 0
        B = int(np.ceil(n / block_n))
        for i in range(B):
            size = min(block_n, n - i*block_n)
            xr = np.random.rand(size, 3) * 2*R - R
            I += np.count_nonzero(np.sum(xr**2, axis=1) < R2)
        return (2*R)**3 * (I/n), B

    # Cálculo do volume da esfera
    for n in N:
        (V, bloques), t = timer(volume_con_bloques, n)
        print("n = {:.0e}, V = {:.6f}, err = {:.2e}, t = {:.4f} s, bloques = {:.0f}".format(n, V, abs(V - V_real), t, bloques))

### -----------------------------------------
# 4 COMPILADOR JIT --------------------------

# Python é unha linguaxe interpretada, polo que o rendemento en datos moi grandes non pode ser igual a outras linguaxes compiladas como C
# Sen embargo, nos últimos anos desarroiouse moito a tecnoloxía dos compiladores JIT ("Just in time")
# O que fan estas pezas de software é convertir funcións de python (e numpy en concreto) a código de máquina durante a execución do programa
# Esto fai que sexa moito máis rápido que a execución de python tradicional
# Ademáis, os avances nos métodos de compilación fan que esta compilación sexa máis rápida cun compilador tradicional

# Nesta solución utilizaremos o módulo "numba", un compilador JIT para python (https://numba.pydata.org)
# É necesario ter instalado esté módulo para poder executar a seguinte parte

# Veremos que os resultados son moito máis rápidos que con calqueira dos métodos polos motivos que xa explicamos
# Esto é a excepción do primeiro, que tarda sobre 3-4s. Este tempo extra é o tempo de compilación da función "volume".
# Utilizando este método as vantaxes só se ven para números moi altos

if solucion == 4:
    import sys
    import importlib.util

    if (importlib.util.find_spec("numba") == None):
        print("Erro: para executar esta solución debes instalar o módulo 'numba'")
        exit()
    
    from numba import jit

    # Esta parte da solución é idéntica á anterior, con excepción da liña @jit

    block_size = 2**20
    float_size = sys.getsizeof(float(0.0))
    block_n = int(block_size / float_size)

    @jit(nopython=True, parallel=True) # Esta liña indica que a seguinte función será compilada na execución
    def volume_jit(n):
        I = 0
        B = int(np.ceil(n / block_n))
        for i in range(B):
            size = min(block_n, n - i*block_n)
            xr = np.random.rand(size, 3) * 2*R - R
            I += np.count_nonzero(np.sum(xr**2, axis=1) < R2)
        return (2*R)**3 * (I/n), B

    for n in N:
        (V, bloques), t = timer(volume_jit, n)
        print("n = {:.0e}, V = {:.6f}, err = {:.2e}, t = {:.4f} s, bloques = {:.0f}".format(n, V, abs(V - V_real), t, bloques))