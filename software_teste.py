from tkinter import *
from tkinter import PhotoImage
from tkinter import messagebox
from PIL import Image, ImageTk 
import customtkinter as ctk
import boxes
import serial
import time
import glob
import subprocess
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.figure
import numpy as np
import pandas as pd
import openpyxl
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import time
import math
from tkinter import ttk
import os
import csv
import re

root = ctk.CTk()
root.title("Nome do Software")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.minsize(width=1280, height=720)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.attributes("-fullscreen", True)

# Criação das telas    
tela_inicial = Frame(root)
tela_dados = Frame(root)
tela_parametros = Frame(root)
tela_anamnese = Frame(root)
tela_resultado = Frame(root)
tela_carregamento = Frame(root)

# Função para trazer a tela pra frente
def show_frame(frame): 
    frame.tkraise()

def close_app():
    root.destroy()

is_fullscreen = True
def toogle_fullscreen():
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)

# For para posicionamento das telas
for frame in (tela_inicial, tela_dados, tela_parametros, tela_resultado, tela_anamnese, tela_carregamento): 
    frame.grid(row=0, column=0, sticky='nsew')

show_frame(tela_inicial)

#Background Telas
bg_geral1 = Image.open("UI/background.png")
bg_geral1 = bg_geral1.resize((screen_width, screen_height), Image.LANCZOS)
bg_geral = ImageTk.PhotoImage(bg_geral1)

bg_dados1 = Image.open("UI/bg_dados.png")
bg_dados1 = bg_dados1.resize((screen_width, screen_height), Image.LANCZOS)
bg_dados = ImageTk.PhotoImage(bg_dados1)

bg_anamnese1 = Image.open("UI/bg_anamnese.png")
bg_anamnese1 = bg_anamnese1.resize((screen_width, screen_height), Image.LANCZOS)
bg_anamnese = ImageTk.PhotoImage(bg_anamnese1)

bg_parametros1 = Image.open("UI/bg_parametros.png")
bg_parametros1 = bg_parametros1.resize((screen_width, screen_height), Image.LANCZOS)
bg_parametros = ImageTk.PhotoImage(bg_parametros1)

bg_carregamento1 = Image.open("UI/bg_carregamento.png")
bg_carregamento1 = bg_carregamento1.resize((screen_width, screen_height), Image.LANCZOS)
bg_carregamento = ImageTk.PhotoImage(bg_carregamento1)

bg_resultado1 = Image.open("UI/Resultado/bg_resultado.png")
bg_resultado1 = bg_resultado1.resize((screen_width, screen_height), Image.LANCZOS)
bg_resultado = ImageTk.PhotoImage(bg_resultado1)

#Bg botão geral
width_bg_btn = int((screen_width * 9.9) / 100)
height_bg_btn = int((screen_height * 9.26) / 100)
bg_btn1 = Image.open("UI/bg_btn.png")
bg_btn1 = bg_btn1.resize((width_bg_btn, height_bg_btn), Image.Resampling.LANCZOS)
bg_btn = ImageTk.PhotoImage(bg_btn1)

#Variavel para tamanho de vonte dos botões gerais
fontsize = int((screen_height * 1.83) / 100)

fontsize14 = int((screen_height * 1.30) / 100)

#MARK: TELA INICIAL --------------------------------------------------------------------------------------------------------------

canvas_inicial = Canvas(tela_inicial, width=1920, height=1080)
canvas_inicial.grid(row=0, column=0)
canvas_inicial.create_image(0, 0, image=bg_geral, anchor="nw")

# Botão de fechar
btn_fechar = ctk.CTkButton(
    tela_inicial,
    text="X",
    font=("Helvetica", 16, "bold"),
    corner_radius=14,
    width=47,
    height=37,
    text_color="#ffffff", 
    fg_color="#3e567c",
    hover_color="#2b3a52",
    command=lambda: close_app()
)
btn_fechar.place(relx=0.97, rely=0.002)

# Icone de fullscreen
icon_fullscreen = Image.open("UI/icon_fullscreen.png").resize((40, 40), Image.LANCZOS)
icon_fullscreen = ImageTk.PhotoImage(icon_fullscreen)
toogle_button = Button(
    tela_inicial,
    image=icon_fullscreen,
    bd=0,
    highlightthickness=0,
    command=toogle_fullscreen,
    bg="white"
)
toogle_button.place(relx=0.947, rely=0)

# Título
canvas_inicial.create_text(
    640, 50,
    text="Tela Inicial", 
    font=('Arial', 24, 'bold'), 
    fill="#3e567c"
)

# Configuração de Botões Inicial
btn_iniciar = Button(
    tela_inicial,
    text="INICIAR",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((screen_width * 9.9) / 100)-2,
    height=((screen_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: show_frame(tela_dados) 
)
btn_iniciar.place(relx=0.5, rely=0.6, anchor='center')

#MARK: TELA DADOS ----------------------------------------------------------------------------------------------------------

canvas_dados = Canvas(tela_dados, width=screen_width, height=screen_height)
canvas_dados.grid(row=0, column=0)
canvas_dados.create_image(0, 0, image=bg_dados, anchor="nw")


# Entradas de dados do paciente
entradas = []

nome_label = Label(tela_dados, text="Nome:", font=("Inter", 16, "bold"), background="#D1DCE4", fg="#2F2F2F")
nome_label.place(relx=0.5531, rely=0.2758)
nome_paciente = ctk.CTkEntry(tela_dados, width=(screen_width *38.28/100), height=(screen_height * 6.02/100), font=("Inter", 16, "bold"), bg_color="#D1DCE4", border_color="#A7BBCB", border_width=3, corner_radius=12)
nome_paciente.place(relx=0.5458, rely=0.3138)
entradas.append(nome_paciente)

idade_label = Label(tela_dados, text="Idade:", font=("Inter", 16, "bold"), background="#D1DCE4", fg="#2F2F2F")
idade_label.place(relx=0.5531, rely=0.398)
idade_paciente = ctk.CTkEntry(tela_dados, width=(screen_width * 18.23/100), height=(screen_height * 6.02/100), font=("Inter", 16, "bold"), bg_color="#D1DCE4", border_color="#A7BBCB", border_width=3, corner_radius=12)
idade_paciente.place(relx=0.5458, rely=0.4306)
entradas.append(idade_paciente)

altura_label = Label(tela_dados, text="Altura:", font=("Inter", 16, "bold"), background="#D1DCE4", fg="#2F2F2F")
altura_label.place(relx=0.7573, rely=0.398)
altura_paciente = ctk.CTkEntry(tela_dados, width=(screen_width *18.23/100), height=(screen_height * 6.02/100), font=("Inter", 16, "bold"), bg_color="#D1DCE4", border_color="#A7BBCB", border_width=3, corner_radius=12)
altura_paciente.place(relx=0.7464, rely=0.4306)
entradas.append(altura_paciente)

peso_label = Label(tela_dados, text="Peso:", font=("Inter", 16, "bold"), background="#D1DCE4", fg="#2F2F2F")
peso_label.place(relx=0.5531, rely=0.514)
peso_paciente = ctk.CTkEntry(tela_dados,width=(screen_width *18.23/100), height=(screen_height * 6.02/100), font=("Inter", 16, "bold"), bg_color="#D1DCE4", border_color="#A7BBCB", border_width=3, corner_radius=12)
peso_paciente.place(relx=0.5458, rely=0.5463)
entradas.append(peso_paciente)

btn_armazenardados = Button(
    tela_dados,
    text="Cadastrar",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((screen_width * 9.9) / 100)-2,
    height=((screen_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    bg="#D1DCE4",
    command=lambda: armazenar_dados()
)
btn_armazenardados.place(relx=0.6729, rely=0.6778)

seta_comboboxPil = Image.open("UI/seta_combobox.png")
img_seta = ctk.CTkImage(dark_image=seta_comboboxPil, light_image=seta_comboboxPil, size=(18, 12))
sexo_label = Label(tela_dados, text="Sexo:", font=("Inter", 16, "bold"), background="#D1DCE4", fg="#2F2F2F")
sexo_label.place(relx=0.7573, rely=0.514)
sexo_paciente = boxes.CustomComboBox(
    tela_dados,
    values=["Feminino", "Masculino", "Outro"],
    width=(screen_width *18.23/100),
    height=(screen_height * 6.02/100),
    font=("Inter", 16, "bold"),
    button_color="#FFFFff",  # Cor do botão principal
    dropdown_fg_color="#E0E0E0",  # Cor do fundo do dropdown
    dropdown_text_color="#304462",  # Cor do texto no dropdown
    img_seta=img_seta,
    text_color="#304462",  # Cor do texto do botão principal
    button_hover_color="#a7bbcb",  # Cor de hover do botão principal
    dropdown_hover_color="#a7bbcb",  # Cor de hover para o dropdown
    border_color="#A7BBCB", 
    border_width=3, 
    corner_radius=12,
    bg_color="#D1DCE4"
    )
sexo_paciente.place(relx=0.7464, rely=0.5463)
entradas.append(sexo_paciente)


# Função para armazenar os dados em uma lista
dados_paciente_lista = []
dados_velocidade_lista = []

def armazenar_dados():
    global dados_paciente_lista
    dados_paciente_lista = [entrada.get() for entrada in entradas]
    for entrada in entradas:
        entrada.delete(0, END)


#MARK: Carregar perfil
def CarregarPerfil():
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    Dados = pd.read_excel(filename)

    Dados_CopX = [0]
    Dados_CopY = [0]

    num = 0

    nome_paciente = Dados.Nome[0]
    idade_paciente = Dados.Idade[0]
    altura_paciente = Dados.Altura[0]
    peso_paciente = Dados.Peso[0]
    sexo_paciente = Dados.Sexo[0]

    for index in Dados.iterrows():

        D0 = Dados.D0[num]
        D1 = Dados.D1[num]
        D2 = Dados.D2[num]
        D3 = Dados.D3[num]
        D4 = Dados.D4[num]
        D5 = Dados.D5[num]
        D6 = Dados.D6[num]
        D7 = Dados.D7[num]
        D8 = Dados.D8[num]
        D9 = Dados.D9[num]
        D10 = Dados.D10[num]
        D11 = Dados.D11[num]
        
        P0 = Dados.D12[num]
        P1 = Dados.D13[num]
        P2 = Dados.D14[num]
        P3 = Dados.D15[num]

        P4 = Dados.D16[num]
        P5 = Dados.D17[num]
        P6 = Dados.D18[num]
        P7 = Dados.D19[num]

        print("Dados do D19:", P7)

        DxP0= 16.8
        DyP0= 16
        DxP1= 3.4
        DyP1= 16.5
        DxP2= 3.4
        DyP2= 16
        DxP3= 17
        DyP3= 16

        DxP4= 3.5
        DyP4= 16
        DxP5= 17
        DyP5= 15.5
        DxP6= 17
        DyP6= 16
        DxP7= 3.8
        DyP7= 16

        if (P0+P1+P2+P3+P4+P5+P6+P7) > 0:
            CopX = (P4*DxP4 + P5*DxP5 + P6*DxP6 + P7*DxP7 - P0*DxP0 - P1*DxP1 - P2*DxP2 - P3*DxP3)/(P0+P1+P2+P3+P4+P5+P6+P7)
        else:
            CopX = 0

        if (P0+P1+P2+P3+P4+P5+P6+P7) > 0:
            CopY = (P0*DyP0 + P1*DyP1 + P4*DyP4 + P5*DyP5 - P2*DyP2 - P3*DyP3 - P6*DyP6 - P7*DyP7)/(P0+P1+P2+P3+P4+P5+P6+P7)
        else:
            CopY = 0

        Dados_CopX.append(CopX)
        Dados_CopY.append(CopY)

        num = num + 1

    ax2.clear() #Limpa o grafico

    lineX = [0, 0, -20, -20, 20, 20, 0]
    lineY = [20, -20, -20, 20, 20, -20, -20]
    ax2.plot(lineX, lineY, color='#A7BBCB')
    ax2.plot(Dados_CopX, Dados_CopY, color='#304462')

    canvasMatplot2.draw() #Desenha o grafico
    
    global dados_paciente_lista
    dados_paciente_lista = [nome_paciente, idade_paciente, altura_paciente, peso_paciente, sexo_paciente]

    show_frame(tela_resultado)
    exibir_canvas(canvas_paciente)

# Função para exibir os dados salvos na tela de resultado
def dados_paciente(tela):
    show_frame(tela)
    exibir_canvas(canvas_paciente)

# Botões tela dados
btn_lerArquivo = Button(
    tela_dados,
    text="LER\nARQUIVO",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((screen_width * 9.9) / 100)-2,
    height=((screen_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command= CarregarPerfil
)
btn_lerArquivo.place(relx=0.1042, rely=0.8611)

btn_avancarDados = Button(
    tela_dados,
    text="AVANÇAR",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((screen_width * 9.9) / 100)-2,
    height=((screen_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: show_frame(tela_parametros)
)
btn_avancarDados.place(relx=0.7969, rely=0.8611)

#MARK: TELA ANAMNESE --------------------------------------------------------------------------------------------------------

canvas_anamnese = Canvas(tela_anamnese, width=screen_width, height=screen_height)
canvas_anamnese.grid(row=0, column=0)
canvas_anamnese.create_image(0, 0, image=bg_anamnese, anchor="nw")

btn_avancarAnamnese = Button(
    tela_anamnese,
    text="AVANÇAR",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((screen_width * 9.9) / 100)-2,
    height=((screen_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: dados_paciente(tela_parametros)
)
btn_avancarAnamnese.place(relx=0.7969, rely=0.8611)

#MARK: TELA PARÂMETROS ----------------------------------------------------------------------------------------------------------

canvas_parametros = Canvas(tela_parametros, width=screen_width, height=screen_height)
canvas_parametros.grid(row=0, column=0)
canvas_parametros.create_image(0, 0, image=bg_parametros, anchor="nw")

width_molduras = int((screen_width * 10.35)/100)
height_moldura01 = int((screen_height * 24.5)/100)
moldura1 = Image.open("UI/Parametros/moldura_01.png")
moldura1 = moldura1.resize((width_molduras, height_moldura01 ), Image.LANCZOS)
moldura01 = ImageTk.PhotoImage(moldura1)

height_moldura02 = int((screen_height * 11.5)/100)
moldura2 = Image.open("UI/Parametros/moldura_02.png")
moldura2 = moldura2.resize((width_molduras, height_moldura02), Image.LANCZOS)
moldura02 = ImageTk.PhotoImage(moldura2)

#Botão confirmar
width_bg_conf = int((screen_width * 7.92) / 100)
height_bg_conf = int((screen_height * 5.5) / 100)
bg_btn_conf1 = Image.open("UI/Parametros/btn_confirmar.png")
bg_btn_conf1 = bg_btn1.resize((width_bg_conf, height_bg_conf), Image.Resampling.LANCZOS)
bg_btn_conf = ImageTk.PhotoImage(bg_btn_conf1)

#MARK: CANVAS MOVIMENTAÇÃO -------------------------
canvas_movimentacao = Canvas(
    tela_parametros,
    width = (screen_width * 58.08)/100,
    height = (screen_height * 41.20)/100,
    bg="#E0E7EC",
    highlightthickness=0,
    highlightcolor=None,
    highlightbackground=None
)
canvas_movimentacao.place(relx=0.3453,rely=0.3491,anchor="nw")

canvas_oscilacao = Canvas(
    tela_parametros,
    width = (screen_width * 58.08)/100,
    height = (screen_height * 41.20)/100,
    bg="#E0E7EC",
    highlightthickness=0,
    highlightcolor=None,
    highlightbackground=None
)
canvas_oscilacao.place(relx=0.3453,rely=0.3491,anchor="nw")

rotina = ctk.CTkScrollableFrame(
    tela_parametros,
    width=(screen_width * 20.5/100),
    height=(screen_height * 41/100),
    corner_radius = 15,
    fg_color="#E0E7EC",
    orientation = "vertical"
    )
rotina.place(relx=0.0583, rely=0.3481, anchor = "nw")


matriz_parametros = []
combobox_criada = []
global index_radio
global index_combo
index_radio = 0
index_combo = 0


#for criando e inicializando um array dentro de um array (matriz) com valores zerados
for i in range (5):
    row = []
    for j in range (7):
        row.append(0)
    matriz_parametros.append(row)
        
var = ctk.IntVar()

def gerar_widgets(scrollable_frame, num_widgets,var):
    for i in range(num_widgets):
        # Criar o Frame para o ComboBox e RadioButton
        frame01 = ctk.CTkFrame(scrollable_frame,bg_color = "#E0E7EC",fg_color="#FFFFFF")
        frame01.pack(fill="x", pady = (screen_width * 0.5)/100)

        # RadioButton
        radio1 = ctk.CTkRadioButton(
            frame01,
            width=(screen_width * 1.3)/100,
            height=(screen_width * 1.3)/100,
            text="",
            variable=var,  # Compartilhando a mesma variável
            value=i + 1,   # Valor único para este botão
            fg_color="#0b2243",
            border_color="#A7BBCB",
            border_width_checked=(screen_width * 0.41)/100,
            command=lambda v = i: radio_button(v)
        )
        radio1.pack(side="left", padx=(screen_width * 0.9)/100, pady=(screen_width * 0.4)/100)

        # Combobox
        opcoes = ["Movimentação", "Oscilação"]
        global combobox
        combobox = ctk.CTkComboBox(
            frame01,
            values=opcoes,
            width=(screen_width * 15.63) / 100,
            height=(screen_height * 5.2) / 100,
            font=("Inter", fontsize, "bold"),
            dropdown_fg_color="#304462",
            fg_color="#0b2243",
            dropdown_text_color="#E0E0E0",
            button_color="#304462",
            text_color="#E0E0E0",
            corner_radius=12,
            border_width=3,
            border_color="#304462",
            button_hover_color="#0B2243",
            dropdown_hover_color="#0b2243",
            command=lambda line, v=i: combo_box(line, v),  # Passa o valor atual de `i`
        )
        combobox.set("Selecione uma opção")
        combobox.configure(state="disabled") 
        combobox.pack(side="right", padx=(screen_width * 0.9)/100, pady=(screen_width * 0.4)/100)
        combobox_criada.append(combobox)

#Essa função só chama se o raio botão relacionado está clicado - Criar verificação se o index selecionado do radio é o mesmo da combobox
def combo_box(line, idx):
    global index_combo
    index_combo = idx
    print(index_combo, line)
    if line == "Movimentação":
        mostrar_movimentacao()
    elif line == "Oscilação":
        mostrar_oscilacao()

def radio_button(value):
    global index_radio
    index_radio = value  # Atualiza o índice do radio selecionado
    print(f"Radio selecionado: {index_radio}")

    canvas_movimentacao.place_forget()
    canvas_oscilacao.place_forget()

    # Desativar todas as comboboxes
    for combobox in combobox_criada:
        combobox.configure(state="disabled")

    # Ativar apenas a combobox correspondente ao índice do radio
    if 0 <= index_radio < len(combobox_criada):
        combobox_criada[index_radio].configure(state="normal")

    # Restaurar valores se já existem na matriz
    if combobox_criada[index_radio].get() == "Movimentação":
        mostrar_movimentacao()
    elif combobox_criada[index_radio].get() == "Oscilação":
        mostrar_oscilacao()
    
gerar_widgets(rotina, 5, var)


def mostrar_movimentacao():
    canvas_movimentacao.place(relx=0.3453,rely=0.3491,anchor="nw")  # Exibe o canvas de movimentação
    canvas_oscilacao.place_forget()  # Oculta o canvas de oscilação
    configurar_canvas_movimentacao()  # Adiciona elementos ao canvas de movimentação

def mostrar_oscilacao():
    canvas_oscilacao.place(relx=0.3453,rely=0.3491,anchor="nw")  # Exibe o canvas de oscilação
    canvas_movimentacao.place_forget()  # Oculta o canvas de movimentação
    configurar_canvas_oscilacao()  # Adiciona elementos ao canvas de oscilação

def configurar_canvas_movimentacao():
    label_moldura01 = Label(canvas_movimentacao, image=moldura01, borderwidth=0, bg="#E0E7EC")
    label_moldura01.image = moldura01
    label_moldura01.place(relx=0.4664, rely= 0.4494, anchor = "center")

    label_moldura02 = Label(canvas_movimentacao, image=moldura02, borderwidth=0, bg="#E0E7EC")
    label_moldura02.image = moldura02
    label_moldura02.place(relx=0.6682, rely= 0.4494, anchor = "center")

    label_moldura03 = Label(canvas_movimentacao, image=moldura01, borderwidth=0, bg="#E0E7EC")
    label_moldura03.image = moldura01
    label_moldura03.place(relx=0.87, rely= 0.4494, anchor = "center")

    movimento_label = Label(canvas_movimentacao, text="MOVIMENTO", font=("Inter", 16, "bold"), background="#E0E7EC", fg="#304462")
    movimento_label.place(relx=0.2, rely= 0.1303, anchor = "center")

    matriz_parametros[index_radio][0] = "M"

    mov_label_i = Label(canvas_movimentacao, text="Tempo Inicial", font=("Inter", fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    mov_tempo_i = boxes.CustomSpinbox(
        canvas_movimentacao,
        min_value=0,
        max_value=9999,
        step=1,
        new_value=matriz_parametros[index_radio][1] if matriz_parametros[index_radio][1] != 0 else 0
    )
    mov_label_i.place(relx=0.4664, rely= 0.2180, anchor = "center")
    mov_tempo_i.place(relx=0.4664, rely = 0.3146, anchor = "center")

    mov_label_f = Label(canvas_movimentacao, text="Tempo Final", font=("Inter", fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    mov_tempo_f = boxes.CustomSpinbox(
        canvas_movimentacao,
        min_value=0,
        max_value=9999,
        step=1,
        new_value=matriz_parametros[index_radio][2] if matriz_parametros[index_radio][2] != 0 else 0
    )
    mov_label_f.place(relx=0.4664, rely= 0.5551, anchor = "center")
    mov_tempo_f.place(relx=0.4664, rely = 0.6472, anchor = "center")

    mov_label_vel = Label(canvas_movimentacao, text="Velocidade", font=("Inter", fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    mov_vel = boxes.CustomSpinbox(
        canvas_movimentacao,
        min_value=1,
        max_value=15,
        step=1,
        new_value=matriz_parametros[index_radio][3] if matriz_parametros[index_radio][3] != 0 else 1
    )
    mov_label_vel.place(relx=0.6682, rely = 0.38, anchor = "center")
    mov_vel.place(relx=0.6682, rely = 0.48, anchor = "center")

    mov_label_x = Label(canvas_movimentacao, text="Ângulo X", font=("Inter", fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    mov_x = boxes.CustomSpinbox(
        canvas_movimentacao,
        min_value=-25,
        max_value=25,
        step=1,
        new_value=matriz_parametros[index_radio][4] if matriz_parametros[index_radio][4] != 0 else -25
    )
    mov_label_x.place(relx=0.87, rely= 0.2180, anchor = "center")
    mov_x.place(relx=0.87, rely = 0.3146, anchor = "center")

    mov_label_y = Label(canvas_movimentacao, text="Ângulo Y", font=("Inter", fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    mov_y = boxes.CustomSpinbox(
        canvas_movimentacao,
        min_value=-25,
        max_value=25,
        step=1,
        new_value=matriz_parametros[index_radio][5] if matriz_parametros[index_radio][5] != 0 else -25
    )
    mov_label_y.place(relx=0.87, rely= 0.5551, anchor = "center")
    mov_y.place(relx=0.87, rely = 0.6472, anchor = "center")

    matriz_parametros[index_radio][6] = 0

    def confirmar_mov():
        valores = [
            mov_tempo_i.current_value.get(),  # Tempo inicial
            mov_tempo_f.current_value.get(),  # Tempo final
            mov_vel.current_value.get(),      # Velocidade
            mov_x.current_value.get(),        # Ângulo X
            mov_y.current_value.get(),        # Ângulo Y
    ]
    
        for j, valor in enumerate(valores):
            matriz_parametros[index_radio][j+1] = valor

        print(f"Matriz atualizada: {matriz_parametros}")

    btn_confirmar_mov = Button(
    canvas_movimentacao,
    text="CONFIRMAR",
    font=("Inter", fontsize14+2,"bold"),
    fg="#E0E0E0",
    image=bg_btn_conf,
    width=((screen_width * 7.92) / 100)-2,
    height=((screen_height * 5.5) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command= confirmar_mov
    #comando do botão precisa ter o get e o .append(matriz_parametros[index_selecionado][posição])
    )
    btn_confirmar_mov.place(relx=0.6655, rely=0.8854, anchor='center')


def configurar_canvas_oscilacao():
    label_moldura01 = Label(canvas_oscilacao, image=moldura01, borderwidth=0, bg="#E0E7EC")
    label_moldura01.image = moldura01
    label_moldura01.place(relx=0.4664, rely= 0.4494, anchor = "center")

    label_moldura02 = Label(canvas_oscilacao, image=moldura01, borderwidth=0, bg="#E0E7EC")
    label_moldura02.image = moldura01
    label_moldura02.place(relx=0.6682, rely= 0.4494, anchor = "center")

    label_moldura03 = Label(canvas_oscilacao, image=moldura01, borderwidth=0, bg="#E0E7EC")
    label_moldura03.image = moldura01
    label_moldura03.place(relx=0.87, rely= 0.4494, anchor = "center")

    oscilacao_label = Label(canvas_oscilacao, text="OSCILAÇÃO", font=("Inter", 16, "bold"), background="#E0E7EC", fg="#304462")
    oscilacao_label.place(relx=0.2, rely= 0.1303, anchor = "center")

    matriz_parametros[index_radio][0] = "O"
    osc_label_maxx = Label(canvas_oscilacao, text="Ângulo Max X", font=("Inter", fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    osc_maxx = boxes.CustomSpinbox(canvas_oscilacao,
        min_value=-25,
        max_value=25,
        step=1,
        new_value=matriz_parametros[index_radio][1] if matriz_parametros[index_radio][1] != 0 else -25)
    osc_label_maxx.place(relx=0.4664, rely= 0.2180, anchor = "center")
    osc_maxx.place(relx=0.4664, rely = 0.3146, anchor = "center")

    osc_label_minx = Label(canvas_oscilacao, text="Ângulo Min X", font=("Inter", fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    osc_minx = boxes.CustomSpinbox(canvas_oscilacao,
        min_value=-25,
        max_value=25,
        step=1,
        new_value=matriz_parametros[index_radio][2] if matriz_parametros[index_radio][2] != 0 else -25)
    osc_label_minx.place(relx=0.4664, rely= 0.5551, anchor = "center")
    osc_minx.place(relx=0.4664, rely = 0.6472, anchor = "center")

    osc_label_vel = Label(canvas_oscilacao, text="Velocidade", font=("Inter",fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    osc_vel = boxes.CustomSpinbox(canvas_oscilacao,
        min_value=1,
        max_value=15,
        step=1,
        new_value=matriz_parametros[index_radio][3] if matriz_parametros[index_radio][3] != 0 else 1)
    osc_label_vel.place(relx=0.6682, rely= 0.2180, anchor = "center")
    osc_vel.place(relx=0.6682, rely = 0.3146, anchor = "center")

    osc_label_rep = Label(canvas_oscilacao, text="Repetições", font=("Inter",fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    osc_rep = boxes.CustomSpinbox(canvas_oscilacao,
        min_value=1,
        max_value=9999,
        step=1,
        new_value=matriz_parametros[index_radio][4] if matriz_parametros[index_radio][4] != 0 else 1)
    osc_label_rep.place(relx=0.6682, rely= 0.5551, anchor = "center")
    osc_rep.place(relx=0.6682, rely = 0.6472, anchor = "center")

    osc_label_maxy = Label(canvas_oscilacao, text="Ângulo Max Y", font=("Inter", fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    osc_maxy = boxes.CustomSpinbox(canvas_oscilacao,
        min_value=-25,
        max_value=25,
        step=1,
        new_value=matriz_parametros[index_radio][5] if matriz_parametros[index_radio][5] != 0 else -25)
    osc_label_maxy.place(relx=0.87, rely= 0.2180, anchor = "center")
    osc_maxy.place(relx=0.87, rely = 0.3146, anchor = "center")

    osc_label_miny = Label(canvas_oscilacao, text="Ângulo Min Y", font=("Inter", fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    osc_miny = boxes.CustomSpinbox(canvas_oscilacao,
        min_value=-25,
        max_value=25,
        step=1,
        new_value=matriz_parametros[index_radio][6] if matriz_parametros[index_radio][6] != 0 else -25)
    osc_label_miny.place(relx=0.87, rely= 0.5551, anchor = "center")
    osc_miny.place(relx=0.87, rely = 0.6472, anchor = "center")

    def confirmar_osc():
        valores = [
            osc_maxx.current_value.get(),  # Max X
            osc_minx.current_value.get(),  # Min X
            osc_vel.current_value.get(),   # Velocidade
            osc_rep.current_value.get(),   # Repetição
            osc_maxy.current_value.get(),  # Max Y
            osc_miny.current_value.get(),  # Min Y
    ]
    
        for j, valor in enumerate(valores):
            matriz_parametros[index_radio][j+1] = valor

        print(f"Matriz atualizada: {matriz_parametros}")

    btn_confirmar_osc= Button(
    canvas_oscilacao,
    text="CONFIRMAR",
    font=("Inter", fontsize14+2,"bold"),
    fg="#E0E0E0",
    image=bg_btn_conf,
    width=((screen_width * 7.92) / 100)-2,
    height=((screen_height * 5.5) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command= confirmar_osc
    #comando do botão precisa ter o get e o .append(matriz_parametros[index_selecionado][posição])
    )
    btn_confirmar_osc.place(relx=0.6655, rely=0.8854, anchor='center')

btn_presets = Button(
    tela_parametros,
    text="PRESETS",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((screen_width * 9.9) / 100)-2,
    height=((screen_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
)
btn_presets.place(relx=0.1042, rely=0.8611)

#MARK: CANVAS CARREGAMENTO ---------------------------------------------------------------------------------------------------------------------------
canvas_carregamento = Canvas(tela_carregamento, width=screen_width, height=screen_height)
canvas_carregamento.grid(row=0, column=0)
canvas_carregamento.create_image(0, 0, image=bg_carregamento, anchor="nw")

fig3 = matplotlib.figure.Figure()
ax3 = fig3.add_subplot()

# Canvas Leitura
canvas_grafico_carregamento= Canvas(tela_carregamento, width=890, height=480, bg="white", highlightthickness=4, highlightbackground = "#8ca0b1")
canvas_grafico_carregamento.place(relx=0.5, rely=0.5, anchor="center")  # Centralizado na tela

canvasMatplot3 = FigureCanvasTkAgg(fig3, master = canvas_grafico_carregamento)
canvasMatplot3.get_tk_widget().pack()

#MARK: MANTER COLETA()
def ManterColeta():

    global PararColeta
    global Dados_CopX
    global Dados_CopY
    global Dados_Tempo
    global baud
    global porta1
    global ard1
    global start
    global loopColeta

    loopColeta = 1
    baud = 9600
    
    porta1 = "COM10" #Enviar dados para essa porta
    
    ard1 = serial.Serial(porta1, baud, timeout=0.01, writeTimeout=3) #Enviar dados para essa porta

    os.startfile("Project1\FileName.exe")  #Executa o programa de coleta de dados
    time.sleep(1) #Espera 1 segundo para o programa abrir e se conectar
    ard1.write(str.encode('#andre6')) # Nome do arquivo em que será salvo os dados (precisa ter o # antes)
    time.sleep(1) # Espera 1 segundo para o arquivo ser criado
    ard1.write(str.encode('I 0 0 0')) #Inicia a coleta

    Dados_CopX = [0]
    Dados_CopY = [0]
    Dados_Tempo = [0]


    show_frame(tela_carregamento)

    start = time.time()

    root.after(10, ColetarDados)


#MARK: COLETAR DADOS DO TEENSY

def ColetarDados():
    
    global baud
    global porta1
    global ard1
    global Dados_CopX
    global Dados_CopY
    global Dados_Tempo
    global start
   
    valueRead = ard1.readline()

    valueSplit = valueRead.split(b",")

    print(valueRead)

    if len(valueSplit) == 20:

        P0 = float(valueSplit[12])
        P1 = float(valueSplit[13])
        P2 = float(valueSplit[14])
        P3 = float(valueSplit[15])

        P4 = float(valueSplit[16])
        P5 = float(valueSplit[17])
        P6 = float(valueSplit[18])
        P7 = float(valueSplit[19])

        X = float(valueSplit[1])
        Y = float(valueSplit[2])

        T = time.time() - start

        DxP0= 16.8
        DyP0= 16
        DxP1= 3.4
        DyP1= 16.5
        DxP2= 3.4
        DyP2= 16
        DxP3= 17
        DyP3= 16

        DxP4= 3.5
        DyP4= 16
        DxP5= 17
        DyP5= 15.5
        DxP6= 17
        DyP6= 16
        DxP7= 3.8
        DyP7= 16

        if (P0+P1+P2+P3+P4+P5+P6+P7) > 0:
            CopX = (P4*DxP4 + P5*DxP5 + P6*DxP6 + P7*DxP7 - P0*DxP0 - P1*DxP1 - P2*DxP2 - P3*DxP3)/(P0+P1+P2+P3+P4+P5+P6+P7)
        else:
            CopX = 0

        if (P0+P1+P2+P3+P4+P5+P6+P7) > 0:
            CopY = (P0*DyP0 + P1*DyP1 + P4*DyP4 + P5*DyP5 - P2*DyP2 - P3*DyP3 - P6*DyP6 - P7*DyP7)/(P0+P1+P2+P3+P4+P5+P6+P7)
        else:
            CopY = 0

        Dados_CopX.append(CopX)
        Dados_CopY.append(CopY)
        Dados_Tempo.append(T)

        ax3.clear() #Limpa o grafico

        lineX = [0, 0, -20, -20, 20, 20, 0]
        lineY = [20, -20, -20, 20, 20, -20, -20]
        ax3.plot(lineX, lineY, color='#A7BBCB')
        ax3.plot(Dados_CopX, Dados_CopY, color='#304462')

        canvasMatplot3.draw() #Desenha o grafico

    if(loopColeta) == 1:
        root.after(10, ColetarDados)
    else: 
        ard1.write(str.encode('F 0 0 0')) #Interrompe a coleta
        time.sleep(1) #Espera 1 segundo para coletar todos os dados

        ard1.close() #Fecha a conexão com o Teensy
        subprocess.call("taskkill /f /im WindowsTerminal.exe", shell=True) #Fecha programa de coleta

        print(str(Dados_CopX) + " " + str(Dados_CopY) + " " + str(Dados_Tempo))


#MARK: TELA CARREGAMENTO ---------------------------------------------------------------------------------------------------------------------------

btn_iniciarCarregamento = Button(
    tela_parametros,
    text="COLETAR",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((screen_width * 9.9) / 100)-2,
    height=((screen_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: show_frame(tela_carregamento)
)
btn_iniciarCarregamento.place(relx=0.7969, rely=0.8611)

def PararColeta():
    global loopColeta

    loopColeta = 0


btn_parar = Button(
    tela_carregamento,
    text="PARAR",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((screen_width * 9.9) / 100)-2,
    height=((screen_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: PararColeta()
)
btn_parar.place(relx=0.1042, rely=0.8611)



#MARK: TELA RESULTADO -----------------------------------------------------------------------------------------------------------------------------------------

canvas_resultado = Canvas(tela_resultado, width=screen_width, height=screen_height)
canvas_resultado.grid(row=0, column=0)
canvas_resultado.create_image(0, 0, image=bg_resultado, anchor="nw")


# Canvas Detalhes
canvas_paciente = Canvas(
    tela_resultado,
    width=(screen_width * 46)/100,
    height=(screen_height * 60)/100,
    bg="#ffffff",
    highlightthickness=6,
    highlightcolor="#A7BBCB",
    highlightbackground="#A7BBCB"
    )
canvas_centro_pressao = Canvas(
    tela_resultado, 
    width=(screen_width * 46)/100, 
    height=(screen_height * 60)/100, 
    bg="#ffffff",
    highlightthickness=6,
    highlightcolor="#A7BBCB",
    highlightbackground="#A7BBCB"
    )
canvas_distr_massas = Canvas(
    tela_resultado,
    width=(screen_width * 46)/100,
    height=(screen_height * 60)/100,
    bg="#ffffff",
    highlightthickness=6,
    highlightcolor="#A7BBCB",
    highlightbackground="#A7BBCB"
    )
canvas_velocidade = Canvas(
    tela_resultado,
    width=(screen_width * 46)/100,
    height=(screen_height * 60)/100,
    bg="#ffffff",
    highlightthickness=6,
    highlightcolor="#A7BBCB",
    highlightbackground="#A7BBCB"
    )
canvas_emg = Canvas(
    tela_resultado,
    width=(screen_width * 46)/100,
    height=(screen_height * 60)/100,
    bg="#ffffff",
    highlightthickness=6,
    highlightcolor="#A7BBCB",
    highlightbackground="#A7BBCB"
    )

#MARK: Canvas Leitura ----------------------------------------------------------------------------------------------------------------------------------

#Label canvas leitura

fig2 = matplotlib.figure.Figure()
ax2 = fig2.add_subplot()

canvas_grafico_leitura = Canvas(canvas_centro_pressao, 
    width=(screen_width * 46)/100, 
    height=(screen_height * 60)/100, 
    bg="#ffffff",
    highlightthickness=6,
    highlightcolor="#A7BBCB",
    highlightbackground="#A7BBCB")
canvas_grafico_leitura.place(relx=0.5, rely=0.5, anchor="center")  # Centralizado na tela

canvasMatplot2 = FigureCanvasTkAgg(fig2, master = canvas_grafico_leitura)
canvasMatplot2.get_tk_widget().pack()

#vdcp_label = Label(canvas_velocidade, text="Velocidade do Centro de Pressão", font=("Helvetica", 16), fg="#24344D", bg= "#EBEBEB")
#vdcp_label.place(relx=0.5, rely=0.3, anchor="center")

#dx_label = Label(canvas_velocidade, text="DX", font=("Helvetica", 16), fg="#24344D", bg= "#EBEBEB")
#dx_label.place(relx=0.5, rely=0.5, anchor="center")

#dy_label = Label(canvas_velocidade, text="DY", font=("Helvetica", 16), fg="#24344D", bg= "#EBEBEB")
#dy_label.place(relx=0.5, rely=0.7, anchor="center")


#MARK: Ler Arquivo() --------------------------------------------------------------------------------------------------------------------------------------

def LerArquivo():
    print("Método para ler o arquivo")

    global D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11
    global P0, P1, P2, P3, P4, P5, P6, P7
    global allData0, allData1, allData2, allData3, allData4, allData5, allData6, allData7, allData8, allData9, allData10, allData11, allData12, allData13, allData14, allData15, allData16, allData17, allData18, allData19

    allData0 = [0]
    allData1 = [0]
    allData2 = [0]
    allData3 = [0]
    allData4 = [0]
    allData5 = [0]
    allData6 = [0]
    allData7 = [0]
    allData8 = [0]
    allData9 = [0]
    allData10 = [0]
    allData11 = [0]
    allData12 = [0]
    allData13 = [0]
    allData14 = [0]
    allData15 = [0]
    allData16 = [0]
    allData17 = [0]
    allData18 = [0]
    allData19 = [0]
    
    Dados_CopX = [0]
    Dados_CopY = [0]
    
    ax2.clear() #Limpa o grafico

    list_of_files = glob.glob('*.tsv') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)

    with open(latest_file) as file:
        Dados = csv.reader(file)

        for row in Dados:
            #print(row)

            valueSplit = str(row).split(",")
            #print(valueSplit)

            if len(valueSplit) == 20:

                D0 = re.sub("[^A-Z]", "", valueSplit[0])
                D1 = float(re.sub("[^0-9]", "", valueSplit[1]))
                D2 = float(re.sub("[^0-9]", "", valueSplit[2]))
                D3 = float(re.sub("[^0-9]", "", valueSplit[3]))
                D4 = float(re.sub("[^0-9]", "", valueSplit[4]))
                D5 = float(re.sub("[^0-9]", "", valueSplit[5]))
                D6 = float(re.sub("[^0-9]", "", valueSplit[6]))
                D7 = float(re.sub("[^0-9]", "", valueSplit[7]))
                D8 = float(re.sub("[^0-9]", "", valueSplit[8]))
                D9 = float(re.sub("[^0-9]", "", valueSplit[9]))
                D10 = float(re.sub("[^0-9]", "", valueSplit[10]))
                D11 = float(re.sub("[^0-9]", "", valueSplit[11]))
                
                P0 = float(re.sub("[^0-9]", "", valueSplit[12]))
                P1 = float(re.sub("[^0-9]", "", valueSplit[13]))
                P2 = float(re.sub("[^0-9]", "", valueSplit[14]))
                P3 = float(re.sub("[^0-9]", "", valueSplit[15]))

                P4 = float(re.sub("[^0-9]", "", valueSplit[16]))
                P5 = float(re.sub("[^0-9]", "", valueSplit[17]))
                P6 = float(re.sub("[^0-9]", "", valueSplit[18]))
                P7 = float(re.sub("[^0-9]", "", valueSplit[19]))

                allData0.append(D0)
                allData1.append(D1)
                allData2.append(D2)
                allData3.append(D3)
                allData4.append(D4)
                allData5.append(D5)
                allData6.append(D6)
                allData7.append(D7)
                allData8.append(D8)
                allData9.append(D9)
                allData10.append(D10)
                allData11.append(D11)
                allData12.append(P0)
                allData13.append(P1)
                allData14.append(P2)
                allData15.append(P3)
                allData16.append(P4)
                allData17.append(P5)
                allData18.append(P6)
                allData19.append(P7)

                DxP0= 16.8
                DyP0= 16
                DxP1= 3.4
                DyP1= 16.5
                DxP2= 3.4
                DyP2= 16
                DxP3= 17
                DyP3= 16

                DxP4= 3.5
                DyP4= 16
                DxP5= 17
                DyP5= 15.5
                DxP6= 17
                DyP6= 16
                DxP7= 3.8
                DyP7= 16

                if (P0+P1+P2+P3+P4+P5+P6+P7) > 0:
                    CopX = (P4*DxP4 + P5*DxP5 + P6*DxP6 + P7*DxP7 - P0*DxP0 - P1*DxP1 - P2*DxP2 - P3*DxP3)/(P0+P1+P2+P3+P4+P5+P6+P7)
                else:
                    CopX = 0

                if (P0+P1+P2+P3+P4+P5+P6+P7) > 0:
                    CopY = (P0*DyP0 + P1*DyP1 + P4*DyP4 + P5*DyP5 - P2*DyP2 - P3*DyP3 - P6*DyP6 - P7*DyP7)/(P0+P1+P2+P3+P4+P5+P6+P7)
                else:
                    CopY = 0

                Dados_CopX.append(CopX)
                Dados_CopY.append(CopY)

    lineX = [0, 0, -20, -20, 20, 20, 0]
    lineY = [20, -20, -20, 20, 20, -20, -20]
    ax2.plot(lineX, lineY, color='#A7BBCB')
    ax2.plot(Dados_CopX, Dados_CopY, color='#304462')

    canvasMatplot2.draw() #Desenha o grafico

    salvar_dados()


btn_avancarResultado = Button(
    tela_carregamento,
    text="RESULTADOS",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((screen_width * 9.9) / 100)-2,
    height=((screen_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    #MARK: Botão para carregar o arquivo do excel
    command=lambda: LerArquivo()
)
btn_avancarResultado.place(relx=0.7969, rely=0.8611)

# Posicionamento relativo
canvas_paciente.place(relx=0.4688, rely=0.213, anchor='nw')
canvas_centro_pressao.place(relx=0.4688, rely=0.213, anchor='nw')
canvas_distr_massas.place(relx=0.4688, rely=0.213, anchor='nw')
canvas_velocidade.place(relx=0.4688, rely=0.213, anchor='nw')
canvas_emg.place(relx=0.4688, rely=0.213, anchor='nw')


# Conteudo Painel PACIENTE


#Texto
#canvas_centro_pressao.create_text(395, 100, text="Centro de Pressão", font=("Arial", 20, "bold"), fill="#000000")
canvas_distr_massas.create_text(395, 100, text="Distribuição de Massa", font=("Arial", 20, "bold"), fill="#000000")
#canvas_velocidade.create_text(395, 100, text="Velocidade", font=("Arial", 20, "bold"), fill="#000000")
canvas_emg.create_text(395, 100, text="EMG", font=("Arial", 20, "bold"), fill="#000000")


#Botão Pressionado
width_btn_click = int((screen_width * 12.24) / 100)
height_btn_click = int((screen_height * 17.6) / 100)
bg_btn_click1 = Image.open("UI/Resultado/btn_clicked.png")
bg_btn_click1 = bg_btn_click1.resize((width_btn_click, height_btn_click), Image.Resampling.LANCZOS)
bg_btn_click = ImageTk.PhotoImage(bg_btn_click1)

fontsize22 = int((screen_height * 2) / 100)

#MARK: Exibir dados()
def exibir_dados_paciente():
    canvas_paciente.delete("all")  # Limpa o conteúdo do Canvas antes de exibir novos dados
    
     # Obtém as dimensões do Canvas
    canvas_width = canvas_paciente.winfo_width()
    canvas_height = canvas_paciente.winfo_height()

    # Suponha que `dados_paciente_lista` contenha [nome, idade, altura, peso]
    nome, idade, altura, peso, sexo = dados_paciente_lista

    # Posiciona cada texto usando valores relativos, sem armazenar coordenadas em variáveis
    canvas_paciente.create_text(canvas_width * 0.5, canvas_height * 0.1, 
                                text=f"{nome}", font=("Inter", fontsize22, "bold"), fill="#304462", anchor = "center")
    canvas_paciente.create_text(canvas_width * 0.5, canvas_height * 0.2, 
                                text=f"Idade: {idade} anos  |  Altura: {altura}cm  |  Peso: {peso}kg  |  Sexo: {sexo}", font=("Inter", fontsize-1), fill="#656565")
    canvas_paciente.create_text(canvas_width * 0.5, canvas_height * 0.28,
                                text="_________________________", font=("Inter", fontsize), fill="#A3A3A3", anchor="center")

def exibir_dados_velocidade():
    canvas_velocidade.delete("all")

    canvas_width = canvas_velocidade.winfo_width()
    canvas_height = canvas_velocidade.winfo_height()

    vdcp, dx, dy = dados_velocidade_lista

    canvas_velocidade.create_text(canvas_width * 0.5, canvas_height * 0.1, 
                                text=f"Velocidade do Centro de Pressao: {vdcp}", font=("Inter", fontsize22, "bold"), fill="#304462", anchor = "center")
    canvas_velocidade.create_text(canvas_width * 0.5, canvas_height * 0.2, 
                                text=f"DX: {dx}  |  DY: {dy}", font=("Inter", fontsize-1), fill="#656565")

# Função para exibir o canvas correto
def exibir_canvas(canvas):
    canvas_paciente.place_forget()
    canvas_distr_massas.place_forget()
    canvas_velocidade.place_forget()
    canvas_emg.place_forget()
    canvas_centro_pressao.place_forget()
    
    #Exibe o canvas selecionado
    canvas.place(relx=0.4688, rely=0.213, anchor='nw')

    if canvas == canvas_paciente:
        exibir_dados_paciente()

        btn_paciente.config(fg="#e0e0e0", image=bg_btn_paciente_click)
        btn_centro_pressao.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_distr_massas.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_emg.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_velocidade.configure(fg="#0B2243", image=bg_btn_resultado)

#MARK: Função do botão Centro de pressão 
    if canvas == canvas_centro_pressao:

        btn_paciente.config(fg="#0B2243", image = bg_btn_paciente)
        btn_centro_pressao.configure(fg="#E0E0E0", image=bg_btn_click)
        btn_distr_massas.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_emg.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_velocidade.configure(fg="#0B2243", image=bg_btn_resultado)

    if canvas == canvas_distr_massas:
        btn_paciente.config(fg="#0B2243", image = bg_btn_paciente)
        btn_centro_pressao.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_distr_massas.configure(fg="#E0E0E0", image=bg_btn_click)
        btn_emg.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_velocidade.configure(fg="#0B2243", image=bg_btn_resultado)

    if canvas == canvas_emg:
        btn_paciente.config(fg="#0B2243", image = bg_btn_paciente)
        btn_centro_pressao.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_distr_massas.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_emg.configure(fg="#E0E0E0", image=bg_btn_click)
        btn_velocidade.configure(fg="#0B2243", image=bg_btn_resultado)

    if canvas == canvas_velocidade:
        exibir_dados_velocidade()

        btn_paciente.config(fg="#0B2243", image = bg_btn_paciente)
        btn_centro_pressao.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_distr_massas.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_emg.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_velocidade.configure(fg="#e0e0e0", image=bg_btn_click)

# Array para armazenar os dados
dados_salvos = []

#MARK: SALVAR DADOS()
def salvar_dados():
    
    nome = dados_paciente_lista[0]
    idade = dados_paciente_lista[1]
    altura = dados_paciente_lista[2]
    peso = dados_paciente_lista[3]
    sexo = dados_paciente_lista[4]

    data = {
        'Nome': nome,
        'Idade': idade,
        'Altura': altura,
        'Peso': peso,
        'Sexo': sexo,
        'D0': allData0,
        'D1': allData1,
        'D2': allData2,
        'D3': allData3,
        'D4': allData4,
        'D5': allData5,
        'D6': allData6,
        'D7': allData7,
        'D8': allData8,
        'D9': allData9,
        'D10': allData10,
        'D11': allData11,
        'D12': allData12,
        'D13': allData13,
        'D14': allData14,
        'D15': allData15,
        'D16': allData16,
        'D17': allData17,
        'D18': allData18,
        'D19': allData19
    }

    df = pd.DataFrame(data)

    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', title="Salvar dados coletados",
                                                filetypes=[("Excel files", "*.xlsx")])
    try:
        df.to_excel(file_path, engine='openpyxl')
        messagebox.showinfo(title=None, message="Salvo com sucesso!")
    except:
        print("Erro ao salvar")

    show_frame(tela_resultado)
    exibir_canvas(canvas_paciente)


#Background Botões
width_paciente = int((screen_width * 26.56) / 100)
height_paciente = int((screen_height * 6.48) / 100)
bg_btn_paciente1 = Image.open("UI/Resultado/btn_paciente_neutro.png")
bg_btn_paciente1 = bg_btn_paciente1.resize((width_paciente, height_paciente), Image.Resampling.LANCZOS)
bg_btn_paciente = ImageTk.PhotoImage(bg_btn_paciente1)

bg_btn_paciente_click1 = Image.open("UI/Resultado/btn_paciente_click.png")
bg_btn_paciente_click1 = bg_btn_paciente_click1.resize((width_paciente, height_paciente), Image.Resampling.LANCZOS)
bg_btn_paciente_click = ImageTk.PhotoImage(bg_btn_paciente_click1)

width_btn_resultado = int((screen_width * 12.24) / 100)
height_btn_resultado = int((screen_height * 17.6) / 100)
bg_btn_resultado1 = Image.open("UI/Resultado/btn_neutro.png")
bg_btn_resultado1 = bg_btn_resultado1.resize((width_btn_resultado, height_btn_resultado), Image.Resampling.LANCZOS)
bg_btn_resultado = ImageTk.PhotoImage(bg_btn_resultado1)


# Botões laterais
btn_paciente = Button(
    tela_resultado,
    text="PACIENTE",
    font=("Inter", fontsize22,"bold"),
    fg="#0B2243",
    image=bg_btn_paciente,
    width=(width_paciente-2),
    height=(height_paciente-2),
    compound="center",
    bd=0,
    activeforeground="#E0E0E0",
    command=lambda: exibir_canvas(canvas_paciente)
)
btn_paciente.place(relx=0.1042, rely=0.2778, anchor = 'nw')

btn_centro_pressao = Button(
    tela_resultado,
    text="CENTRO DE\nPRESSÃO",
    font=("Inter", fontsize22,"bold"),
    fg="#0B2243",
    image=bg_btn_resultado,
    width=(width_btn_resultado-2),
    height=(height_btn_resultado-2),
    compound="center",
    bd=0,
    activeforeground="#E0E0E0",
    command=lambda: exibir_canvas(canvas_centro_pressao)
)
btn_centro_pressao.place(relx=0.1042, rely=0.376, anchor = 'nw')

btn_distr_massas = Button(
    tela_resultado,
    text="DISTRIBUIÇÃO\nDE MASSA",
    font=("Inter", fontsize22,"bold"),
    fg="#0B2243",
    image=bg_btn_resultado,
    width=(width_btn_resultado-2),
    height=(height_btn_resultado-2),
    compound="center",
    bd=0,
    activeforeground="#E0E0E0",
    command=lambda: exibir_canvas(canvas_distr_massas)
)
btn_distr_massas.place(relx=0.2474, rely=0.3759, anchor = 'nw')

btn_velocidade = Button(
    tela_resultado,
    text="VELOCIDADE",
    font=("Inter", fontsize22,"bold"),
    fg="#0B2243",
    image=bg_btn_resultado,
    width=(width_btn_resultado-2),
    height=(height_btn_resultado-2),
    compound="center",
    bd=0,
    activeforeground="#E0E0E0",
    command=lambda: exibir_canvas(canvas_velocidade)
)
btn_velocidade.place(relx=0.1042, rely=0.5880, anchor = 'nw')

btn_emg = Button(
    tela_resultado,
    text="EMG",
    font=("Inter", fontsize22,"bold"),
    fg="#0B2243",
    image=bg_btn_resultado,
    width=(width_btn_resultado-2),
    height=(height_btn_resultado-2),
    compound="center",
    bd=0,
    activeforeground="#E0E0E0",
    command=lambda: exibir_canvas(canvas_emg)
)
btn_emg.place(relx=0.2474, rely=0.5880, anchor = 'nw')

def restart(frame): 
    frame.tkraise()
    canvas_paciente.delete("all")
    canvas_centro_pressao.delete("all")
    canvas_distr_massas.delete("all")
    canvas_velocidade.delete("all")
    canvas_emg.delete("all")

btn_voltarInicial = Button(
    tela_resultado,
    text="VOLTAR",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((screen_width * 9.9) / 100)-2,
    height=((screen_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: restart(tela_inicial))
btn_voltarInicial.place(relx= 0.1042, rely=0.8611)

btn_fechar2 = ctk.CTkButton(
    tela_resultado,
    text="X",
    font=("Inter", 16, "bold"),
    corner_radius=14,
    width=47,
    height=37,
    text_color="#ffffff", 
    fg_color="#3e567c",
    hover_color="#2b3a52",
    command=lambda: close_app()
)
btn_fechar2.place(relx=0.97, rely=0.002)

root.mainloop()