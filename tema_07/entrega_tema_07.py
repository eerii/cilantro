# Ecuación unidimensional de difusión - Tema 7
# José Pazos Pérez - G3

# Índice
#     - [14]  Importacións
#     - [22]  Preparación de matplotlib
#     - [36]  Valores iniciais
#     - [56]  Coeficientes
#     - [110] Solución da ecuación de difusión
#     - [223] Funcións auxiliares da representación gráfica
#     - [494] Execución da aplicación

# ------------------------------------------------------------------
# Importacións
# ------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button, RadioButtons
import matplotlib

# ------------------------------------------------------------------
# Preparación de matplotlib
# ------------------------------------------------------------------

# Eixos
fig, ax = plt.subplots(figsize=(9, 6))
fig.subplots_adjust(bottom=0.2, right=0.8, top=0.95, left=0.08)

# Modo interactivo
plt.ion()

# Rotación de cores
matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler("color", ["royalblue", "mediumseagreen", "gold", "orange", "tomato", "hotpink", "mediumorchid"])

# ------------------------------------------------------------------
# Valores iniciais
# ------------------------------------------------------------------

# Iteracions temporais
it = 2000
# Parámetros da discretización
dt = 0.1
dx = 0.5
alfa = 0.1
N = 50
# Estabilidade
s = alfa * (dt/dx**2)
# Eixo temporal
t = np.linspace(0, dt*N, N+1)
# Valor inicial da temperatura
Ti = np.random.random(N+1) * 10
# Condicións de fronteira
cf = [0, 10]

# ------------------------------------------------------------------
# Coeficientes de x e t para os distintos métodos 
# Actualízase automáticamente cando cambiamos s
# ------------------------------------------------------------------
coeficientes = lambda: {
    "FTCS": ({
        -1: s,
        0: 1 - 2*s,
        1: s
    }, {}),

    "3 niveis temporais": ({
        -1: 2*s/3,
        0: (4/3)*(1 - s),
        1: 2*s/3
    }, {
        -1: -1/3
    }),

    "5 veciños espaciais": ({
        -2: -s/12,
        -1: 4*s/3,
        0: 1 - 5*s/2,
        1: 4*s/3,
        2: -s/12
    }, {}),

    "DuFort-Frankel": ({
        -1: (2*s)/(1 + 2*s),
        0: 0,
        1: (2*s)/(1 + 2*s)
    }, {
        -1: (1 - 2*s)/(1 + 2*s)
    }),

    "[Impl] FTCS": ({
        -1: -s,
        0: 1 + 2*s,
        1: -s
    }, {}),

    "[Impl] Crank-Nicolson": ({
        -1: -s/2,
        0: 1 + s,
        1: -s/2
    }, {
        -1: s/2,
        0: 1 -s,
        1: s/2
    }),
}

metodo = "FTCS"

# ------------------------------------------------------------------
# Solución da ecuación de difusión
# ------------------------------------------------------------------

def representar():
    # Función temperatura
    T = Ti.copy()

    # Condicións de frontera de Dirichlet
    if isinstance(cf[0], int) or isinstance(cf[0], float):
        T[0] = cf[0]
    if isinstance(cf[1], int) or isinstance(cf[1], float):
        T[N] = cf[1]

    # Coeficientes
    cx, ct = coeficientes()[metodo]

    # Dimensión do método (1 para 3 coeficientes, 2 para 5...)
    x_n = (len(cx) >> 1)

    # ---

    # Método implícito
    implicito = metodo[0:6] == "[Impl]"
    C = None
    if implicito:
        # Matriz de coeficientes A
        A = np.zeros((N+x_n, N+x_n))
        for i in range(x_n, N):
            for c in cx:
                A[i, i+c] = cx[c]
        for i in range(x_n):
            A[i, i] = 1
            A[N+x_n-i-1, N+x_n-i-1] = 1

        if len(ct) == 0:
            # Matriz inversa
            C = np.linalg.inv(A)
        else:
            # Matriz de coeficientes B
            B = np.zeros((N+x_n, N+x_n))
            for i in range(x_n, N):
                for c in ct:
                    B[i, i+c] = ct[c]
            for i in range(x_n):
                B[i, i] = 1
                B[N+x_n-i-1, N+x_n-i-1] = 1
            
            # Combinación de ambas matrices
            Bi = np.linalg.inv(B)
            C = np.linalg.inv(np.dot(Bi, A))

        T = np.vstack([T])
    # Método explícito
    else:
        # Engadimos valores auxiliares ós lados de T
        T = np.concatenate(([T[0]] * (x_n-1), T, [T[N]] * (x_n-1)))

        # Crear varios arrays para almacear os valores pasados no tempo (0 é o actual, 1 é o anterior...)
        T = np.vstack([T] * (len(ct)+1))

    # Limpar a representación anterior
    ax.clear()

    # ---

    # Bucle temporal
    for i in range(it):
        # Cálculo do seguinte vector sen cambiar as condiciones de frontera
        # Método implícito
        if implicito:
            T[0] = np.dot(C, T[0])
        # Método explícito
        else:
            # Suma a parte pertinente ós coeficientes temporais e os coeficientes espaciais
            T[0, x_n:-x_n] = sum([T[0, x_n+i : -x_n+i or None] * coef for i, coef in cx.items()]) + sum([T[-i, x_n:-x_n] * coef for i, coef in ct.items()])

        # Condicions de frontera de fluxo nulo
        if cf[0] == "FN":
            T[0, 0:x_n] = T[0, x_n+1]
        if cf[1] == "FN":
            T[0, -x_n:] = T[0, -x_n-1]

        # Condicions de frontera variables
        if cf[0] == "SIN":
            T[0, 0:x_n] = np.sin(0.5*i*dt)
        if cf[1] == "SIN":
            T[0, -x_n:] = np.sin(0.5*i*dt)

        # Propagar os cambios de atrás cara adiante (só explícito)
        if not implicito:
            for j in range(len(ct), 0, -1):
                T[j] = T[j-1].copy()

        # Representación cada varias iteracións
        if i % (it // 20) == 0:
            # 2D
            if button_2d3d.button.label.get_text() == "2D":
                ax.plot(t, T[0, x_n-1:-x_n+1 or None])
            # 3D
            else:
                Tp = T.copy()
                ax.plot(t, [i]*len(t), Tp[0, x_n-1:-x_n+1 or None])

    # Actualizar a vista
    if button_2d3d.button.label.get_text() == "2D":
        ax.relim()
        ax.autoscale_view()

# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# Funcións auxiliares para a representación gráfica
# Botóns, caixas de texto...
# ------------------------------------------------------------------

def textbox_expresion():
    def submit(expr):
        global Ti
        Ti = eval(expr)
        representar()

    ax_box = fig.add_axes([0.08, 0.1, 0.72, 0.05])
    textbox_expresion.box = TextBox(ax_box, "T", textalignment="center", initial="np.random.random(N+1) * 10")
    textbox_expresion.box.on_submit(submit)

def textbox_t0():
    def submit(expr):
        global cf
        cf[0] = "FN" if button_t0.button.label.get_text() == "FN" else eval(expr)
        representar()

    ax_box = fig.add_axes([0.08, 0.02, 0.05, 0.05])
    textbox_t0.box = TextBox(ax_box, "T[0] ", textalignment="center", initial=str(cf[0]))
    textbox_t0.box.on_submit(submit)

def textbox_tn():
    def submit(expr):
        global cf
        cf[1] = "FN" if button_tn.button.label.get_text() == "FN" else eval(expr)
        representar()

    ax_box = fig.add_axes([0.22, 0.02, 0.05, 0.05])
    textbox_tn.box = TextBox(ax_box, "T[N] ", textalignment="center", initial=str(cf[1]))
    textbox_tn.box.on_submit(submit)

def button_t0():
    def click(event):
        global cf
        if cf[0] == "FN": # De fluxo nulo a condicións de Dirichlet
            button_t0.button.label.set_text("CF")
            textbox_t0.box.set_val(button_t0.previous_text)
        else: # De condicións de Dirichlet a fluxo nulo
            button_t0.button.label.set_text("FN")
            button_t0.previous_text = textbox_t0.box.text
            textbox_t0.box.set_val("")

    ax_box = fig.add_axes([0.13, 0.02, 0.04, 0.05])
    button_t0.button = Button(ax_box, "CF")
    button_t0.button.on_clicked(click)

def button_tn():
    def click(event):
        global cf
        if cf[1] == "FN": # De fluxo nulo a condicións de Dirichlet
            button_tn.button.label.set_text("CF")
            textbox_tn.box.set_val(button_tn.previous_text)
        else: # De condicións de Dirichlet a fluxo nulo
            button_tn.button.label.set_text("FN")
            button_tn.previous_text = textbox_tn.box.text
            textbox_tn.box.set_val("")

    ax_box = fig.add_axes([0.27, 0.02, 0.04, 0.05])
    button_tn.button = Button(ax_box, "CF")
    button_tn.button.on_clicked(click)

def textbox_dt():
    def submit(expr):
        global dt, t, s, Ti
        dt = eval(expr)
        s = alfa * (dt/dx**2)
        t = np.linspace(0, dt*N, N+1)
        Ti = eval(textbox_expresion.box.text)
        representar()

    ax_box = fig.add_axes([0.345, 0.02, 0.07, 0.05])
    textbox_dt.box = TextBox(ax_box, "dt ", textalignment="center", initial=str(dt))
    textbox_dt.box.on_submit(submit)

def textbox_dx():
    def submit(expr):
        global dx, s
        dt = eval(expr)
        s = alfa * (dt/dx**2)
        representar()

    ax_box = fig.add_axes([0.45, 0.02, 0.07, 0.05])
    textbox_dx.box = TextBox(ax_box, "dx ", textalignment="center", initial=str(dx))
    textbox_dx.box.on_submit(submit)

def textbox_alfa():
    def submit(expr):
        global alfa, s
        alfa = eval(expr)
        s = alfa * (dt/dx**2)
        representar()

    ax_box = fig.add_axes([0.54, 0.02, 0.07, 0.05])
    textbox_alfa.box = TextBox(ax_box, "$\\alpha$ ", textalignment="center", initial=str(alfa))
    textbox_alfa.box.on_submit(submit)

def textbox_N():
    def submit(expr):
        global N, t, Ti
        N = eval(expr)
        t = np.linspace(0, dt*N, N+1)
        Ti = eval(textbox_expresion.box.text)
        representar()

    ax_box = fig.add_axes([0.635, 0.02, 0.07, 0.05])
    textbox_N.box = TextBox(ax_box, "N ", textalignment="center", initial=str(N))
    textbox_N.box.on_submit(submit)

def textbox_it():
    def submit(expr):
        global it
        it = eval(expr)
        representar()

    ax_box = fig.add_axes([0.73, 0.02, 0.07, 0.05])
    textbox_N.box = TextBox(ax_box, "it ", textalignment="center", initial=str(it))
    textbox_N.box.on_submit(submit)

def seleccionar_metodo():
    def click(label):
        global metodo
        metodo = label
        representar()

    m = [k for k, v in coeficientes().items()]
    ax_box = fig.add_axes([0.82, 0.7, 0.16, 0.25])

    seleccionar_metodo.buttons = RadioButtons(ax_box, m, active=0, activecolor="royalblue")
    seleccionar_metodo.buttons.on_clicked(click)

    rpos = ax_box.get_position().get_points()
    fh = fig.get_figheight()
    fw = fig.get_figwidth()
    rscale = (rpos[:,1].ptp() / rpos[:,0].ptp()) * (fh / fw)

    for c in seleccionar_metodo.buttons.circles:
        c.height /= rscale

def cambiar_valor_box(b, t):
    if b.box.text != t:
        b.box.set_val(t)

def cambiar_valor_button(b, t):
    if b.button.label.get_text() != t:
        b.button.label.set_text(t)

def seleccionar_exercicio():
    def click(label):
        if label == "Exercicio 1ab":
            cambiar_valor_box(textbox_expresion, "np.random.random(N+1) * 10")
            cambiar_valor_button(button_t0, "CF")
            cambiar_valor_button(button_tn, "CF")
            cambiar_valor_box(textbox_t0, "0")
            cambiar_valor_box(textbox_tn, "10")
            seleccionar_metodo.buttons.set_active(0)
        elif label == "Exercicio 1c":
            cambiar_valor_box(textbox_expresion, "np.random.random(N+1) - 0.5")
            cambiar_valor_button(button_t0, "CF")
            cambiar_valor_button(button_tn, "CF")
            cambiar_valor_box(textbox_t0, "0")
            cambiar_valor_box(textbox_tn, "'SIN'")
            seleccionar_metodo.buttons.set_active(0)
        elif label == "Exercicio 1d":
            cambiar_valor_box(textbox_expresion, "np.random.random(N+1) * 10")
            cambiar_valor_button(button_t0, "FN")
            cambiar_valor_button(button_tn, "FN")
            cambiar_valor_box(textbox_t0, "")
            cambiar_valor_box(textbox_tn, "")
            seleccionar_metodo.buttons.set_active(0)
        else:
            if label[-1] == "a":
                cambiar_valor_button(button_t0, "CF")
                cambiar_valor_button(button_tn, "CF")
                cambiar_valor_box(textbox_t0, "0")
                cambiar_valor_box(textbox_tn, "10")
            else:
                cambiar_valor_button(button_t0, "FN")
                cambiar_valor_button(button_tn, "FN")
                cambiar_valor_box(textbox_t0, "")
                cambiar_valor_box(textbox_tn, "")

            cambiar_valor_box(textbox_expresion, "np.random.random(N+1) * 10")
            seleccionar_metodo.buttons.set_active(int(label[-2])-1)

    ex = ["Exercicio 1ab", "Exercicio 1c", "Exercicio 1d", "Exercicio 2a", "Exercicio 2b", "Exercicio 3a", "Exercicio 3b", "Exercicio 4a", "Exercicio 4b", "Exercicio 5a", "Exercicio 5b", "Exercicio 6a", "Exercicio 6b"]
    ax_box = fig.add_axes([0.82, 0.1, 0.16, 0.57])

    seleccionar_exercicio.buttons = RadioButtons(ax_box, ex, activecolor="mediumseagreen")
    seleccionar_exercicio.buttons.on_clicked(click)

    rpos = ax_box.get_position().get_points()
    fh = fig.get_figheight()
    fw = fig.get_figwidth()
    rscale = (rpos[:,1].ptp() / rpos[:,0].ptp()) * (fh / fw)

    for c in seleccionar_exercicio.buttons.circles:
        c.height /= rscale * 0.5
        c.width /= 0.5

def button_2d3d():
    def click(event):
        global ax
        ax.remove()
        if button_2d3d.button.label.get_text() == "2D":
            ax = fig.add_subplot(111, projection="3d")
            button_2d3d.button.label.set_text("3D")
        else:
            ax = fig.add_subplot(111)
            button_2d3d.button.label.set_text("2D")
        representar()

    ax_box = fig.add_axes([0.94, 0.02, 0.04, 0.05])
    button_2d3d.button = Button(ax_box, "2D")
    button_2d3d.button.on_clicked(click)

def button_sin():
    def click(event):
        cambiar_valor_box(textbox_expresion, "np.sin(np.pi*t)")
        cambiar_valor_button(button_t0, "CF")
        cambiar_valor_button(button_tn, "CF")
        cambiar_valor_box(textbox_t0, "0")
        cambiar_valor_box(textbox_tn, "0")

    ax_box = fig.add_axes([0.82, 0.045, 0.05, 0.025])
    button_sin.button = Button(ax_box, "Sin")
    button_sin.button.on_clicked(click)

def button_gauss():
    def click(event):
        cambiar_valor_box(textbox_expresion, "np.exp(-(t-2.5)**2/0.2)")
        cambiar_valor_button(button_t0, "CF")
        cambiar_valor_button(button_tn, "CF")
        cambiar_valor_box(textbox_t0, "0")
        cambiar_valor_box(textbox_tn, "0")

    ax_box = fig.add_axes([0.87, 0.045, 0.05, 0.025])
    button_gauss.button = Button(ax_box, "Gauss")
    button_gauss.button.on_clicked(click)

def button_rand():
    def click(event):
        cambiar_valor_box(textbox_expresion, "np.random.random(N+1) - 0.5")
        cambiar_valor_button(button_t0, "CF")
        cambiar_valor_button(button_tn, "CF")
        cambiar_valor_box(textbox_t0, "0")
        cambiar_valor_box(textbox_tn, "0")

    ax_box = fig.add_axes([0.82, 0.02, 0.05, 0.025])
    button_rand.button = Button(ax_box, "Rand")
    button_rand.button.on_clicked(click)

def button_flujo():
    def click(event):
        cambiar_valor_box(textbox_expresion, "t")
        cambiar_valor_button(button_t0, "FN")
        cambiar_valor_button(button_tn, "FN")
        cambiar_valor_box(textbox_t0, "")
        cambiar_valor_box(textbox_tn, "")

    ax_box = fig.add_axes([0.87, 0.02, 0.05, 0.025])
    button_flujo.button = Button(ax_box, "Flujo")
    button_flujo.button.on_clicked(click)

# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# Parte principal da aplicación
# ------------------------------------------------------------------

# Función para romper o bucle e sair da aplicacións
running = True
def stop(event):
    global running
    running = False

# Execución
def main():
    # Sair da aplicación ó cerrar a ventana de matplotlib
    fig.canvas.mpl_connect('close_event', stop)

    # Debuxar os botóns e caixas de texto
    textbox_expresion()
    textbox_t0()
    button_t0()
    textbox_tn()
    button_tn()
    textbox_dt()
    textbox_dx()
    textbox_alfa()
    textbox_N()
    textbox_it()
    seleccionar_metodo()
    seleccionar_exercicio()
    button_sin()
    button_gauss()
    button_rand()
    button_flujo()
    button_2d3d()

    # Representar os valores por defecto
    representar()

    # Bucle de presentación
    while running:
        try:
            plt.pause(0.016)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()