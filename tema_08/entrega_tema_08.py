# Ecuacións de convección e transporte - Tema 8
# José Pazos Pérez - G3

# Índice
#     - [14]  Importacións
#     - [23]  Preparación de matplotlib
#     - [40]  Valores iniciais
#     - [74]  Coeficientes
#     - [186] Solución da ecuacións e representación
#     - [418] Funcións da interfaz gráfica
#     - [560] Execución da aplicación

# ------------------------------------------------------------------
# Importacións
# ------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button, RadioButtons
from matplotlib.animation import ArtistAnimation
import matplotlib

# ------------------------------------------------------------------
# Preparación de matplotlib
# ------------------------------------------------------------------

# Eixos
fig, ax_1D = plt.subplots(figsize=(9, 6))
fig.subplots_adjust(bottom=0.11, right=0.8, top=0.95, left=0.08)
ax_2D = fig.add_subplot(111)
ax_2D.set_visible(False)

# Modo interactivo
plt.ion()

# Rotación de cores
cores = ["royalblue", "mediumseagreen", "gold", "orange", "tomato", "hotpink", "mediumorchid"]
matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler("color", cores)

# ------------------------------------------------------------------
# Valores iniciais
# ------------------------------------------------------------------

# Iteracions temporais
it = 2000
# Escala espacial
N = 50
# Número de fotogramas
fr = 30

# Parámetros da discretización
dt = 0.1
dx = 0.5
a = 0.5
u = 0.05
C, s, t, Ti = None, None, None, None

# Parámetros específicos para as ecuacións en dúas dimensións
d2x = 0.5
d2y = 0.5
sx, sy = None, None

# Función para actualizar os parámetros que dependen de outros ó realizar algún cambio na interfaz
def calcular_parametros():
    global C, s, t, Ti, sx, sy
    C = u * (dt/dx)
    s = a * (dt/dx**2)
    t = np.linspace(0, dt*N, N+1)
    Ti = np.exp(-(t-1.0)**2/0.2)
    sx = a * (dt/d2x**2)
    sy = a * (dt/d2y**2)
calcular_parametros()

# ------------------------------------------------------------------
# Coeficientes de x e t para os distintos métodos 
# Actualízase automáticamente cando cambiamos C ou s
# C - Convección
# T - Transporte
# M - Multidimensional (de difusión)
# I - Implícito (ou semiimplícito no caso da ecuación de difusión 2D)
# ------------------------------------------------------------------

coeficientes = lambda: {
    "[C] FTCS": ({
        -1: 0.5*C,
        0: 1,
        1: -0.5*C
    }, {}),

    "[C] Upwind": ({
        -1: C,
        0: 1 - C,
        1: 0
    }, {}),

    "[C] DuFort-\nFrankel": ({
        -1: C,
        0: 0,
        1: -C
    }, {
        -1: 1
    }),

    "[CI] 2 niveis": ({
        -1: -0.5*C,
        0: 1,
        1: 0.5*C
    }, {
        0: 1
    }),

    "[CI] Crank-\nNicolson": ({
        -1: -C/4,
        0: 1,
        1: C/4
    }, {
        -1: C/4,
        0: 1,
        1: -C/4
    }),

    "[T] FTCS": ({
        -1: 0.5*C + s,
        0: -2*s + 1,
        1: -0.5*C + s
    }, {}),

    "[T] Upwind": ({
        -1: C + s,
        0: 1 - C - 2*s,
        1: s
    }, {}),

    "[T] DuFort-\nFrankel": ({
        -1: 1/(1+2*s) * (C + 2*s),
        0: 0,
        1: 1/(1+2*s) * (-C + 2*s)
    }, {
        -1: 1/(1+2*s) * (1 - 2*s)
    }),

    "[TI] 2 niveis": ({
        -1: -0.5*C - s,
        0: 1 + 2*s,
        1: 0.5*C - s
    }, {
        0: 1
    }),

    "[TI] Crank-\nNicolson": ({
        -1: -s/2 - C/4,
        0: 1 + s,
        1: -s/2 + C/4
    }, {
        -1: s/2 + C/4,
        0: 1 - s,
        1: s/2 - C/4
    }),

    "[M] FTCS 2D\nDifusión": ({
        -1: sx,
        0: 1 - 2*sx - 2*sy,
        1: sx
    }, {
        -1: sy,
        1: sy
    }),

    "[MI] ADI 2D\nDifusión": ({
        -1: -0.5*sx,
        0: 1+sx,
        1: -0.5*sx
    }, {
        -1: -0.5*sy,
        0: 1+sy,
        1: -0.5*sy
    }),
}

metodo = "[C] FTCS"

# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# Elixir entre a representación de unha e dúas dimensións en base ó método empregado
# Na representación 2D ocultamos os controles, non porque non sexa posible utilizamos, mais tómalle tempo á pantalla representar
# a animación e o cambio de valores fai que a aplicación se conxele un tempo considerable mentres se recalculan
# Estaría ben optimizar a xeración e representación de imaxes en 2D mais para unha primeira versión considero que é aceptable
# ------------------------------------------------------------------

def representar():
    if metodo[1] == "M":
        ax_boton_pausa.set_visible(False)
        ax_boton_animar.set_visible(False)
        ax_textbox_dt.set_visible(False)
        ax_textbox_dx.set_visible(False)
        ax_textbox_a.set_visible(False)
        ax_textbox_u.set_visible(False)
        ax_textbox_N.set_visible(False)
        ax_textbox_it.set_visible(False)
        text_2D.set_visible(True)
        plt.pause(0.0001)
        representar_2D()
    else:
        ax_boton_pausa.set_visible(True)
        ax_boton_animar.set_visible(True)
        ax_textbox_dt.set_visible(True)
        ax_textbox_dx.set_visible(True)
        ax_textbox_a.set_visible(True)
        ax_textbox_u.set_visible(True)
        ax_textbox_N.set_visible(True)
        ax_textbox_it.set_visible(True)
        text_2D.set_visible(False)
        representar_1D()

# ------------------------------------------------------------------
# Solución das ecuacións de convección e transporte en unha dimensión
# ------------------------------------------------------------------

def representar_1D():
    # Limpar a representación anterior
    ax_1D.clear()
    representar.frames.clear()

    # Función temperatura
    T = Ti.copy()

    # Coeficientes
    cx, ct = coeficientes()[metodo]

    # Dimensión do método (1 para 3 coeficientes, 2 para 5...)
    x_n = (len(cx) >> 1)

    # ---

    # Método implícito
    implicito = metodo[2] == "I"
    M = None
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
            M = np.linalg.inv(A)
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
            M = np.linalg.inv(np.dot(Bi, A))

        T = np.vstack([T])

    # ---
    
    # Método explícito
    else:
        # Engadimos valores auxiliares ós lados de T
        T = np.concatenate(([T[0]] * (x_n-1), T, [T[N]] * (x_n-1)))

        # Crear varios arrays para almacear os valores pasados no tempo (0 é o actual, 1 é o anterior...)
        T = np.vstack([T] * (len(ct)+1))

    # ---

    # Bucle temporal
    for i in range(it):
        # Cálculo do seguinte vector sen cambiar as condiciones de frontera
        # Método implícito
        if implicito:
            T[0] = np.dot(M, T[0])
        # Método explícito
        else:
            # Suma a parte pertinente ós coeficientes temporais e os coeficientes espaciais
            T[0, x_n:-x_n] = sum([T[0, x_n+i : -x_n+i or None] * coef for i, coef in cx.items()]) + sum([T[-i, x_n:-x_n] * coef for i, coef in ct.items()])

        # Condicions de frontera de fluxo nulo
        T[0, 0:x_n] = T[0, x_n+1]
        T[0, -x_n:] = T[0, -x_n-1]

        # Propagar os cambios de atrás cara adiante (só explícito)
        if not implicito:
            for j in range(len(ct), 0, -1):
                T[j] = T[j-1].copy()

        # Gardamos un fotograma cada varias iteracións
        if i % (it // fr) == 0:
            im = ax_1D.plot(t, T[0, x_n-1:-x_n+1 or None], animated=True, color="royalblue")
            representar.frames.append(im)

    if anim_evolucion:
        for i in range(len(representar.frames)):
            representar.frames[i][0].set_animated(False)
            representar.frames[i][0].set_visible(True)
            representar.frames[i][0].set_color(cores[i % len(cores)])

    ax_1D.set_visible(True)

# ------------------------------------------------------------------
# Solución da ecuación de difusión en dúas dimensións
# ------------------------------------------------------------------

def representar_2D():
    # Limpar a representación anterior
    ax_2D.clear()
    representar.frames.clear()

    # Función temperatura (liña no centro)
    T = np.zeros((N+1, N+1))
    for i in range(N+1):
        if i > N/2 - N/10 and i < N/2 + N/10:
            T[i, i] = 10

    # Coeficientes
    cx, cy = coeficientes()[metodo]

    # Dimensión do método (1 para 3 coeficientes, 2 para 5...)
    x_n = (len(cx) >> 1)
    assert x_n == 1

    # ---

    # Método semiimplícito
    semiimplicito = metodo[2] == "I"
    Ai, Bi = None, None
    if semiimplicito:
        # Matriz de coeficientes A
        A = np.zeros((N+1, N+1))
        for i in range(1, N):
            for c in cx:
                A[i, i+c] = cx[c]
        A[0, 0] = 1
        A[N, N] = 1
        # Matriz de coeficientes B
        B = np.zeros((N+1, N+1))
        for i in range(1, N):
            for c in cy:
                B[i, i+c] = cy[c]
        B[0, 0] = 1
        B[N, N] = 1
        # Matrices inversas
        Ai = np.linalg.inv(A)
        Bi = np.linalg.inv(B)

    # ---

    # Bucle temporal
    for i in range(it):
        T_ = T.copy()

        # Método semi implicito (ADI)
        if semiimplicito:
            for j in range(1, N):
                # Paso explícito en y
                Y = np.concatenate([[0], sy/2 * T[1:N, j-1] + (1-sy) * T[1:N, j] + sy/2 * T[1:N, j+1], [0]])
                # T_ por columnas
                T_[:, j] = np.dot(Ai, Y)
            for j in range(1, N):
                # Paso explícito en x
                X = np.concatenate([[0], sx/2 * T_[j-1, 1:N] + (1-sx) * T_[j, 1:N] + sx/2 * T_[j+1, 1:N], [0]])
                # T por filas
                T[j, :] = np.dot(Bi, X)
        # Método explícito
        else:
            for j in range(1, N):
                for k in range(1, N):
                    T_[j, k] = sum([T[j+i, k] * coef for i, coef in cx.items()]) + sum([T[j, k+i] * coef for i, coef in cy.items()])
            T = T_.copy()

        # Condicions de fronteira de fluxo nulo
        T[0, :] = T[1, :]
        T[-1, :] = T[-2, :]
        T[:, 0] = T[:, 1]
        T[:, -1] = T[:, -2]

        # Gardamos un fotograma cada varias iteracións
        if i % (it // fr) == 0:
            im = ax_2D.imshow(T, animated=True)
            representar.frames.append([im])
            text_2D.set_text(f"Calculando... iteración {i}/{it}")
            plt.pause(0.000001)
    
    # Actualizamos o texto indicativo e amosamos o gráfico na pantalla
    text_2D.set_text("Amosando en pantalla... (isto pode tardar un rato)")
    plt.pause(0.1)
    ax_2D.set_visible(True)
    text_2D.set_text(f"it = {it}, dt = {dt}, dx = {d2x}, dy = {d2y}, alpha = {a}, sx = {sx}, sy = {sy}")


# Lista con fotogramas da animación
representar.frames = []

# Controlador da animación
anim = ArtistAnimation(fig, representar.frames, interval=60, blit=True)
anim_pausa = False
anim_evolucion = False

# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# Interfaz
# ------------------------------------------------------------------

# Botón pausa
ax_boton_pausa = plt.axes([0.08, 0.02, 0.03, 0.04])
boton_pausa = Button(ax_boton_pausa, "II", color="royalblue", hovercolor="lightblue")
boton_pausa.label.set_weight("bold")
boton_pausa.label.set_color("white")

def pausa(event):
    global anim_pausa, boton_pausa
    anim_pausa = not anim_pausa
    anim.pause() if anim_pausa else anim.resume()
    boton_pausa.label.set_text(">" if anim_pausa else "II")

boton_pausa_cid = boton_pausa.on_clicked(pausa)

# Botón mostrar animación/evolución
ax_boton_animar = plt.axes([0.12, 0.02, 0.07, 0.04])
boton_animar = Button(ax_boton_animar, "mostrar\nevolución", color="royalblue", hovercolor="lightblue")
boton_animar.label.set_color("white")
boton_animar.label.set_fontsize("8")

def animar(event):
    global anim_evolucion, anim_pausa, boton_animar, boton_pausa, boton_pausa_cid
    anim_evolucion = not anim_evolucion
    if anim_evolucion:
        anim_pausa = True
        anim.pause()

        boton_animar.label.set_text("mostrar\nanimación")

        boton_pausa.disconnect(boton_pausa_cid)
        boton_pausa.label.set_text("")
        boton_pausa.color = "slategray"

        for i in range(len(representar.frames)):
            representar.frames[i][0].set_animated(False)
            representar.frames[i][0].set_visible(True)
            representar.frames[i][0].set_color(cores[i % len(cores)])
    else:
        anim_pausa = False
        anim.resume()

        boton_animar.label.set_text("mostrar\nevolución")

        boton_pausa_cid = boton_pausa.on_clicked(pausa)
        boton_pausa.label.set_text("II")
        boton_pausa.color = "royalblue"

        for i in range(len(representar.frames)):
            representar.frames[i][0].set_animated(True)
            representar.frames[i][0].set_visible(False)
            representar.frames[i][0].set_color("royalblue")

boton_animar.on_clicked(animar)

# Teclado
def pulsar_tecla(event):
    if event.key == " " and not metodo[1] == "M":
        pausa(event)

# Seleccionar método
def seleccionar_metodo(label):
    global metodo, it, dt, a, anim_evolucion
    metodo = label

    anim.pause()
    ax_1D.set_visible(False)
    ax_2D.set_visible(False)

    if metodo[1] == "C":
        it = 2000
        dt = 0.1

    if metodo[1] == "T":
        it = 2000
        dt = 0.1
        a = 0.01

    if metodo[1] == "M":
        anim_evolucion = False
        it = 100
        dt = 0.1
        a = 0.5

    calcular_parametros()
    actualizar_textboxes()
    representar()
    if not anim_evolucion:
        anim.resume()

m = [k for k, v in coeficientes().items()]
seleccionar_metodo_ax = fig.add_axes([0.82, 0.11, 0.16, 0.84])

seleccionar_metodo_button = RadioButtons(seleccionar_metodo_ax, m, active=list(coeficientes().keys()).index(metodo), activecolor="royalblue")
seleccionar_metodo_button.on_clicked(seleccionar_metodo)

rpos = seleccionar_metodo_ax.get_position().get_points()
fh = fig.get_figheight()
fw = fig.get_figwidth()
rscale = (rpos[:,1].ptp() / rpos[:,0].ptp()) * (fh / fw)

for c in seleccionar_metodo_button.circles:
    c.height /= rscale

# Textboxes
def textbox(nome, x, y):
    def submit(expr):
        if globals()[nome] == eval(expr):
            return
        globals()[nome] = eval(expr)
        calcular_parametros()
        representar()
    box_ax = fig.add_axes([x, y, 0.055, 0.04])
    box = TextBox(box_ax, nome + " ", initial=str(globals()[nome]))
    box.on_submit(submit)
    return box, box_ax

textbox_dt, ax_textbox_dt = textbox("dt", 0.220, 0.02)
textbox_dx, ax_textbox_dx = textbox("dx", 0.305, 0.02)
textbox_a, ax_textbox_a = textbox("a", 0.385 , 0.02)
textbox_u, ax_textbox_u = textbox("u", 0.465, 0.02)
textbox_N, ax_textbox_N = textbox("N", 0.545, 0.02)
textbox_it, ax_textbox_it = textbox("it", 0.625, 0.02)

text_2D = fig.text(0.08, 0.03, "Calculando... iteración 0/100", color="royalblue")
text_2D.set_visible(False)

def actualizar_textboxes():
    textbox_dt.set_val(str(dt))
    textbox_dx.set_val(str(dx))
    textbox_a.set_val(str(a))
    textbox_u.set_val(str(u))
    textbox_N.set_val(str(N))
    textbox_it.set_val(str(it))

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
    # Eventos
    fig.canvas.mpl_connect('close_event', stop)
    fig.canvas.mpl_connect('key_press_event', pulsar_tecla)

    # Representar os valores iniciais
    representar()
    representar.frames[0][0].set_visible(False)

    # Animación
    anim.resume()

    # Bucle de presentación
    while running:
        try:
            plt.pause(0.005)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()