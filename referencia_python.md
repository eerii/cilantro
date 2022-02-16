# referencia de python :snake::sparkles:
@joseko - [última versión](https://github.com/josekoalas/cilantro)

- [varios](#varios)
  - [comentarios](#comentarios)
  - [imprimir](#imprimir)
- [variables](#variables)
  - [tipos](#tipos)
  - [operadores aritméticos](#operadores-aritméticos)
  - [operadores asignación](#operadores-asignación)
- [lóxica](#lóxica)
  - [operadores lóxicos](#operadores-lóxicos)
  - [operadores de comparación](#operadores-de-comparación)
  - [bloque if](#bloque-if)
  - [bloque else](#bloque-else)
  - [bloque elif](#bloque-elif)
- [listas](#listas)
  - [tuplas](#tuplas)
  - [conversións](#conversións)
  - [seleccionar partes](#seleccionar-partes)
- [bucles](#bucles)
  - [bucles for (lista)](#bucles-for-lista)
  - [bucles for (rango)](#bucles-for-rango)
  - [bucles while](#bucles-while)
  - [continue](#continue)
  - [break](#break)
- [funcións\*](#funcións)
- [numpy\*](#numpy)
- [matplotlib\*](#matplotlib)
- [técnicas avanzadas\*](#técnicas-avanzadas)
  - [try / catch\*](#try--catch)
  - [formato avanzado\*](#formato-avanzado)
  - [programación funcional\*](#programación-funcional)
  - [lectura e escritura de archivos\*](#lectura-e-escritura-de-archivos)
- [outros paquetes útiles\*](#outros-paquetes-útiles)
  - [pandas\*](#pandas)
  - [uncertainties\*](#uncertainties)
  - [axustes (polyfit e curvefit)\*](#axustes-polyfit-e-curvefit)

_* : en progreso_


## varios

### comentarios

```python
# comentarios
```

### imprimir

```python
# texto
print("uwu")
> uwu

# números
print(3.14)
> 3.14

# variables
a = 3
print(a)
> 3

# varias cousas
print(3, "hola", False)
> 3 hola False

# con formato (insertar nt("{:.2f}".format(3.141519))
> 3.14
```


## variables

```python
# declaración
# nome = valor
x = 3
```

### tipos

```python
# tipos básicos
numero = 1 # int
decimal = 3.14 # float
complexo = 0+1j # complex
texto = "hola" # str
condicion = True # bool
```

```python
# obter o tipo
print(type(3))
> int
```

```python
# diferencias entre tipos e convertir entre eles
x = str(3)    # x será un texto co valor "3"
y = int(3)    # y será un número enteiro co valor 3
z = float(3)  # z será un número decimal co valor 3.0
```

### operadores aritméticos

```python
a + b # suma
a - b # resta
a * b # multiplicación
a / b # división
a % b # módulo da división
a ** b # 'a' elevado a 'b'
```

**exemplo:**

```python
# calcular o cadrado dun número
x = 4
y = x ** 2
print(y)
> 16
```

### operadores asignación

```python
a = b # asigna a 'a' o valor de 'b'
a += b # equivalente a "a = a + b", suma o valor de 'b' a 'a' e garda o resultado en 'a'
# tamén hai a -= b, a *= b, a /= b, ...
```


## lóxica

```python
# tipo bool
a = True # verdadeiro, equivalente a 1
b = False # false, equivalente a 0
```

### operadores lóxicos

```python
# and : só é verdadeiro se ambos son verdadeiros
True and True = True
True and False = False
False and False = False
```

```python
# or : é verdadeiro se algún é verdadeiro
True or True = True
True or False = True
False or False = False
```

```python
# not : invirte o valor
not True = False
not False = True
```

### operadores de comparación

```python
a == b # igual : verdadeiro se a é igual a b
a != b # non igual : verdadeiro se a é distinto de b
a > b # maior : verdadeiro se a é maior que b
a < b # menor : verdadeiro se a é menor que b
a >= b # maior ou igual
a <= b # menor ou igual
```

**exemplo:**

```python
a = 3
b = 5
c = 10

print(b > a)
> True

print(c == 2 * b and a != 4)
> True

print(a >= 6 or b + c == 17)
> False

print(not False)
> True
```

### bloque if

```python
if condicion:
  # se a condición é verdadeira fai isto
```

**indentación:**

```python
# o bloque inclue o que esté no seu nivel de indentación
if condicion:
  # fai isto
  # e isto
# isto faise sempre, independentemente da condición
```

**exemplo:**

```python
a = -2
if a >= 0:
  # o bloque comeza aquí
  print("a é positivo")
  # e remata aquí

a += 5
if a == 3:
  print("a é 3!")

> a é 3!
# o primeiro bloque non se executa porque 'a' é negativo
# logo súmaselle 5 ó valor de 'a', que queda en 3 (podes facer 'print(a)' xusto despois para comprobalo)
# o segundo bloque sí se executa porque o valor de 'a' é 3
# mira ben onde comezan e rematan os bloques, está marcado pola indentación
```

**múltiples bloques:**

```python
if condicion_1:
  if condicion_2:
    if condicion_3:
      # isto faise se as 3 condicións son verdadeiras
```

```python
if condicion_1:
  if condicion_2:
    # isto faise se as condicións 1 e 2 son verdadeiras, *antes* de comprobar se a terceira o é
    if condicion_3:
      # ...
    # isto tamén se fai se as condicións 1 e 2 son verdadeiras, pero *despóis* de comprobar a terceira
    # non influe se a terceira é verdadeira o non, pero o código de aquí executarase despois do anterior
    # de novo, a indentación é moi importante para saber qué bloque fai qué
```

**exemplo:**

```python
if x > 0:
  if y > 0:
    print("primeiro cuadrante")
    if x**2 + y**2 == 1:
      print("parte do círculo unidade no primeiro cuadrante")
```

### bloque else

```python
if condicion:
  # fai isto se se cumpre a condición
else:
  # fai isto se non se cumpre
```

```python
# para saber con qué if vai un else, hai que mirar a indentación
if c_1:
  if c_2:
    #...
  else: # corresponde ó if 2
    #...
else: # corresponde ó if 1
  #...
```

### bloque elif

```python
if c_1:
  # cúmprese a condición 1
elif c_2:
  # non se cumpre a condición 1 pero se cumpre a condición 2
else:
  # non se cumpre a condición 1 nin a 2

# nota: non é obligatorio ter sempre as tres, podes usar so if, if e elif, if e else ou as tres (nunca elif ou else sós)
```

**multiples elif:**

```python
if c_1:
  # cúmprese c_1
elif c_2:
  # cúmprese c_2, non se cumpre c_1
elif c_3:
  # cúmprese c_3, non se cumpren c_1 nin c_2
elif c_4:
  # cúmprese c_4, non se cumpren c_1, c_2 nin c_3
else:
  # non se cumpre ningunha
```

**exemplo:**

```python
a == 4
if a < 3:
  print("a é menor que 3")
elif a > 3:
  print("a é maior que 3")
else:
  print("a é 3")

> a é maior que 3
```

## listas

```python
l = [1, 2, 3] # entre corchetes, separados por comas
l = [a, b, c] # copia o valor das variables
l = [1, "uwu", True] # pode facerse, pero non é recomendable, o mellor e ter listas de elementos do mesmo tipo
```

**número de elementos:**

```python
l = [1, 2, 3]
n = len(l)
print(n)
> 3
```

**acceder a un elemento:**

```python
l = [2.4, 5.1, 6.0]
print(l[0]) # l[i] devolve o valor da lista l na posición i
> 2.4

# importante: a posición comeza a contar dende cero
# unha lista de 9 elementos terá posicións dende 0 ata 8
# utilizar unha posición fora de rango da erro (se a = [5, 4], facer a[9] da un erro)
```

**cambiar o valor dun elemento:**

```python
l = [2, 8, 9]
l[1] = 4 # modificamos o elemento na posición 1, que é o segundo (ó principio é algo lioso)
print(l) # podense imprimir listas igual que outras variables
> [2, 4, 9]
```

**engadir elementos a unha lista:**

```python
l = ["amarillo", "azul", "añil"]

# engadir ó final
l.append("ambar")
print(l)
> ["amarillo", "azul", "añil", "ambar"]

# engadir nunha posición concreta
l.insert(1, "aguamarina")
print(l)
> ["amarillo", "aguamarina", "azul", "añil", "ambar"] # inserta o elemento nese índice (contando desde cero)
```

**eliminar elementos dunha lista:**

```python
l = ["verde", "vermello", "violeta"]

# eliminar por valor
l.remove("vermello")
print(l)
> ["verde", "violeta"]

# eliminar por índice
l.pop(0)
print(l)
> ["violeta"]

# eliminar todos os elementos
l.clear()
print(l)
> []
```

**unir dúas listas:**

```python
a = [1, 2, 3]
b = [4, 5, 6]
c = a + b
print(c)
> [1, 2, 3, 4, 5, 6]
```

### tuplas

```python
# case nunca vas utilizar esto, máis o inclúo por completitude
# unha tupla é unha lista que *non* pode ser modificada (engadir, quitar ou cambiar elementos)
t = (1, 2, 3)
# t.append(4) da erro
```

### conversións

```python
t = (1, 2, 3)
l = list(t) # l é unha lista cos mesmos contidos ca tupla
a = tuple(l) # l é unha tupla cos mesmos contidos ca lista
```

### seleccionar partes

```python
lista = ["a", "b", "c", "d", "e", "f"]

lista[i] # seleccionar o elemento no índice i dunha lista
print(lista[2])
> c

lista[a:b] # devolve unha lista cos elementos de a ata b (sen incluír b)
print(lista[1:4])
> ["b", "c", "d"]

lista[a:] # se non se especifica, dende ese elemento ata ó final
print(lista[3:])
> ["d", "e", "f"]

lista[:b] # o mesmo, pero ata ese elemento sen incluílo
print(lista[:2])
> ["a", "b"]

print(lista[:-1]) # índice negativo, comeza por detrás, neste caso, elimina o último elemento
> ["a", "b", "c", "d", "e"]

print(lista[:]) # imprime toda a lista
> ["a", "b", "c", "d", "e", "f"]
```


## bucles

**comparación dos distintos tipos de bucles (exemplo):**

```python
# bucle for (range-based)
for elemento in lista:
  print(elemento)

# bucle for (iterator-based)
for indice in range(len(lista)):
  print(lista[i])

# bucle while
i = 0
while i < len(lista):
  print(lista[i])
  i += 
  
# funcion map (volveremos a el despois, insertar referencia)
map(funcion, lista)
```

### bucles for (lista)

```python
for elemento in lista:
  # por cada elemento que haxa na lista, executar este código
  # además, garda o valor do elemento co que estamos traballando na variable 'elemento'
  # así que podemos utilizar ese valor no bucle, incluso modificalo
  # igual co bloque if, está indentado
```

**exemplo:**

```python
# para cada numero da lista, aumentar o seu valor nunha unidade
l = [1, 2, 3]
for numero in l:
  numero += 1
print(l)
> [2, 3, 4]
```

**exemplo:**

```python
# se o valor non é "owo", imprimir en pantalla
l = ["uwu", "owo", ":D", "^-^"]
for texto in l:
  if texto != "owo":
    print(texto)
> uwu
> :D
> ^-^
# vemos que podemos combinar perfectamente os bloques condicionais e os bucles
# nota: agora aparecerán en distintas líneas xa que estamos a chamar a función print para cada texto, varias veces
```

### bucles for (rango)

**range:**

```python
range(a) # crea unha lista* de números enteiros de 0 ata a-1 (así ten lonxitude a) -> [0, a)
range(a, b) # crea unha lista* de números enteiros de a ata b-1 -> [a, b)
# pode chamarse de ambas maneiras, pero neste caso utilizaremos a primeira
len(lista) # devolve o número de elementos da lista
# polo tanto:
range(len(lista)) # crea unha lista* de 0 ata o número de elementos da lista menos 1
# isto é perfecto, xa que é unha lista de índices da lista, sen pasarse (recorda que os índices comenzan en 0)

# * nota: non é técnicamente unha lista, pero para o uso nos bucles é o mesmo
# pódese convertir a unha lista tradicional facendo:
l = list(range(a))
```

**exemplo:**

```python
l = [4, 2, 9, 0]
n = len(l) # 4
r = range(len(l))
print(list(r)) # vou a convertilo nunha lista para imprimilo en pantalla, pero logo non vai facer falta co bucle
> [0, 1, 2, 3]
```

**bucle:**

```python
for i in range(len(lista)):
  # por cada índice da lista, executa este código
  # nesta ocasión, en vez de ter acceso a cada elemento da lista, tes acceso ó indice desta iteración
  # podes obter o elemento asociado ó indice facendo lista[i]
```

**exemplo:**

```python
l = [4, 6, 7, 10]
for i in range(len(l)):
  if i % 2 == 0: # uso do operador módulo, neste caso para probar se o número é par
    print("o número", l[i], "é par, e está no índice", i)
> o número 4 é par e está no índice 0
> o número 6 é par e está no índice 1
> o número 10 é par e está no índice 3
```

**exemplo:**

```python
# na miña opinión sempre que se poida é preferible utilizar o for para listas xa que queda máis claro
# sen embargo, nalgúns casos non é posible, por exemplo, cando tes dúas listas
x = [0, 1, 2, 3, 4, 5]
y = [-3, -1, 1, 3, 5]
for i in range(len(x)):
  print("coordeada ({}, {})".format(x[i], y[i])) # ver a sintaxe de format no apartado de print
> coordeada (0, -3)
> coordeada (1, -1)
> ...
# nota, este exemplo só funciona se as dúas listas teñen o mesmo tamaño
```

### bucles while

```python
while condicion:
  # mentres se cumpra a condición, repite isto
```

**exemplo:**

```python
i = 1
while i < 8:
  print("o valor de i é", i)
  i *= 2
# este bucle repetirase 3 veces
# na primeira iteración, i valerá 0, imprimirase en pantalla, e sumarase un
# cando i chegue a 8, o bucle deixará de repetirse
> o valor de i é 1
> o valor de i é 2
> o valor de i é 4
```

**similitudes con for:**

```python
# un bucle while pode facer o mesmo cun bucle for, pero a sintaxe é algo máis larga
lista = [2, 5, 10]
i = 0
while i < range(len(lista)):
  print(lista[i])
  i += 1

# equivalente a:
for i in range(len(lista)):
  print(lista[i])

# e tamén a:
for elemento in lista:
  print(elemento)
```

### continue

```python
lista = [3.0, 4.3, 0.0, 7.9, 0.0, 1.2]
for a in lista:
  if a == 0.0:
    continue
  print(round(1.0/a, 2))

# a palabra clave continue fai que o bucle salte á seguinte iteración
# todo o código despóis non se executa
# nesta caso, se o valor da lista é 0, continuamos, polo que non se imprimirá en pantalla
# nota: round redondea ó número de decimáis que indiques

> 0.33
> 0.23
> 0.13
> 0.83
```

### break

```python
lista = [3.0, 4.3, 0.0, 7.9, 0.0, 1.2]
for a in lista:
  if a == 0.0:
    break
  print(round(1.0/a, 2))

# neste caso, a palabra clave break detén a execución do bucle por completo
# o programa deixa de facer o bucle e continúa despóis, da igual que queden máis elementos
# nesta caso parará no terceiro elemento

> 0.33
> 0.23
```

**while true:**

```python
# case sempre é recomendable utilizar for para traballar con listas ou calqueira tipo de repetición
# sen embargo, hai unha aplicación útil para while

while True:
  # ...

# este bucle executarase para sempre, e a única maneira de paralo é utilizando 'break'
# é un patrón moi utilizado na creación de aplicacións ou videoxogos
```

**exemplo:**

```python
# queremos crear un xogo
# o programa consta de tres partes (todas as funcións son inventadas)

# inicio
iniciar_xogo()

# bucle principal
while True:
  obter_teclado()
  mover_xogador()
  actualizar_pantalla()
  # ...
  if pechou_ventana:
    break

# finalización
limpar_recursos()
finalizar_xogo()

# todo o xogo despóis do inicio transcurre no bucle principal
# este repetirase indefinidamente ata que o xogador peche a ventana do xogo
# neste momento, usamos 'break' para parar o xogo e saír do bucle
```


## funcións*



## numpy*



## matplotlib*



## técnicas avanzadas*

### try / catch*

### formato avanzado*

### programación funcional*

### lectura e escritura de archivos*



## outros paquetes útiles*

### pandas*

### uncertainties*

### axustes (polyfit e curvefit)*