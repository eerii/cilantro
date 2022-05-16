# Ecuacións de convección e transporte - Tema 8
# José Pazos Pérez - G3

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
fig, ax = plt.subplots(figsize=(9, 6))
fig.subplots_adjust(bottom=0.2, right=0.92, top=0.95, left=0.08)

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
u = 0.05
C = u * (dt/dx)

# Eixo temporal
t = np.linspace(0, dt*N, N+1)

# Valor inicial da temperatura
Ti = np.exp(-(t-1.0)**2/0.2)

# ------------------------------------------------------------------
# Coeficientes de x e t para os distintos métodos 
# Actualízase automáticamente cando cambiamos s
# ------------------------------------------------------------------

coeficientes = lambda: {
    "FTCS": ({
        -1: 0.5*C,
        0: 1,
        1: -0.5*C
    }, {}),

    "Upwind": ({
        -1: C,
        0: 1 - C,
        1: 0
    }, {}),

    "DuFort-Frankel": ({
        -1: C,
        0: 0,
        1: -C
    }, {
        -1: 1
    }),

    "[Impl] Dos niveles": ({
        -1: -0.5*C,
        0: 1,
        1: 0.5*C
    }, {
        0: 1
    }),

    "[Impl] Crank-Nicolson": ({
        -1: -C/4,
        0: 1,
        1: C/4
    }, {
        -1: C/4,
        0: 1,
        1: -C/4
    }),
}

metodo = "[Impl] Crank-Nicolson"

# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# Solución da ecuación
# ------------------------------------------------------------------

def representar():
    # Limpar a representación anterior
    ax.clear()

    # Función temperatura
    T = Ti.copy()

    # Coeficientes
    cx, ct = coeficientes()[metodo]

    # Dimensión do método (1 para 3 coeficientes, 2 para 5...)
    x_n = (len(cx) >> 1)

    # ---

    # Método implícito
    implicito = metodo[0:6] == "[Impl]"
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
            im = ax.plot(t, T[0, x_n-1:-x_n+1 or None], animated=True, color="royalblue")
            representar.frames.append(im)

    # Actualizar a vista
    ax.relim()
    ax.autoscale_view()

# Lista con fotogramas da animación
representar.frames = []

# Controlador da animación
anim = ArtistAnimation(fig, representar.frames, interval=60, blit=True, repeat_delay=1000)
anim_pausa = False
anim_evolucion = False

# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# Interfaz
# ------------------------------------------------------------------

# Botón pausa
ax_boton_pausa = plt.axes([0.08, 0.10, 0.03, 0.04])
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
ax_boton_animar = plt.axes([0.12, 0.10, 0.07, 0.04])
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
    if event.key == " ":
        pausa(event)

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