# Importacións
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
import matplotlib

# ------------------------------------------------------------------

# Preparación de matplotlib
fig, ax = plt.subplots(figsize=(9, 6))
fig.subplots_adjust(bottom=0.2, right=0.8, top=0.95, left=0.08)
plt.ion()

# Rotación de cores
matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler("color", ["royalblue", "mediumseagreen", "gold", "orange", "tomato", "hotpink", "mediumorchid"])

# ------------------------------------------------------------------

# Iteracions temporais
it = 2000
# Parámetros da discretización
dt = 0.1
dx = 0.5
alfa = 0.1
N = 100
# Estabilidade
s = alfa * (dt/dx**2)
# Eixo temporal
t = np.linspace(0, dt*N, N+1)

Ti = np.sin(t)
cf = [0, 0]

# ------------------------------------------------------------------

# Coeficientes de x e t para os distintos métodos (actualízase automáticamente cando cambiamos s)
coeficientes = lambda: {
    "FTCS": ({
        -1: s,
        0: 1 - 2*s,
        1: s
    }, {}),

    "Tres niveis temporais": ({
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
}

metodo = "FTCS"

# ------------------------------------------------------------------


def representar():
    # Función temperatura
    T = Ti.copy()

    # Condicións de frontera de Dirichlet
    if cf[0] != "FN":
        T[0] = cf[0]
    if cf[1] != "FN":
        T[N] = cf[1]

    # Coeficientes
    cx, ct = coeficientes()[metodo]

    # Dimensión do método (1 para 3 coeficientes, 2 para 5...)
    # Engadimos valores auxiliares ós lados de T
    x_n = (len(cx) >> 1)
    T = np.concatenate(([T[0]] * (x_n-1), T, [T[N]] * (x_n-1)))

    # Crear varios arrays para almacear os valores pasados no tempo (0 é o actual, 1 é o anterior...)
    T = np.vstack([T] * (len(ct)+1))

    # Limpar a representación anterior
    ax.clear()

    # Bucle temporal
    for i in range(it):
        # Cálculo do seguinte vector sen cambiar as condiciones de frontera
        # Suma a parte pertinente ós coeficientes temporais e os coeficientes espaciais
        T[0, x_n:-x_n] = sum([T[0, x_n+i : -x_n+i or None] * coef for i, coef in cx.items()]) + sum([T[-i, x_n:-x_n] * coef for i, coef in ct.items()])

        # Condicions de frontera de fluxo nulo
        if cf[0] == "FN":
            T[0, 0:x_n] = T[0, x_n+1]
        if cf[1] == "FN":
            T[0, -x_n:] = T[0, -x_n-1]

        # Propagar os cambios de atrás cara adiante
        for j in range(len(ct), 0, -1):
            T[j] = T[j-1].copy()

        # Representación cada varias iteracións
        if i % (it // 20) == 0:
            ax.plot(t, T[0, x_n-1:-x_n+1 or None])

    # Actualizar a vista
    ax.relim()
    ax.autoscale_view()

# ------------------------------------------------------------------

def textbox_expresion():
    def submit(expr):
        global Ti
        Ti = eval(expr)
        representar()

    ax_box = fig.add_axes([0.08, 0.1, 0.72, 0.05])
    textbox_expresion.box = TextBox(ax_box, "T", textalignment="center", initial="np.sin(t)")
    textbox_expresion.box.on_submit(submit)

def textbox_t0():
    def submit(expr):
        global cf
        cf[0] = "FN" if button_t0.button.label.get_text() == "FN" else eval(expr)
        representar()

    ax_box = fig.add_axes([0.08, 0.02, 0.07, 0.05])
    textbox_t0.box = TextBox(ax_box, "T[0] ", textalignment="center", initial="0")
    textbox_t0.box.on_submit(submit)

def textbox_tn():
    def submit(expr):
        global cf
        cf[1] = "FN" if button_tn.button.label.get_text() == "FN" else eval(expr)
        representar()

    ax_box = fig.add_axes([0.25, 0.02, 0.07, 0.05])
    textbox_tn.box = TextBox(ax_box, "T[N] ", textalignment="center", initial="0")
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

    ax_box = fig.add_axes([0.15, 0.02, 0.05, 0.05])
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

    ax_box = fig.add_axes([0.32, 0.02, 0.05, 0.05])
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

    ax_box = fig.add_axes([0.4, 0.02, 0.07, 0.05])
    textbox_dt.box = TextBox(ax_box, "dt ", textalignment="center", initial=str(dt))
    textbox_dt.box.on_submit(submit)

def textbox_dx():
    def submit(expr):
        global dx, s
        dt = eval(expr)
        s = alfa * (dt/dx**2)
        representar()

    ax_box = fig.add_axes([0.5, 0.02, 0.07, 0.05])
    textbox_dx.box = TextBox(ax_box, "dx ", textalignment="center", initial=str(dx))
    textbox_dx.box.on_submit(submit)

def textbox_alfa():
    def submit(expr):
        global alfa, s
        alfa = eval(expr)
        s = alfa * (dt/dx**2)
        representar()

    ax_box = fig.add_axes([0.59, 0.02, 0.07, 0.05])
    textbox_alfa.box = TextBox(ax_box, "$\\alpha$ ", textalignment="center", initial=str(alfa))
    textbox_alfa.box.on_submit(submit)

def textbox_N():
    def submit(expr):
        global N, t, Ti
        N = eval(expr)
        t = np.linspace(0, dt*N, N+1)
        Ti = eval(textbox_expresion.box.text)
        representar()

    ax_box = fig.add_axes([0.685, 0.02, 0.8 - 0.685, 0.05])
    textbox_N.box = TextBox(ax_box, "N ", textalignment="center", initial=str(N))
    textbox_N.box.on_submit(submit)

# ------------------------------------------------------------------

# Función para romper o bucle e sair da aplicacións
running = True
def stop(event):
    global running
    running = False

# Parte principal da aplicación
def main():
    fig.canvas.mpl_connect('close_event', stop)

    textbox_expresion()
    textbox_t0()
    textbox_tn()

    button_t0()
    button_tn()

    textbox_dt()
    textbox_dx()
    textbox_alfa()
    textbox_N()

    representar()

    while running:
        try:
            plt.pause(0.01)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()