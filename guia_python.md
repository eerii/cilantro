# Como aprender Python sen morrer no intento 🐍
~ joseko

- [Como aprender Python sen morrer no intento 🐍](#como-aprender-python-sen-morrer-no-intento-)
  - [Antes de comezar](#antes-de-comezar)
    - [Comentarios](#comentarios)
    - [Imprimir calqueira cousa](#imprimir-calqueira-cousa)
  - [Variables](#variables)
    - [Tipos básicos](#tipos-básicos)
    - [Problemas entre tipos](#problemas-entre-tipos)
    - [Asignar variables](#asignar-variables)
    - [Operadores aritméticos](#operadores-aritméticos)
  - [Lóxica](#lóxica)
    - [Operadores lóxicos](#operadores-lóxicos)
    - [Operadores de comparación](#operadores-de-comparación)
    - [Bloque if](#bloque-if)
    - [Indentación](#indentación)
    - [Bloque else](#bloque-else)
    - [Bloque elif](#bloque-elif)
  - [Funcións](#funcións)
    - [Argumentos](#argumentos)

## Antes de comezar

### Comentarios

```python
# esto é un comentario
a = 3 # pódense poñer onde queiras con un '#'
print(a) # é moi importante documentar o código para saber o que fai
```

### Imprimir calqueira cousa

É fundamental poder ver o que está ocurrindo dentro do programa. Hai varias maneiras de facer iso, pero a que máis vamos a utilizar é `print`. Esta función imprime o que lle poñas dentro na consola, xa sexa o valor dunha [variable](#variables), un número ou algo máis complexo.

Coma calqueira [función](#funcións) chámase escribindo o nome e abrindo parénteses. Dentro escribes os [argumentos](#argumentos), separados por comas. Por exemplo:

```python
print("uwu")
```
```python
>> uwu
```

Nota: de aquí en adiante utilizarei o símbolo `>>` para representar o que imprime a consola cando executas o código superior.

```python
print(3.14) # números
print("uwu") # texto
print(a) # variables
print("cosas", 10, b) # varias cousas, sepáranse por comas
```

## Variables

As variables son o espacio onde gardas datos. Decáranse da seguinte maneira:

```python
# nome = valor
x = 3
```

### Tipos básicos

Poden ter varios tipos, pero en `python` non é obligatorio especificalo antes de crear unha variable, simplemente teñen o tipo do valor que lle asignas:

```python
numero = 1 # int
decimal = 3.14 # float
complexo = 0+1j # complex
texto = "hola" # str
condicion = True # bool
```

Podes obter o tipo dunha variable utilizando a función `type`:

```python
print(type(3))
```
```python
>> int
```

Se te fixas chamamos directamente á función `print` co resultado da función `type`. Isto é totalmente válido e aforra moito tempo en ocasións.

### Problemas entre tipos

Os valores `3`, `3.0` e `"3"` son distintos: `3` é un número enteiro (`int`), `3.0` é un número decimal (`float`), e `"3"` é un texto có caracter 3. Non darse conta da diferencia pode dar pé a quebraderos de cabeza, xa que se intentas sumar un número con un texto, o programa terá un erro.

Para evitar isto, fixate ben en como declaras as variables, e se tes dudas sempre podes utilizar `type()` para ver o tipo que ten unha variable nun momento dado.

Se queres convertir dun tipo a outro podes facer _casting_. Isto faise poñendo o nome oficial do tipo e o valor a convertir entre parénteses. Por exemplo:

```python
x = str(3)    # x será un texto co valor "3"
y = int(3)    # y será un número enteiro co valor 3
z = float(3)  # z será un número decimal co valor 3.0
```

### Asignar variables

Podes asignar unha variable (darlle valor) as veces que queiras, incluso a tipos diferentes (aínda que para comezar é recomendable non mezclar tipos para evitar confusións).

```python
a = 3
b = 4

a = 10 # agora a vale 10
b = a + 5 # agora b vale 10+5=15

a = "hola" # pode facerse pero non é moi recomendable
```

Cando asignas variables podes utllizar o valor de outra variable, como fixemos na penúltima liña, e operacións entre elas.

Tamén podes utilizar o valor da mesma variable, por exemplo, `a = a + 1`, que aumentará o valor de `a` nunha unidade.

### Operadores aritméticos

En `python` hai varios tipos de operadores. Comezaremos cos aritméticos:

```python
a + b # suma
a - b # resta
a * b # multiplicación
a / b # división
a % b # módulo da división
a ** b # 'a' elevado a 'b'
```

Tamén temos o **operador asignación**, que é `=`, e asigna o valor da dereita á variable da esquerda, como xa vimos. Ademáis, hai uns operadores moi útiles que mezclan os aritméticos e o operador asignación, como:

```python
a += b # esto é equivamente a 'a = a + b'
```

Podes utilizar a suma, a resta ou calqueira dos outros operadores seguido do signo igual. Esto o que fai e sumarlle ó valor de a o que poñas na man dereita. Por exemplo, incrementar unha variable nunha unidade `a = a + 1` pódese resumir por `a += 1` (aínda que ambas son equivalentes).

## Lóxica

Gardar números e outras cousas non nos serve de moito se non temos qué facer con eles. Para iso introduciremos a **lóxica booleana**, isto é, que se basa en valores verdadeiros e falsos. O tipo `bool` pode tomar dous valores:

```python
a = True # verdadeiro, equivalente a 1
b = False # false, equivalente a 0
```

### Operadores lóxicos

Temos tres operadores lóxicos que modifican unha condición:

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

### Operadores de comparación

Para comparar duás variables ou valores aparecen os operadores de comparación. Estes **sempre** devolven un resultado `bool`, cun valor ou verdadeiro ou falso.

```python
a == b # igual : verdadeiro se a é igual a b
a != b # non igual : verdadeiro se a é distinto de b
a > b # maior : verdadeiro se a é maior que b
a < b # menor : verdadeiro se a é menor que b
a >= b # maior ou igual
a <= b # menor ou igual
```

Ademáis, podes encadear varias comparacións utilizando os operadores lóxicos:

```python
a != b and b > 0 # a é distinto de b e b é maior que 0
not a == b # a non é igual a b (esto é equivalente a: a != b)
a > b or c > d # a maior que b ou c maior que d
```

### Bloque if

Estaraste a preguntar para que serve toda esta lóxica. Podemos utilizala para **controlar** o programa.

O bloque `if` executara o código no seu interior se a condición indicada se cumpre.

```python
if condicion:
  # executa isto
```

Por _condición_ referímonos a un valor verdadeiro ou falso, que normalmente ven dado por un dos operadoradores de comparación que xa vimos. O código que execute pode ser **calqueira cousa**. Vamos facer un exemplo simple con `print`.

```python
if a > 3:
  print("a é maior que 3")
```

Debemos fixarnos en dous detalles. Primeiro, a sintaxe do bloque `if` é `if condicion:`, especial énfase nos dous puntos. Isto indica que remata a condición e comeza o código a executar se esta se cumple.

### Indentación

O segundo é a **indentación**. Noutras linguaxes de programación para separar código utilízanse os corchetes `{}`, sen embargo, `python` utiliza os espazos. Calqueira editor de `python` decente o fará automáticamente, pero é moi importante indentar o código. Todo o código que esté ó mesmo nivel de indentación será parte do mesmo bloque.

Vamos a ver un exemplo simple con `if`. Como sabe o programa qué código ten que executar o bloque if, e onde continúa o programa normal? Utilizando indentación:

```python
a = 5

if a > 3:
  print("esto se executa se a é maior que 3")

print("esto se executa sempre")
```

Se te fixas, díante do primeiro `print` hai dous espazos, que indican que está no seguinte nivel (sempre se usan dous espazos). O segundo `print` volve a estar no nivel base do programa.

Dentro do bloque `if` podemos poñer **calqueira** código, incluído outro bloque `if`:

```python
if a > 3:
  if b == 5:
    if c != 4:
      print("chegaches aquí!")

# nota: este código non é moi elegante, pero está así para ilustrar
# os niveis de indentanción. un código equivalente é:
if a > 3 and b == 5 and c != 4:
  print("chegaches aquí!")
```

Podes observar que cada bloque if aumenta a indentación en dous espazos. Isto fai que podamos poñer condicións anidadas. Ademáis, tamén podemos facer o seguinte:

```python
if a > 3:
  if b == 5:
    print("hola")
  print("adeus")
```

Neste caso, se `a > 3`, primeiro comprobarase se `b == 5`. Se este é o caso, imprimirá "hola" na consola. Independentemente do que resulte o segundo `if`, logo imprimirá "adeus". Isto é así porque adeus está no nivel do primeiro `if`, polo que non depende do segundo para nada, como podemos ver a continuación:

```python
if a > 3:
  #...
  print("adeus")
```

É moi importante adoptar esta mentalidade de **bloques** indentados, e practicar para comprender o que está pasando. Mira o seguinte exemplo, máis complexo, pero cos mesmos bloques básicos (non te centres demasiado nas funcións, simplemente na maneira que a indentación é importante):

```python
# movemento_x e movemento_y son variables
# mover_dereita() e comprobar_terra() son funcións arbitrarias
# comprobar_terra() devolve un valor verdadeiro ou falso

if movemento_x > 0: # vai cara a dereita
  if movemento_y == 0: # non se move na horizontal
    mover_dereita()
  if movemento_y > 0: # móvese cara arriba na horizontal
    saltar()
    print("estás no aire!") # podes poñer varias liñas debaixo dun if
  if movemento_y < 0: # móvese cara abaixo
    terra = comprobar_terra()
    if (terra):
      print("chocaches co chan!")
      movemento_y = 0 # deixas de moverte cara abaixo
```

### Bloque else

Ademáis do bloque `if`, temos o seu compañeire, `else`. A sintaxe é como segue:

```python
if a > 3:
  print("a é maior que 3")
else:
  print("a non é maior que 3")
```

Se queremos cubrir o caso no que a condición **non é certa** podemos utilizar un `else` despoís de todo o código do `if`. Presta atención á indentación, o bloque `else` colócase á mesma altura que o `if` ó que complementa, e o seu código ten unha indentación máis, igual que o código do `if`.

### Bloque elif

Nalgunas ocasións queres ter un maior control no que o programa fará dependendo da condición indicada. Para iso está `elif`. Despóis dun `if` podes colocar este bloque **con outra condición**. Se _todo o anterior_ é falso, pero a condición é verdadeira, entón ese bloque executarase. Vamos velo mellor cun exemplo:

```python
if a % 2 == 0: # utlizando a operación de módulo da división
  print("a é par")
elif a > 2:
  print("a é impar, e ademáis maior que 2")
elif a > 0:
  print("a é impar, menor ou igual a 2, e maior que cero")
```

Como ves as condicións vanse acumulando, e cada vez é mais concreto. Tamén pode incluirse un `else` ó final para cubrir todas as opcións restantes (mentres que pode haber varios `elif`, só pode haber un `else` xa que este xa cubre todas as condicións que queden, e o `else` sempre debe ir ó final):

```python
if a > 3:
  print("a é maior que 3")
elif a < 3:
  print("a é menor que 3")
else:
  print("a é 3")
```

## Funcións

### Argumentos

