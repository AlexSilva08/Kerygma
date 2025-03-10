import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import numpy as np
import matplotlib.figure
import random

def plot():
    ax.clear() #Limpa o grafico

    nLinhas = 9
    nColunas = 9
    

    

    #Z = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    #Z = Z , [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    Z = []
    Zfim = []

    for m in range(0,nColunas):

        for n in range(0,nLinhas):

            x = random.random()
            #x = n/10

            Z.append(x)

        Zfim.append(Z)
        Z = []

    print(Zfim)

    #c = ax.pcolor(Zfim, cmap='RdBu', vmin=0, vmax=1)
    c = ax.pcolor(Zfim, cmap='YlOrRd', vmin=0, vmax=1)
    #c = ax.pcolor(Zfim, cmap='Reds', vmin=0, vmax=1)

    ax.set_title('default: no edges')

    fig.tight_layout()
    plt.show()
    
    canvas.draw() #Desenha o grafico


#Comeca o tkinter
root = tk.Tk()
fig = matplotlib.figure.Figure()
ax = fig.add_subplot()


#Aplicação do tkinter
frame = tk.Frame(root)
label = tk.Label(text= "Matplotlib + Tkinter!")
label.config(font=("Courier",32))
label.pack()
frame.pack()

canvas = FigureCanvasTkAgg(fig, master = frame)
canvas.get_tk_widget().pack()

toolbar = NavigationToolbar2Tk(canvas, frame, pack_toolbar = False) #Cria a barra de ferramentas do matplotlib
toolbar.update()
toolbar.pack(anchor="w", fill=tk.X)

tk.Button(frame, text= "Plot Graph", command = plot).pack(pady= 10)

root.mainloop()