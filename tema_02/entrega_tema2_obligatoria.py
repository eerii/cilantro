# Sistemas de ecuacións lineais - Tema 2
# Entrega obligatoria (Exercicio 1)
# Eliminación gaussiana sen pivoteo

# Librerías
import numpy as np

### -----------------------------------------
#   Definición de funcións xerais
### -----------------------------------------

# Función max:
# Toma unha lista e devolve o valor do elemento máximo
# Pode ser sustituída por max() ou np.max()
def max_(l):
    m = l[0]
    for i in l:
        m = m if m > i else i
    return m

# Funcións argmax:
# Toma unha lista e devolve o valor do indice do elemento máximo
# Pode ser sustituída por np.argmax()
def argmax_(l):
    a = 0
    for i in range(len(l)):
        a = a if l[a] > l[i] else i
    return a

# Matrices bonitas:
# Imprime unha matriz de maneira elegante coa columna de términos independentes separada
def print_matriz(m, nome=None, despois=None):
    n_filas = len(m)
    n_columnas = len(m[0])

    if nome is not None:
        print("{}".format(nome))

    anchuras = [max_([len(str(m[i][j])) for i in range(n_filas)]) for j in range(n_columnas)]
    for i in range(len(m)):
        coefs = " ".join([str(m[i][j]).rjust(max_(anchuras[:-1])) for j in range(n_columnas-1)])
        print(coefs, "|", str(m[i][-1]).rjust(anchuras[-1]))
        
    if despois is not None:
        print(despois)

# Procesar unha ecuación da forma "a1 x1 + a2 x2 + a3 x3 = b" a un array de numpy (e unha lista de nomes das variables)
# Pode ter un número N de incógnitas con un nome arbitratio, poden repetirse e os seus valores sumaránse
# Só pode estar separado por sumas ou restas
# Poden pasarse M ecuacións e devolverá un array de orde 2
# Esta función é totalmente opcional para o funcionamento do programa, xa que podería pasarse simplemente
# un par de matrices (coeficientes e termos independientes), pero parecíame interesante tratar de implementala
def procesar_ecuacion(*args, nomes=False):
    ecuaciones = []
    keys = []

    for arg in args:
        ecuaciones.append({})
        d = ecuaciones[-1]

        # Eliminar espazos
        e = arg.replace(" ", "") 

        # Determinar o tipo (int ou float)
        tipo = float if "." in e else int

        # Separar en partes polo igual
        if (e.count("=") != 1):
            raise ValueError("[error] a ecuación non ten o formato correcto, falta un =")
        e_a, e_b = e.split("=")

        # Engadir soporte para restas
        e_a = e_a.replace("-", "+-")
        if e_a[0] == "+":
            e_a = e_a[1:]

        # Procesar parte a (dereita)
        for x in e_a.split("+"):
            # Encontrar o nome da variable
            ch = [ch for ch in x if ch.isalpha()]
            if (len(ch) == 0):
                raise ValueError("[error] a ecuación non ten o formato correcto, non engadiches o nome da variable en {}".format(x))

            # Dividir no valor e na variable
            a, xi = x.split(ch[0])
            xi = ch[0] + xi

            # Sustitucións comúns
            if (a == ""):
                a = "1"
            if (a == "-"):
                a = "-1"

            # Engadir ao diccionario
            try:
                d[xi] = tipo(a) if not xi in d else d[xi] + tipo(a)
            except:
                raise ValueError("[error] a ecuación non ten o formato correcto, a non é un número({})".format(a))

        # Procesar parte b (esquerda)
        try:
            d["b"] = tipo(e_b)
        except:
            raise ValueError("[error] a ecuación non ten o formato correcto, b non é un número ({})".format(e_b))

        # Engadir novas chaves ó diccionario
        if len(keys) == 0:
            keys = list(d.keys())
        new_keys = set(d.keys()) - set(keys)
        for k in new_keys:
            keys.insert(-1, k)
        for e in ecuaciones:
            e.update(dict([(k, 0) for k in new_keys if not k in e]))

        # Arreglar as variables que faltan na ecuación
        missing_keys = set(keys) - set(d.keys())
        for k in missing_keys:
            d[k] = 0

    # Ordear a lista de ecuacións polos nomes ordeados
    ec_list = [[ec[key] for key in sorted(ec.keys(), key=lambda x: keys.index(x))] for ec in ecuaciones]
    # Devolver un array de orde 1 ou 2 (dependendo de unha ou máis ecuacións pasadas á función)
    # Tamén devolve os nomes das incógnitas se está así indicado
    ec_arr = np.array(ec_list[0]) if len(ec_list) == 1 else np.array(ec_list)
    if nomes:
        return ec_arr, keys
    return ec_arr

### -----------------------------------------


### -----------------------------------------
#   Definición de funcións específicas
### -----------------------------------------

# Eliminación de Gauss
# Algoritmo para eliminar os ceros dunha columna nunha matriz representando un sistema de ecuacións
# - sistema: Matriz extendida dun sistema de ecuacións
# - columna: Indice da columna actual
# - salida: Imprimir os pasos un por un
# Ademáis, tamén ten variables propias que persisten entre varias execucións (o motivo será claro cando implementemos a seguinte función)
# - eliminacion_gauss.fila_pivote: Indice da fila que esteamos a utilizar como pivote actualmente
# - eliminacion_gauss.outras_filas: Lista coas filas que quedan por pivotar
# Todos as liñas que comezan en 'if salida:' son para imprimir en pantalla
def eliminacion_gauss(sistema, columna, salida=True):
    p = sistema[eliminacion_gauss.fila_pivote][columna]

    if salida:
        print("Columna {}, Fila pivote: {}".format(columna+1, eliminacion_gauss.fila_pivote+1))

    for f in eliminacion_gauss.outras_filas:
        # Cálculo coeficiente
        k = sistema[f][columna] / p

        if salida:
            print("Fila: {}, a_{}{} / a_{}{} = {}".format(f+1, f+1, columna+1, eliminacion_gauss.fila_pivote+1, columna+1, k))
        
        # Restamos a cada fila o producto do coeficiente pola fila pivote
        temp = np.copy(sistema[f])
        sistema[f] -= k * sistema[eliminacion_gauss.fila_pivote]

        if salida:
            stringify = lambda arr : " ".join([str(x) for x in arr[:-1]]) + " | " + str(arr[-1])
            print("{}  >>  {}".format(stringify(temp), stringify(sistema[f])))
    
    # Eliximos unha nova fila pivote e eliminamos a anterior da lista de outras filas
    for f in eliminacion_gauss.outras_filas:
        if sistema[f][columna] == 0:
            eliminacion_gauss.fila_pivote = f
            eliminacion_gauss.outras_filas.remove(f)
            break

    if salida:
        print_matriz(sistema, "\nSistema:", "")

# Triangulación sen pivote:
# Transforma unha matriz nunha matriz triangular superior utilizando o método de gauss descrito anteriormente
def triangulacion_sen_pivote(ecuacions, fila_pivote=0, salida=True):
    # Sistema de ecuacions sobre o que operar
    sistema = ecuacions.astype(float)
    
    # Parametros iniciais da eliminación de Gauss
    eliminacion_gauss.fila_pivote = fila_pivote
    eliminacion_gauss.outras_filas = [f for f in range(len(sistema)) if f != fila_pivote] # Filas distintas da pivote
    
    # Iterar polos elementos do triángulo iferior da matriz
    for c in range(len(ecuacions[0])):
        eliminacion_gauss(sistema, c, salida)
        if len(eliminacion_gauss.outras_filas) == 0:
            break

    return sistema

# Comproba que unha matríz é triangular superior
def comprobar_matriz_triangular(m):
    for i in range(len(m)):
        for j in range(len(m[0])):
            if i > j and m[i][j] != 0:
                return False
    return True

# Ordea unha matríz triangular superior baseandose no número de ceros que ten, deixando o maior número de ceros abaixo
def ordear_matriz_triangular(m):
    if not comprobar_matriz_triangular(m):
        raise ValueError("A matriz non é triangular superior")
    m_ = np.copy(m).tolist()
    m_.sort(key = lambda m: m[:-1].count(0))
    return np.array(m_)

# Sustitución regresiva:
# Atopa as solucións dun sistema de ecuacións lineal triangulado por sustitución regresiva
# Utiliza a función ordear_matriz_triangular() definida anteriormente
def sustitucion_regresiva(sistema):
    m = ordear_matriz_triangular(sistema)
    solucions = np.zeros(len(m))

    for i in range(len(m))[::-1]:
        a = m[i][:-1] * solucions
        solucions[i] = (m[i][-1] - sum(a)) / m[i][i]

    return solucions

# Pequena utilidade para imprimir unha lista de solucións cos seus nomes:
solucions_a_texto = lambda sol, keys, sep: sep.join(["{} = {:.6f}".format(list(keys)[i], sol[i]) for i in range(len(sol))])

### -----------------------------------------


### -----------------------------------------
#   Exercicio 1
### -----------------------------------------

# Implementar un programa que resolva o seguinte sistema de ecuacións lineais:

ecuacions = (
    "2x1 -  x2 + x3  = 3",
    "-x1 +  x2 + 2x3 = 7",
    " x1 + 2x2 - x3  = 2",
)
print("Sistema inicial:")
print("\n".join(ecuacions))

# Obtemos a matriz que representa ó sistema
ec, keys = procesar_ecuacion(*ecuacions, nomes=True)
print_matriz(ec, "\nMatriz do sistema:", "")

# Triangulamos o sistema polo método de gauss sen pivote
sistema_triangular = triangulacion_sen_pivote(ec)

# Obtemos as solucións por sustitución regresiva
sol = sustitucion_regresiva(sistema_triangular)
print("Solucións:\n", solucions_a_texto(sol, keys, "\n "))