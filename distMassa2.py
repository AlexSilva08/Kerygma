import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import numpy as np
import pandas as pd
from tkinter import filedialog

def carregar_dados():
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx;*.xls")])
    if not arquivo:
        return
    
    df = pd.read_excel(arquivo)  # Lê a planilha

    colunas_desejadas = ["D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11"]

    # Verifica se todas as colunas necessárias estão no arquivo
    if not all(col in df.columns for col in colunas_desejadas):
        lbl_status.config(text="Erro: As colunas 'D4' até 'D11' não foram encontradas!")
        return

    # Filtra as colunas necessárias
    dados = df[colunas_desejadas]

    # Remove linhas onde todas as colunas são zero
    dados = dados[(dados != 0).any(axis=1)]

    # Verifica se ainda há dados após a remoção
    if dados.empty:
        lbl_status.config(text="Erro: Todas as linhas continham apenas zeros!")
        return

    # Converte os dados para uma matriz NumPy
    matriz = dados.to_numpy()

    plot(matriz)

def plot(matriz):
    ax.clear()  # Limpa o gráfico

    # Cria o mapa de calor usando os dados filtrados
    c = ax.pcolor(matriz, cmap='YlOrRd', vmin=np.min(matriz), vmax=np.max(matriz))

    ax.set_title("Distribuição de Massa - Dados do Excel")

    fig.tight_layout()
    plt.show()
    
    canvas.draw()  # Atualiza o gráfico no Tkinter

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Mapa de Calor - Dados do Excel")

fig = plt.Figure()
ax = fig.add_subplot()

# Criando a interface gráfica
frame = tk.Frame(root)
label = tk.Label(text="Matplotlib + Tkinter + Excel!")
label.config(font=("Courier", 20))
label.pack()
frame.pack()

canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack()

toolbar = NavigationToolbar2Tk(canvas, frame, pack_toolbar=False)  # Barra de ferramentas do Matplotlib
toolbar.update()
toolbar.pack(anchor="w", fill=tk.X)

tk.Button(frame, text="Carregar Dados do Excel", command=carregar_dados).pack(pady=10)

lbl_status = tk.Label(root, text="Selecione um arquivo Excel com os dados de D4 até D11.")
lbl_status.pack()

root.mainloop()
