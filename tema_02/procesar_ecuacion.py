import numpy as np

# Procesar unha ecuación da forma "a1 x1 + a2 x2 + a3 x3 = b" a un array de numpy (e unha lista de nomes das variables)
# Pode ter un número N de incógnitas con un nome arbitratio, poden repetirse e os seus valores sumaránse
# Só pode estar separado por sumas ou restas
def procesar_ecuacion_con_nomes(s):
    par_dict = {}

    # Eliminar espazos
    e = s.replace(" ", "") 
    # Engadir soporte para restas
    e = e.replace("-", "+-")

    # Determinar o tipo (int ou float)
    tipo = float if "." in e else int

    # Separar en partes polo igual
    if (e.count("=") != 1):
        raise ValueError("[error] a ecuación non ten o formato correcto, falta un =")
    e_a, e_b = e.split("=")

    # Procesar parte a (dereita)
    for x in e_a.split("+"):
        # Encontrar o nome da variable
        ch = [ch for ch in x if ch.isalpha()]
        if (len(ch) == 0):
            raise ValueError("[error] a ecuación non ten o formato correcto, non engadiches o nome da variable en {}".format(x))

        # Dividir no valor e na variable
        a, xi = x.split(ch[0])
        xi = ch[0] + xi

        # Engadir ao diccionario
        try:
            par_dict[xi] = tipo(a) if not xi in par_dict else par_dict[xi] + tipo(a)
        except:
            raise ValueError("[error] a ecuación non ten o formato correcto, a non é un número({})".format(a))

    # Procesar parte b (esquerda)
    try:
        par_dict["b"] = tipo(e_b)
    except:
        raise ValueError("[error] a ecuación non ten o formato correcto, b non é un número ({})".format(e_b))

    # Convertir a numpy array
    return np.array([par_dict[x] for x in par_dict]), par_dict.keys()

# Versión simplificada que non devolve o nome das variables
def procesar_ecuacion(s):
    return procesar_ecuacion_con_nomes(s)[0]

# Exemplos

"""
from procesar_ecuacion import *

eq = procesar_ecuacion("3x1 - 2x2 + 4x1 + 4y = 5")
print(eq)

> [ 7 -2  4  5]
"""

"""
from procesar_ecuacion import *

ecuacions_s = [
    "3x - 2y + 4z = 0",
    "5x + 3y - 2z = 3",
    "2x + 4y - 3z = 4",
]

ecuacions_a = np.array(list(map(procesar_ecuacion, ecuacions_s)))
print(ecuacions_a)

> array([[ 3, -2,  4,  0],
         [ 5,  3, -2,  3],
         [ 2,  4, -3,  4]])
"""

# Nota: Para importar este ficheiro como un módulo (usando from procesar_ecuacion import *),
#       debes de colocalo na mesma carpeta co ficheiro de python no que estéas a traballar.
#       Se estás utilizando jupyter, reinicia o kernel para cargalo ou ó facer modificacións.