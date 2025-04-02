from tkinter import *
from tkinter import *
from tkinter import PhotoImage
from tkinter import messagebox
from PIL import Image, ImageTk 
import customtkinter as ctk
import boxes
import validates
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
import ctypes
import textwrap
import pyautogui
from screeninfo import get_monitors


# Ajuste de DPI
ctypes.windll.shcore.SetProcessDpiAwareness(2)

# Resolução física e escala de DPI
user32 = ctypes.windll.user32
physical_width = user32.GetSystemMetrics(0)
physical_height = user32.GetSystemMetrics(1)

dpi = ctypes.windll.shcore.GetScaleFactorForDevice(0)
scale_factor = dpi / 100

# Obtendo monitores
monitors = get_monitors()
if len(monitors) < 2:
    print("É necessário pelo menos dois monitores.")
    exit()

monitor1 = monitors[1]
monitor2 = monitors[0]  # Segundo monitor

# Criando a Janela Principal (Monitor 1)
root = ctk.CTk()
root.title("EquiSystem K2000")
screen_width = int(physical_width / scale_factor)
screen_height = int(physical_height / scale_factor)
root.geometry(f"{screen_width}x{screen_height}")
root.minsize(width=1280, height=720)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.attributes("-fullscreen", True)

root.iconbitmap("UI/icon.ico") 
myappid = "K2000.V1"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Criando a Janela Secundária (Monitor 2)
second_window = ctk.CTkToplevel(root)
second_window.geometry(f"{monitor2.width}x{monitor2.height}+{monitor2.x}+{monitor2.y}")
second_window.overrideredirect(True)  # Remove bordas da janela
second_window.attributes("-topmost", True)  # Mantém a janela sempre no topo

# Carregar a imagem de fundo para o segundo monitor
bg_inicial1 = Image.open("UI/bg_inicial.png")
bg_inicial1 = bg_inicial1.resize((monitor2.width, monitor2.height), Image.LANCZOS)
bg_inicial = ImageTk.PhotoImage(bg_inicial1)

bg_label = ctk.CTkLabel(second_window, image=bg_inicial, text="")
bg_label.pack(fill="both", expand=True)

# Criando as telas do software principal
tela_inicial = ctk.CTkFrame(root)
tela_dados = ctk.CTkFrame(root)
tela_parametros = ctk.CTkFrame(root)
tela_anamnese = ctk.CTkFrame(root)
tela_resultado = ctk.CTkFrame(root)
tela_carregamento = ctk.CTkFrame(root)

# Função para trazer a tela pra frente
def show_frame(frame): 
    frame.tkraise()

def close_app():
    root.destroy()

# Posicionando as telas
for frame in (tela_inicial, tela_dados, tela_parametros, tela_resultado, tela_anamnese, tela_carregamento): 
    frame.grid(row=0, column=0, sticky='nsew')

show_frame(tela_inicial)
#show_frame(tela_parametros)

#Background Telas
bg_geral1 = Image.open("UI/background.png")
bg_geral1 = bg_geral1.resize((physical_width, physical_height), Image.LANCZOS)
bg_geral = ImageTk.PhotoImage(bg_geral1)

bg_inicial1 = Image.open("UI/bg_inicial.png")
bg_inicial1 = bg_inicial1.resize((physical_width, physical_height), Image.LANCZOS)
bg_inicial = ImageTk.PhotoImage(bg_inicial1)

bg_dados1 = Image.open("UI/bg_dados.png")
bg_dados1 = bg_dados1.resize((physical_width, physical_height), Image.LANCZOS)
bg_dados = ImageTk.PhotoImage(bg_dados1)

bg_anamnese1 = Image.open("UI/bg_anamnese.png")
bg_anamnese1 = bg_anamnese1.resize((physical_width, physical_height), Image.LANCZOS)
bg_anamnese = ImageTk.PhotoImage(bg_anamnese1)

bg_parametros1 = Image.open("UI/bg_parametros.png")
bg_parametros1 = bg_parametros1.resize((physical_width, physical_height), Image.LANCZOS)
bg_parametros = ImageTk.PhotoImage(bg_parametros1)

bg_carregamento1 = Image.open("UI/bg_carregamento.png")
bg_carregamento1 = bg_carregamento1.resize((physical_width, physical_height), Image.LANCZOS)
bg_carregamento = ImageTk.PhotoImage(bg_carregamento1)

bg_resultado1 = Image.open("UI/Resultado/bg_resultado.png")
bg_resultado1 = bg_resultado1.resize((physical_width, physical_height), Image.LANCZOS)
bg_resultado = ImageTk.PhotoImage(bg_resultado1)

#Bg botão geral 
width_bg_btn = int((physical_width * 9.9) / 100) 
height_bg_btn = int((physical_height * 9.26) / 100) 
bg_btn1 = Image.open("UI/bg_btn.png")
bg_btn1 = bg_btn1.resize((width_bg_btn, height_bg_btn), Image.Resampling.LANCZOS)
bg_btn = ImageTk.PhotoImage(bg_btn1)

#Bg botão fechar
width_bg_btnfechar = int((physical_width * 5.73) / 100)
height_bg_btnfechar = int((physical_height * 8.33) / 100)
bg_btnfechar1 = Image.open("UI/btn_fechar.png")
bg_btnfechar1 = bg_btnfechar1.resize((width_bg_btnfechar, height_bg_btnfechar), Image.Resampling.LANCZOS)
bg_btnfechar = ImageTk.PhotoImage(bg_btnfechar1)

#Variavel para tamanho de vonte dos botões gerais
fontsize = int((screen_height * 1.83) / 100)

fontsize14 = int((screen_height * 1.30) / 100)

fontsize22 = int((screen_height * 2) / 100)

#MARK: TELA INICIAL --------------------------------------------------------------------------------------------------------------

canvas_inicial = Canvas(tela_inicial, width=physical_width, height=physical_height)
canvas_inicial.grid(row=0, column=0)
canvas_inicial.create_image(0, 0, image=bg_inicial, anchor="nw")

# Botão de fechar
btn_fechar = Button(
    tela_inicial,
    image=bg_btnfechar,
    width=((physical_width * 5.73) / 100)-2,
    height=((physical_height * 8.33) / 100)-2,
    compound="center",
    bd=0,
    command=lambda: close_app()
)
btn_fechar.place(relx=0.975, rely=-0.05)


# Título

# Configuração de Botões Inicial
btn_iniciar = Button(
    tela_inicial,
    text="INICIAR",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((physical_width * 9.9) / 100)-2,
    height=((physical_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: show_frame(tela_dados) 
)
btn_iniciar.place(relx=0.5, rely=0.8611, anchor='center')

#MARK: TELA DADOS ----------------------------------------------------------------------------------------------------------

canvas_dados = Canvas(tela_dados, width=physical_width, height=physical_height)
canvas_dados.grid(row=0, column=0)
canvas_dados.create_image(0, 0, image=bg_dados, anchor="nw")

# Registra as funções de validação
validacao_nome = tela_dados.register(validates.validar_nome)
validacao_idade = tela_dados.register(validates.validar_idade)
validacao_altura = tela_dados.register(validates.validar_altura)
validacao_peso = tela_dados.register(validates.validar_peso)

btn_fechar_dados = Button(
    tela_dados,
    image=bg_btnfechar,
    width=((physical_width * 5.73) / 100)-2,
    height=((physical_height * 8.33) / 100)-2,
    compound="center",
    bd=0,
    command=lambda: close_app()
)
btn_fechar_dados.place(relx=0.975, rely=-0.05)

# Variável para controlar se o teclado já foi aberto
teclado_aberto = False

def abrir_teclado():
    global teclado_aberto
    if not teclado_aberto:
        pyautogui.hotkey('win', 'ctrl', 'o')  # Abre o teclado virtual
        teclado_aberto = True

def fechar_teclado():
    global teclado_aberto
    if teclado_aberto:
        pyautogui.hotkey('esc')  # A tecla 'esc' pode ser usada para fechar o teclado
        teclado_aberto = False
        tela_dados.focus_set()  # Remove o foco da entrada, desfocando a entrada

def on_focus_out(event):
    fechar_teclado()

def on_enter_pressed(event):
    fechar_teclado()


# Entradas de dados do paciente
entradas = []

nome_label = Label(tela_dados, text="Nome:", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
nome_label.place(relx=0.0901, rely=0.2907, anchor= "center")
nome_paciente = ctk.CTkEntry(tela_dados, width=(screen_width *38.28/100), height=(screen_height * 6.02/100), fg_color="#FFFFFF", text_color="#2F2F2F", font=("Inter", 16, "bold"),
                             bg_color="#D1DCE4", border_color="#A7BBCB", border_width=3, corner_radius=12, validate="key", validatecommand=(validacao_nome, "%P"))
nome_paciente.place(relx=0.2547, rely=0.3391, anchor = "center")

nome_paciente.bind("<FocusIn>", lambda event: abrir_teclado())
nome_paciente.bind("<Return>", on_enter_pressed)
nome_paciente.bind("<FocusOut>", on_focus_out)

idade_label = Label(tela_dados, text="Idade:", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
idade_label.place(relx=0.0891, rely=0.4431, anchor = "center")
idade_paciente = ctk.CTkEntry(tela_dados, width=(screen_width * 18.23/100), height=(screen_height * 6.02/100), fg_color="#FFFFFF", text_color="#2F2F2F", font=("Inter", 16, "bold"),
                              bg_color="#D1DCE4", border_color="#A7BBCB", border_width=3, corner_radius=12, validate="key", validatecommand=(validacao_idade, "%P"))
idade_paciente.place(relx=0.1542, rely=0.4965, anchor = "center")

idade_paciente.bind("<FocusIn>", lambda event: abrir_teclado())
idade_paciente.bind("<Return>", on_enter_pressed)
idade_paciente.bind("<FocusOut>", on_focus_out)

altura_label = Label(tela_dados, text="Altura:", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
altura_label.place(relx=0.2943, rely=0.4431, anchor = "center")
altura_paciente = ctk.CTkEntry(tela_dados, width=(screen_width *18.23/100), height=(screen_height * 6.02/100),fg_color="#FFFFFF", text_color="#2F2F2F", font=("Inter", 16, "bold"),
                               bg_color="#D1DCE4", border_color="#A7BBCB", border_width=3, corner_radius=12, validate="key", validatecommand=(validacao_altura, "%P"))
altura_paciente.place(relx=0.3547, rely=0.4965, anchor = "center")

altura_paciente.bind("<FocusIn>", lambda event: abrir_teclado())
altura_paciente.bind("<Return>", on_enter_pressed)
altura_paciente.bind("<FocusOut>", on_focus_out)

peso_label = Label(tela_dados, text="Peso:", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
peso_label.place(relx=0.0870, rely=0.6003, anchor = "center")
peso_paciente = ctk.CTkEntry(tela_dados,width=(screen_width *18.23/100), height=(screen_height * 6.02/100), fg_color="#FFFFFF", text_color="#2F2F2F", font=("Inter", 16, "bold"),
                             bg_color="#D1DCE4", border_color="#A7BBCB", border_width=3, corner_radius=12, validate="key", validatecommand=(validacao_peso, "%P"))
peso_paciente.place(relx=0.1542, rely=0.6527, anchor = "center")

peso_paciente.bind("<FocusIn>", lambda event: abrir_teclado())
peso_paciente.bind("<Return>", on_enter_pressed)
peso_paciente.bind("<FocusOut>", on_focus_out)

seta_comboboxPil = Image.open("UI/seta_combobox.png")
img_seta = ctk.CTkImage(dark_image=seta_comboboxPil, light_image=seta_comboboxPil, size=(18, 12))
sexo_label = Label(tela_dados, text="Sexo:", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
sexo_label.place(relx=0.2911, rely=0.6003, anchor = "center")
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
sexo_paciente.place(relx=0.3547, rely=0.6527, anchor = "center")

def radio_selection(variable, entry, place_holder):
    # Obtém o valor atual da variável
    value = variable.get()

    if value == "1":  # Verifica se o valor é "1" (Sim)
        if variable == var_dor:  # Verifica qual variável está ativa
            place_holder.place(relx=0.5, rely=0.5, anchor="center")
            entry.place(relx=0.8266, rely=0.3093, anchor = "center")
            entradas.append(dor_entrada)
        elif variable == var_queda:
            place_holder.place(relx=0.5, rely=0.5, anchor="center")
            entry.place(relx=0.8266, rely=0.4463, anchor="center")
            entradas.append(queda_entrada)
        elif variable == var_labirintite:
            place_holder.place(relx=0.5, rely=0.5, anchor="center")
            entry.place(relx=0.8266, rely=0.5843, anchor = "center")
            entradas.append(labirintite_entrada)
    else:  # Se não for "1" (Sim), remove a entrada
        entry.place_forget()
        place_holder.place_forget()  # Remove a entrada da tela

# Anamnese

# Inicialização das variáveis
var_dor = StringVar()  # Default: Não
var_queda = StringVar()  # Default: Não
var_labirintite = StringVar()  # Default: Não
var_membroDom = StringVar()

# Inicialização das verificações
validacao_dor = tela_dados.register(lambda valor: validates.validar_dor(valor, dor_placeholder))
validacao_queda = tela_dados.register(lambda valor: validates.validar_queda(valor, queda_placeholder))
validacao_labirintite = tela_dados.register(lambda valor: validates.validar_labirintite(valor, labirintite_placeholder))

# Dor
dor_label = Label(tela_dados, text="Tem dor?", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
dor_label.place(relx=0.5698, rely=0.2546, anchor = "center")

radio_dor_nao = ctk.CTkRadioButton(
        tela_dados,
        width=(screen_width * 1.3)/100,
        height=(screen_width * 1.3)/100,
        text="",
        variable=var_dor,
        value=2,
        fg_color="#0b2243",
        border_color="#577B8E",
        bg_color="#D1DCE4",
        border_width_checked=(screen_width * 0.41)/100,
        command=lambda: radio_selection(var_dor, dor_entrada, dor_placeholder)
        )
radio_dor_nao.place(relx= 0.5495, rely = 0.3093, anchor = 'center')
   
radio_dor_sim = ctk.CTkRadioButton(
        tela_dados,
        width=(screen_width * 1.7)/100,
        height=(screen_width * 1.7)/100,
        text="",
        variable=var_dor,
        value=1,
        fg_color="#0b2243",
        border_color="#577B8E",
        bg_color="#D1DCE4",
        border_width_checked=(screen_width * 0.41)/100,
        command=lambda: radio_selection(var_dor, dor_entrada, dor_placeholder)
        )
radio_dor_sim.place(relx= 0.6708, rely = 0.3093, anchor = 'center')

dor_nao_label = Label(tela_dados, text="NÃO", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
dor_nao_label.place(relx= 0.5776, rely = 0.3093, anchor = 'center')

dor_sim_label = Label(tela_dados, text="SIM", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
dor_sim_label.place(relx= 0.6944, rely = 0.3093, anchor = 'center')

dor_entrada = ctk.CTkEntry(tela_dados, width=(screen_width * 19.79/100), height=(screen_height * 6.02/100), fg_color="#FFFFFF", text_color="#2F2F2F", font=("Inter", fontsize, "bold"),bg_color="#D1DCE4", border_color="#A7BBCB", border_width=3, corner_radius=12,
    validate="key", validatecommand=(validacao_dor, "%P"))

dor_entrada.bind("<FocusIn>", lambda event: abrir_teclado())
dor_entrada.bind("<Return>", on_enter_pressed)
dor_entrada.bind("<FocusOut>", on_focus_out)

# Queda
queda_label = Label(tela_dados, text="Evento de queda no último ano?", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
queda_label.place(relx=0.6380, rely=0.3926, anchor = 'center')

radio_queda_nao = ctk.CTkRadioButton(
        tela_dados,
        width=(screen_width * 1.3)/100,
        height=(screen_width * 1.3)/100,
        text="",
        variable=var_queda,
        value=2,  # Corrigindo o índice para sempre ser sequencial
        fg_color="#0b2243",
        border_color="#577B8E",
        bg_color="#D1DCE4",
        border_width_checked=(screen_width * 0.41)/100,
        command=lambda: radio_selection(var_queda, queda_entrada, queda_placeholder)
        )
radio_queda_nao.place(relx= 0.5495, rely=0.4463, anchor = "center")

radio_queda_sim = ctk.CTkRadioButton(
        tela_dados,
        width=(screen_width * 1.3)/100,
        height=(screen_width * 1.3)/100,
        text="",
        variable=var_queda,
        value=1,  # Corrigindo o índice para sempre ser sequencial
        fg_color="#0b2243",
        border_color="#577B8E",
        bg_color="#D1DCE4",
        border_width_checked=(screen_width * 0.41)/100,
        command=lambda: radio_selection(var_queda, queda_entrada, queda_placeholder)
        )
radio_queda_sim.place(relx= 0.6708, rely=0.4463, anchor = "center")

queda_nao_label = Label(tela_dados, text="NÃO", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
queda_nao_label.place(relx= 0.5776, rely=0.4463, anchor = "center")

queda_sim_label = Label(tela_dados, text="SIM", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
queda_sim_label.place(relx= 0.6944, rely=0.4463, anchor = "center")

queda_entrada = ctk.CTkEntry(tela_dados, width=(screen_width * 19.79/100), height=(screen_height * 6.02/100), fg_color="#FFFFFF", text_color="#2F2F2F", font=("Inter", fontsize, "bold"),bg_color="#D1DCE4", border_color="#A7BBCB", border_width=3, corner_radius=12,
    validate="key", validatecommand=(validacao_queda, "%P"))

queda_entrada.bind("<FocusIn>", lambda event: abrir_teclado())
queda_entrada.bind("<Return>", on_enter_pressed)
queda_entrada.bind("<FocusOut>", on_focus_out)

# Labirintite
labirintite_label = Label(tela_dados, text="Crise de labirintite no último mês?", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
labirintite_label.place(relx=0.6438, rely=0.5306, anchor = 'center')

radio_labirintite_nao = ctk.CTkRadioButton(
        tela_dados,
        width=(screen_width * 1.3)/100,
        height=(screen_width * 1.3)/100,
        text="",
        variable=var_labirintite,
        value=2,  # Corrigindo o índice para sempre ser sequencial
        fg_color="#0b2243",
        border_color="#577B8E",
        bg_color="#D1DCE4",
        border_width_checked=(screen_width * 0.41)/100,
        command=lambda: radio_selection(var_labirintite, labirintite_entrada, labirintite_placeholder)
        )
radio_labirintite_nao.place(relx= 0.5495, rely = 0.5843, anchor = "center")

radio_labirintite_sim = ctk.CTkRadioButton(
        tela_dados,
        width=(screen_width * 1.3)/100,
        height=(screen_width * 1.3)/100,
        text="",
        variable=var_labirintite,
        value=1,  # Corrigindo o índice para sempre ser sequencial
        fg_color="#0b2243",
        border_color="#577B8E",
        bg_color="#D1DCE4",
        border_width_checked=(screen_width * 0.41)/100,
        command=lambda: radio_selection(var_labirintite, labirintite_entrada, labirintite_placeholder)
        )
radio_labirintite_sim.place(relx= 0.6708, rely = 0.5843, anchor = "center")

labirintite_nao_label = Label(tela_dados, text="NÃO", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
labirintite_nao_label.place(relx= 0.5776, rely = 0.5843, anchor = "center")

labirintite_sim_label = Label(tela_dados, text="SIM", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
labirintite_sim_label.place(relx= 0.6944, rely = 0.5843, anchor = "center")

labirintite_entrada = ctk.CTkEntry(tela_dados, width=(screen_width * 19.79/100), height=(screen_height * 6.02/100), fg_color="#FFFFFF", text_color="#2F2F2F", font=("Inter", fontsize, "bold"),bg_color="#D1DCE4", border_color="#A7BBCB", border_width=3, corner_radius=12,
    validate="key", validatecommand=(validacao_labirintite, "%P"))

labirintite_entrada.bind("<FocusIn>", lambda event: abrir_teclado())
labirintite_entrada.bind("<Return>", on_enter_pressed)
labirintite_entrada.bind("<FocusOut>", on_focus_out)

#Membro Dominante
membroDom_label = Label(tela_dados, text="Membro Dominante", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
membroDom_label.place(relx=0.6005, rely=0.6685, anchor = "center")

radio_membro_esq = ctk.CTkRadioButton(
        tela_dados,
        width=(screen_width * 1.3)/100,
        height=(screen_width * 1.3)/100,
        text="",
        variable=var_membroDom,
        value=2,
        fg_color="#0b2243",
        border_color="#577B8E",
        bg_color="#D1DCE4",
        border_width_checked=(screen_width * 0.41)/100,
        )
radio_membro_esq.place(relx= 0.5495, rely = 0.7222, anchor = 'center')
   
radio_membro_dir = ctk.CTkRadioButton(
        tela_dados,
        width=(screen_width * 1.7)/100,
        height=(screen_width * 1.7)/100,
        text="",
        variable=var_membroDom,
        value=1,
        fg_color="#0b2243",
        border_color="#577B8E",
        bg_color="#D1DCE4",
        border_width_checked=(screen_width * 0.41)/100,
        )
radio_membro_dir.place(relx= 0.6708, rely = 0.7222, anchor = 'center')

membroEsq_label = Label(tela_dados, text="ESQUERDO", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
membroEsq_label.place(relx= 0.599, rely = 0.7222, anchor = 'center')

membroDir_label = Label(tela_dados, text="DIREITO", font=("Inter", fontsize, "bold"), background="#D1DCE4", fg="#2F2F2F")
membroDir_label.place(relx= 0.7073, rely = 0.7222, anchor = 'center')

queda_placeholder = Label(queda_entrada, text="Quantos?", font=("Inter", fontsize, "bold"), background="#FFFFFF", fg="#CDCDCD")
dor_placeholder = Label(dor_entrada, text="Qual nível? (0 a 10)", font=("Inter", fontsize, "bold"), background="#FFFFFF", fg="#CDCDCD")
labirintite_placeholder = Label(labirintite_entrada, text="Tratamento utilizado?", font=("Inter", fontsize, "bold"), background="#FFFFFF", fg="#CDCDCD")

# Função para armazenar os dados em uma lista
global dados_paciente_lista
dados_paciente_lista = []
dados_velocidade_lista = []

def armazenar_dados():
    global dados_paciente_lista
    # Dados básicos
    nome = nome_paciente.get().strip()
    idade = idade_paciente.get().strip()
    altura = altura_paciente.get().strip()
    peso = peso_paciente.get().strip()
    sexo = sexo_paciente.get().strip()

    # Coleta de respostas da Anamnese
    tem_dor = "Sim" if var_dor.get() == "1" else "Não" if var_dor.get() == "2" else ""
    nivel_dor = dor_entrada.get().strip() if tem_dor == "Sim" else "0"

    tem_queda = "Sim" if var_queda.get() == "1" else "Não" if var_queda.get() == "2" else ""
    qtd_quedas = queda_entrada.get().strip() if tem_queda == "Sim" else "0"

    tem_labirintite = "Sim" if var_labirintite.get() == "1" else "Não" if var_labirintite.get() == "2" else ""
    tratamento_labirintite = labirintite_entrada.get().strip() if tem_labirintite == "Sim" else "Nenhum"

    membroDominante = "Direito" if var_membroDom.get() == "1" else "Esquerdo" if var_membroDom.get() == "2" else ""

    # Verificação dos campos obrigatórios
    if not all([nome, idade, altura, peso, sexo, tem_dor, tem_queda, tem_labirintite, membroDominante]):
        messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios!")
        return
    
    # Verificação das entradas condicionais
    if tem_dor == "Sim" and not nivel_dor:
        messagebox.showwarning("Atenção", "Você marcou que tem dor, mas não especificou o nível da dor!")
        return
    if tem_queda == "Sim" and not qtd_quedas:
        messagebox.showwarning("Atenção", "Você marcou que teve queda, mas não especificou a quantidade de quedas!")
        return
    if tem_labirintite == "Sim" and not tratamento_labirintite:
        messagebox.showwarning("Atenção", "Você marcou que tem labirintite, mas não especificou o tratamento!")
        return

    # Lista com todos os dados organizados
    dados_paciente_lista = [
        nome, idade, altura, peso, sexo,  # Dados básicos
        tem_dor, nivel_dor,               # Dados sobre dor
        tem_queda, qtd_quedas,            # Dados sobre quedas
        tem_labirintite, tratamento_labirintite,  # Dados sobre labirintite
        membroDominante
        
    ]

    print(dados_paciente_lista)

    # Resetando os checkboxes e entradas condicionais
    var_dor.set(0)
    var_queda.set(0)
    var_labirintite.set(0)
    var_membroDom.set(0)

    dor_entrada.place_forget()
    queda_entrada.place_forget()
    labirintite_entrada.place_forget()

    dor_entrada.delete(0, "end")
    queda_entrada.delete(0, "end")
    labirintite_entrada.delete(0, "end")

    nome_paciente.delete(0, "end")
    altura_paciente.delete(0, "end")
    peso_paciente.delete(0, "end")
    idade_paciente.delete(0, "end")
    sexo_paciente.reset_button_text()

    messagebox.showinfo("Sucesso", "Dados cadastrados com sucesso!")
    show_frame(tela_parametros)
    return dados_paciente_lista

#MARK: Carregar perfil
def CarregarPerfil():
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    Dados = pd.read_excel(filename)

    global allData4, allData5, allData6, allData7, allData8, allData9, allData10, allData11

    allData4 = [0]
    allData5 = [0]
    allData6 = [0]
    allData7 = [0]
    allData8 = [0]
    allData9 = [0]
    allData10 = [0]
    allData11 = [0]

    Dados_CopX = [0]
    Dados_CopY = [0]

    num = 0

    nome_paciente = Dados.Nome[0]
    idade_paciente = Dados.Idade[0]
    altura_paciente = Dados.Altura[0]
    peso_paciente = Dados.Peso[0]
    sexo_paciente = Dados.Sexo[0]
    tem_dor = Dados.Dor[0]
    nivel_dor = Dados.Nivel_da_dor[0]
    tem_queda = Dados.Queda[0]
    qtd_quedas = Dados.Quantidade_de_quedas[0]
    tem_labirintite = Dados.Labirintite[0]
    tratamento_labirintite = Dados.Tratamento_de_labirintite[0]
    vdcp = Dados.Tempo[0]
    Dx = Dados.Dx[0]
    Dy = Dados.Dy[0]

    for index in Dados.iterrows():

        D0 = Dados.D0[num]
        D1 = Dados.D1[num]
        D2 = Dados.D2[num]
        D3 = Dados.D3[num]

        D4 = Dados.D4[num]
        D5 = Dados.D5[num]
        D6 = Dados.D6[num]
        D7 = Dados.D7[num]
        
        P0 = Dados.D12[num]
        P1 = Dados.D13[num]
        P2 = Dados.D14[num]
        P3 = Dados.D15[num]

        P4 = Dados.D16[num]
        P5 = Dados.D17[num]
        P6 = Dados.D18[num]
        P7 = Dados.D19[num]

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
            Dados_CopX.append(CopX)
        
        if (P0+P1+P2+P3+P4+P5+P6+P7) > 0:
            CopY = (P0*DyP0 + P1*DyP1 + P4*DyP4 + P5*DyP5 - P2*DyP2 - P3*DyP3 - P6*DyP6 - P7*DyP7)/(P0+P1+P2+P3+P4+P5+P6+P7)
            Dados_CopY.append(CopY)

        allData4.append(D4)
        allData5.append(D5)
        allData6.append(D6)
        allData7.append(D7)

        num = num + 1

    ax2.clear() #Limpa o grafico

    lineX = [0, 0, -20, -20, 20, 20, 0]
    lineY = [20, -20, -20, 20, 20, -20, -20]
    ax2.plot(lineX, lineY, color='#A7BBCB')
    ax2.plot(Dados_CopX, Dados_CopY, color='#304462')

    canvasMatplot2.draw() #Desenha o grafico
    
    global dados_paciente_lista
    dados_paciente_lista = [nome_paciente, idade_paciente, altura_paciente, peso_paciente, sexo_paciente, tem_dor, nivel_dor, tem_queda, qtd_quedas, tem_labirintite, tratamento_labirintite]

    global dados_velocidade_lista
    dados_velocidade_lista = [vdcp, Dx, Dy]

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
    width=((physical_width * 9.9) / 100)-2,
    height=((physical_height * 9.26) / 100)-2,
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
    width=((physical_width * 9.9) / 100)-2,
    height=((physical_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: armazenar_dados()
)
btn_avancarDados.place(relx=0.7969, rely=0.8611)

#MARK: TELA ANAMNESE --------------------------------------------------------------------------------------------------------

canvas_anamnese = Canvas(tela_anamnese, width=physical_width, height=physical_height)
canvas_anamnese.grid(row=0, column=0)
canvas_anamnese.create_image(0, 0, image=bg_anamnese, anchor="nw")

btn_avancarAnamnese = Button(
    tela_anamnese,
    text="AVANÇAR",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((physical_width * 9.9) / 100)-2,
    height=((physical_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: dados_paciente(tela_parametros)
)
btn_avancarAnamnese.place(relx=0.7969, rely=0.8611)

#MARK: TELA PARÂMETROS ----------------------------------------------------------------------------------------------------------

canvas_parametros = Canvas(tela_parametros, width=physical_width, height=physical_height)
canvas_parametros.grid(row=0, column=0)
canvas_parametros.create_image(0, 0, image=bg_parametros, anchor="nw")

btn_fechar_parametros = Button(
    tela_parametros,
    image=bg_btnfechar,
    width=((physical_width * 5.73) / 100)-2,
    height=((physical_height * 8.33) / 100)-2,
    compound="center",
    bd=0,
    command=lambda: close_app()
)
btn_fechar_parametros.place(relx=0.975, rely=-0.05)


width_molduras = int((physical_width * 10.35)/100)
height_moldura01 = int((physical_height * 24.5)/100)
moldura1 = Image.open("UI/Parametros/moldura_01.png")
moldura1 = moldura1.resize((width_molduras, height_moldura01 ), Image.LANCZOS)
moldura01 = ImageTk.PhotoImage(moldura1)

height_moldura02 = int((physical_height * 11.5)/100)
moldura2 = Image.open("UI/Parametros/moldura_02.png")
moldura2 = moldura2.resize((width_molduras, height_moldura02), Image.LANCZOS)
moldura02 = ImageTk.PhotoImage(moldura2)

#Botão confirmar
width_bg_conf = int((physical_width * 7.92) / 100)
height_bg_conf = int((physical_height * 5.5) / 100)
bg_btn_conf1 = Image.open("UI/Parametros/btn_confirmar.png")
bg_btn_conf1 = bg_btn1.resize((width_bg_conf, height_bg_conf), Image.Resampling.LANCZOS)
bg_btn_conf = ImageTk.PhotoImage(bg_btn_conf1)

#Botão Adicionar - Remover
width_bg_adc = int((physical_width * 2.6) / 100)
height_bg_adc = int((physical_width * 2.6) / 100)
bg_btn_adc1 = Image.open("UI/Parametros/btn_adc-rmv.png")
bg_btn_adc1 = bg_btn_adc1.resize((width_bg_adc, height_bg_adc), Image.Resampling.LANCZOS)
bg_btn_adc = ImageTk.PhotoImage(bg_btn_adc1)



#MARK: CANVAS MOVIMENTAÇÃO -------------------------
canvas_movimentacao = Canvas(
    tela_parametros,
    width = (physical_width * 58.08)/100,
    height = (physical_height * 41.20)/100,
    bg="#E0E7EC",
    highlightthickness=0,
    highlightcolor=None,
    highlightbackground=None
)
canvas_movimentacao.place(relx=0.3453,rely=0.3491,anchor="nw")

canvas_oscilacao = Canvas(
    tela_parametros,
    width = (physical_width * 58.08)/100,
    height = (physical_height * 41.20)/100,
    bg="#E0E7EC",
    highlightthickness=0,
    highlightcolor=None,
    highlightbackground=None
)
canvas_oscilacao.place(relx=0.3453,rely=0.3491,anchor="nw")

rotina = ctk.CTkScrollableFrame(
    tela_parametros,
    width=(screen_width * 20.5/100),
    height=(screen_height * 33/100),
    corner_radius = 15,
    fg_color="#E0E7EC",
    bg_color="#E0E7EC",
    orientation = "vertical"
    )
rotina.place(relx=0.0583, rely=0.3481, anchor = "nw")

matriz_parametros = []
combobox_criada = []
global index_radio
global index_combo
index_radio = 0
index_combo = 0

var = ctk.IntVar()

def adicionar_linha():
    global matriz_parametros

    # Adiciona uma nova linha de valores zerados na matriz
    nova_linha = [0] * 7
    matriz_parametros.append(nova_linha)

    # Chama a função para adicionar um pacote de widgets
    gerar_widgets(rotina, 1, var, len(matriz_parametros) - 1)
    
    print(f"Matriz atualizada: {matriz_parametros}")
    

def remover_linha():
    global matriz_parametros, combobox_criada, frames_widgets

    # Verifica se há elementos para remover
    if len(matriz_parametros) > 0:
        # Remove a última linha da matriz
        matriz_parametros.pop()

        # Verifica e remove o último frame de widgets
        if frames_widgets:
            frame_para_remover = frames_widgets.pop()
            frame_para_remover.destroy()  # Remove visualmente o frame

        # Verifica e remove o último combobox
        if combobox_criada:
            combobox_criada.pop()
            
        print(f"Matriz atualizada: {matriz_parametros}")
        
def atualizar_indices():
    # Atualiza os valores de rádio e índices na combobox para se manterem coerentes
    for i, frame in enumerate(frames_widgets):
        # Atualizar variável de rádio
        radio_buttons[i].configure(value=i)
        radio_buttons[i].configure(command=lambda v=i: radio_button(v))

        # Atualizar comando da combobox
        combobox_criada[i].configure(command=lambda line, v=i: combo_box(line, v))


def gerar_widgets(scrollable_frame, num_widgets, var, indice):
    global combobox_criada, frames_widgets
    idx_inicial = len(combobox_criada)

    for i in range(num_widgets):
        frame01 = ctk.CTkFrame(scrollable_frame, bg_color="#E0E7EC", fg_color="#E0E7EC")
        frame01.pack(fill="x", pady=(screen_width * 0.5) / 100)

        frames_widgets.append(frame01)

        # RadioButton
        radio1 = ctk.CTkRadioButton(
            frame01,
            width=(screen_width * 1.3)/100,
            height=(screen_width * 1.3)/100,
            text="",
            variable=var,
            value=idx_inicial + i+1,
            fg_color="#0b2243",
            border_color="#A7BBCB",
            border_width_checked=(screen_width * 0.41)/100,
            command=lambda v=idx_inicial + i: radio_button(v)
        )
        radio1.pack(side="left", padx=(screen_width * 0.9) / 100, pady=(screen_width * 0.4) / 100)
        
        # ComboBox
        opcoes = ["Movimentação", "Oscilação"]
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
            state="normal",
            command=lambda line, v=idx_inicial + i: combo_box(line, v)
        )

        # Bloquear edição manual
        combobox.bind("<Key>", lambda e: "break")

        # **Definir valor inicial com base na matriz**
        if 0 <= indice < len(matriz_parametros):
            valor_inicial = "Movimentação" if matriz_parametros[indice][0] == "M" else "Oscilação"
            combobox.set(valor_inicial)
        else:
            combobox.set("Selecione uma opção")  # Caso índice inválido

        combobox.configure(state="disabled")
        combobox.pack(side="right", padx=(screen_width * 0.9) / 100, pady=(screen_width * 0.4) / 100)

        combobox_criada.append(combobox)



# Inicialização de listas auxiliares
frames_widgets = []  # Armazena referências aos frames
radio_buttons = []   # Armazena referências aos botões de rádio

# Botão Adicionar
btn_adicionar = Button(
    tela_parametros,
    text="+",
    font=("Inter", fontsize14+3,"bold"),
    fg="#E0E0E0",
    activebackground="#E0E7EC",
    background="#E0E7EC",
    image=bg_btn_adc,
    width=((physical_width * 3) / 100)-2,
    height=((physical_width * 3) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=adicionar_linha
)
btn_adicionar.place(relx=0.1693, rely=0.726, anchor="center")

btn_remover = Button(
    tela_parametros,
    text="-",
    font=("Inter", fontsize14+3, "bold"),
    fg="#E0E0E0",
    activebackground="#E0E7EC",
    background="#E0E7EC",
    image=bg_btn_adc,
    width=((physical_width * 3) / 100) - 2,
    height=((physical_width * 3) / 100) - 2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: remover_linha()
)
btn_remover.place(relx=0.2, rely=0.726, anchor="center")

#Essa função só chama se o raio botão relacionado está clicado - Criar verificação se o index selecionado do radio é o mesmo da combobox
def combo_box(line, idx):
    global index_combo
    index_combo = idx
    if line == "Movimentação":
        mostrar_movimentacao()
    elif line == "Oscilação":
        mostrar_oscilacao()

def radio_button(value):
    global index_radio
    index_radio = value

    canvas_movimentacao.place_forget()
    canvas_oscilacao.place_forget()

    # Desativar todas as comboboxes
    for combobox in combobox_criada:
        combobox.configure(state="disabled")

    # Verifique se o índice é válido antes de acessar a lista
    if 0 <= index_radio < len(combobox_criada):
        combobox_criada[index_radio].configure(state="normal")

        # Restaurar valores se já existem na matriz
        if combobox_criada[index_radio].get() == "Movimentação":
            mostrar_movimentacao()
        elif combobox_criada[index_radio].get() == "Oscilação":
            mostrar_oscilacao()
    
#CONFIGURAÇÃO DO GIF

def play_gif(label, gif_path, size=(300, 300)):  # Define o tamanho desejado
    img = Image.open(gif_path)
    frames = []

    try:
        while True:
            resized_frame = img.copy().resize(size)  # Redimensiona o frame
            frames.append(ImageTk.PhotoImage(resized_frame))
            img.seek(len(frames))  # Avança para o próximo frame
    except EOFError:
        pass  # Final da sequência de frames

    def update(ind):
        frame = frames[ind]
        label.configure(image=frame)
        label.image = frame
        ind = (ind + 1) % len(frames)  # Loop infinito
        label.after(30, update, ind)  # Atualiza o frame a cada 100ms

    update(0)  # Inicia a animação

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
        new_value=matriz_parametros[index_radio][3] if matriz_parametros[index_radio][3] != 0 else 5
    )
    mov_label_vel.place(relx=0.6682, rely = 0.38, anchor = "center")
    mov_vel.place(relx=0.6682, rely = 0.48, anchor = "center")

    mov_label_x = Label(canvas_movimentacao, text="Ângulo X", font=("Inter", fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    mov_x = boxes.CustomSpinbox(
        canvas_movimentacao,
        min_value=-25,
        max_value=25,
        step=1,
        new_value=matriz_parametros[index_radio][4] if matriz_parametros[index_radio][4] > -25 else -25
    )
    mov_label_x.place(relx=0.87, rely= 0.2180, anchor = "center")
    mov_x.place(relx=0.87, rely = 0.3146, anchor = "center")

    mov_label_y = Label(canvas_movimentacao, text="Ângulo Y", font=("Inter", fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    mov_y = boxes.CustomSpinbox(
        canvas_movimentacao,
        min_value=-25,
        max_value=25,
        step=1,
        new_value=matriz_parametros[index_radio][5] if matriz_parametros[index_radio][5] > -25 else -25
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
    width=((physical_width * 7.92) / 100)-2,
    height=((physical_height * 5.5) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    background="#E0E7EC", 
    command= confirmar_mov
    #comando do botão precisa ter o get e o .append(matriz_parametros[index_selecionado][posição])
    )
    btn_confirmar_mov.place(relx=0.6655, rely=0.8854, anchor='center')

    label_gif_mov = Label(canvas_movimentacao, borderwidth=5, bg="#A7BBCB")
    label_gif_mov.place(relx=0.1991, rely=0.52, anchor="center")

    play_gif(label_gif_mov, "UI/GIF/gif_mov.gif", size = (300, 300))


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
        new_value=matriz_parametros[index_radio][1] if matriz_parametros[index_radio][1] > -25 else -25)
    osc_label_maxx.place(relx=0.4664, rely= 0.2180, anchor = "center")
    osc_maxx.place(relx=0.4664, rely = 0.3146, anchor = "center")

    osc_label_minx = Label(canvas_oscilacao, text="Ângulo Min X", font=("Inter", fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    osc_minx = boxes.CustomSpinbox(canvas_oscilacao,
        min_value=-25,
        max_value=25,
        step=1,
        new_value=matriz_parametros[index_radio][2] if matriz_parametros[index_radio][2] > -25 else -25)
    osc_label_minx.place(relx=0.4664, rely= 0.5551, anchor = "center")
    osc_minx.place(relx=0.4664, rely = 0.6472, anchor = "center")

    osc_label_vel = Label(canvas_oscilacao, text="Velocidade", font=("Inter",fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    osc_vel = boxes.CustomSpinbox(canvas_oscilacao,
        min_value=1,
        max_value=15,
        step=1,
        new_value=matriz_parametros[index_radio][3] if matriz_parametros[index_radio][3] != 0 else 5)
    osc_label_vel.place(relx=0.6682, rely= 0.2180, anchor = "center")
    osc_vel.place(relx=0.6682, rely = 0.3146, anchor = "center")

    osc_label_rep = Label(canvas_oscilacao, text="Repetições", font=("Inter",fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    osc_rep = boxes.CustomSpinbox(canvas_oscilacao,
        min_value=1,
        max_value=100,
        step=1,
        new_value=matriz_parametros[index_radio][4] if matriz_parametros[index_radio][4] != 0 else 1)
    osc_label_rep.place(relx=0.6682, rely= 0.5551, anchor = "center")
    osc_rep.place(relx=0.6682, rely = 0.6472, anchor = "center")

    osc_label_maxy = Label(canvas_oscilacao, text="Ângulo Max Y", font=("Inter", fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    osc_maxy = boxes.CustomSpinbox(canvas_oscilacao,
        min_value=-25,
        max_value=25,
        step=1,
        new_value=matriz_parametros[index_radio][5] if matriz_parametros[index_radio][5] > -25 else -25)
    osc_label_maxy.place(relx=0.87, rely= 0.2180, anchor = "center")
    osc_maxy.place(relx=0.87, rely = 0.3146, anchor = "center")

    osc_label_miny = Label(canvas_oscilacao, text="Ângulo Min Y", font=("Inter", fontsize14, "bold"), background="#E0E7EC", fg="#656565")
    osc_miny = boxes.CustomSpinbox(canvas_oscilacao,
        min_value=-25,
        max_value=25,
        step=1,
        new_value=matriz_parametros[index_radio][6] if matriz_parametros[index_radio][6] > -25 else -25)
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
    width=((physical_width * 7.92) / 100)-2,
    height=((physical_height * 5.5) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    background="#E0E7EC",
    command= confirmar_osc
    #comando do botão precisa ter o get e o .append(matriz_parametros[index_selecionado][posição])
    )
    btn_confirmar_osc.place(relx=0.6655, rely=0.8854, anchor='center')

    label_gif_osc = Label(canvas_oscilacao, borderwidth=5, bg="#A7BBCB")
    label_gif_osc.place(relx=0.1991, rely=0.52, anchor="center")

    play_gif(label_gif_osc, "UI/GIF/gif_osc.gif", size = (300, 300))


def limpar_widgets():
    global combobox_criada, frames_widgets

    # Destruir todos os frames dentro da lista
    for frame in frames_widgets:
        frame.destroy()
    
    # Esvaziar as listas
    frames_widgets.clear()
    combobox_criada.clear()

def carregar_presets():
    global matriz_parametros

    # Defina aqui a matriz predefinida
    matriz_parametros = [['O', 0, 0, 10, 3, 10, -10],
                         ['O', 10, -10, 10, 3, 0, 0], 
                         ]

    # Remove os widgets antigos antes de criar novos
    limpar_widgets()

    # Criar os novos widgets com base na matriz
    for i in range(len(matriz_parametros)):
        gerar_widgets(rotina, 1, var, i)
    
    messagebox.showinfo(title=None, message="Carregamento de predefinição concluído")

btn_presets = Button(
    tela_parametros,
    text="PRESETS",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((physical_width * 9.9) / 100)-2,
    height=((physical_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command= carregar_presets
)
btn_presets.place(relx=0.1042, rely=0.8611)

#MARK: CANVAS CARREGAMENTO ---------------------------------------------------------------------------------------------------------------------------
canvas_carregamento = Canvas(tela_carregamento, width=physical_width, height=physical_height)
canvas_carregamento.grid(row=0, column=0)
canvas_carregamento.create_image(0, 0, image=bg_carregamento, anchor="nw")

btn_fechar_carregamento = Button(
    tela_carregamento,
    image=bg_btnfechar,
    width=((physical_width * 5.73) / 100)-2,
    height=((physical_height * 8.33) / 100)-2,
    compound="center",
    bd=0,
    command=lambda: close_app()
)
btn_fechar_carregamento.place(relx=0.975, rely=-0.05)

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
    global loopColeta
    global start

    global NMov, Passo, TempoStart, Movendo, AngXAtual, AngYAtual, RepAtual

    NMov = 0
    Passo = 1
    TempoStart = time.time()
    Movendo = 0

    AngXAtual = 0
    AngYAtual = 0

    RepAtual = 1

    loopColeta = 1
    baud = 500000
    
    #COM8 - SALVAMENTO DE DADOS
    #COM9 - ESCREVE
    #COM18 - LÊ

    porta1 = "COM9" #Enviar dados para essa porta
    #porta2 = "COM18"

    ard1 = serial.Serial(porta1, baud, timeout=0.01, writeTimeout=3) #Enviar dados para essa porta
    #ard2 = serial.Serial(porta2, baud, timeout=0.01, writeTimeout=3)

    os.startfile("Supervisorio.exe")  #Executa o programa de coleta de dados
    time.sleep(1) #Espera 1 segundo para o programa abrir e se conectar
    ard1.write(str.encode('#andre9,0,0,5\n')) # Nome do arquivo em que será salvo os dados (precisa ter o # antes)
    time.sleep(1) # Espera 1 segundo para o arquivo ser criado
    ard1.write(str.encode('I,0,0,5\n')) #Inicia a coleta

    Dados_CopX = [0]
    Dados_CopY = [0]
    Dados_Tempo = [0]


    show_frame(tela_carregamento)

    start = time.time()

    root.after(10, ColetarDados)




def ControlarMovimento():

    global matriz_parametros, NMov, TempoStart, Movendo, Passo, AngYAtual, AngXAtual, RepAtual, AngX, AngY

    Linhas = len(matriz_parametros)

    if NMov < Linhas:

        Tipo = matriz_parametros[NMov][0]

        if (Tipo == "O"):

            AngXmax = matriz_parametros[NMov][1]
            AngXmin = matriz_parametros[NMov][2]
            VelOci = matriz_parametros[NMov][3]
            Rep = matriz_parametros[NMov][4]
            AngYmax = matriz_parametros[NMov][5]
            AngYmin = matriz_parametros[NMov][6]

            if Passo == 1:

                if(time.time() - TempoStart) >= 1:

                    Passo = 2

                    TempoStart = time.time()

            if Passo == 2:

                if Movendo == 0:

                    AngX = abs( AngXAtual - AngXmin)
                    AngY = abs( AngYAtual - AngYmin)

                    ard1.write(str.encode(f"I,{AngXmin},{AngYmin},{VelOci}\n")) #Movimento
                    Movendo = 1

                    TempoStart = time.time()

                if Movendo == 1 and (time.time() - TempoStart) >= abs(AngX/VelOci) and (time.time() - TempoStart) >= abs(AngY/VelOci):

                    Passo = 3
                    Movendo = 0
                    TempoStart = time.time()

                    AngXAtual = AngXmin
                    AngYAtual = AngYmin

            if Passo == 3:

                if Movendo == 0:

                    AngX = abs( AngXAtual - AngXmax)
                    AngY = abs( AngYAtual - AngYmax)

                    ard1.write(str.encode(f"I,{AngXmax},{AngYmax},{VelOci}\n")) #Movimento
                    Movendo = 1

                    TempoStart = time.time()

                if Movendo == 1 and (time.time() - TempoStart) >= abs(AngX/VelOci) and (time.time() - TempoStart) >= abs(AngY/VelOci):

                    Passo = 4
                    Movendo = 0
                    TempoStart = time.time()

                    AngXAtual = AngXmax
                    AngYAtual = AngYmax

            if Passo == 4:

                RepAtual = RepAtual +1

                if RepAtual > Rep:

                    Passo = 5

                else:

                    Passo = 2
                    TempoStart = time.time()

            if Passo == 5:

                if Movendo == 0:

                    AngX = abs( AngXAtual - 0)
                    AngY = abs( AngYAtual - 0)

                    ard1.write(str.encode(f"I,0,0,{VelOci}\n")) #Movimento
                    Movendo = 1

                    TempoStart = time.time()

                if Movendo == 1 and (time.time() - TempoStart) >= abs(AngX/VelOci) and (time.time() - TempoStart) >= abs(AngY/VelOci):

                    Passo = 1
                    Movendo = 0
                    TempoStart = time.time()

                    RepAtual = 1

                    AngXAtual = 0
                    AngYAtual = 0

                    NMov = NMov + 1

        if (Tipo == "M"):

            TempoIni = matriz_parametros[NMov][1]
            TempoFin = matriz_parametros[NMov][2]
            VelMov = matriz_parametros[NMov][3]
            AngX = abs( AngXAtual - matriz_parametros[NMov][4])
            AngY = abs( AngYAtual - matriz_parametros[NMov][5])
            CorX = matriz_parametros[NMov][4]
            CorY = matriz_parametros[NMov][5]

            if Passo == 1:

                if(time.time() - TempoStart) >= TempoIni:

                    Passo = 2

                    TempoStart = time.time()

            if Passo == 2:

                if Movendo == 0:

                    ard1.write(str.encode(f"I,{CorX},{CorY},{VelMov}\n")) #Movimento
                    Movendo = 1

                if Movendo == 1 and (time.time() - TempoStart) >= abs(AngX/VelMov) and (time.time() - TempoStart) >= abs(AngY/VelMov):

                    Passo = 3
                    Movendo = 0
                    TempoStart = time.time()

                    AngXAtual = CorX
                    AngYAtual = CorY

            if Passo == 3:

                if(time.time() - TempoStart) >= TempoFin:

                    Passo = 1

                    TempoStart = time.time()

                    NMov = NMov + 1

    else:
        PararColeta()

#MARK: COLETAR DADOS DA PLATAFORMA

def ColetarDados():
    
    global start, fim
    global baud
    global porta1
    global ard1
    global Dados_CopX
    global Dados_CopY
    global Dados_Tempo
    global Dados_Tempo

    ControlarMovimento()


    list_of_files = glob.glob('*.txt') #* means all if need specific format then #.csv
    latest_file = max(list_of_files, key= os.path.getctime)

    try:

        with open(latest_file,"r", encoding="utf-8",errors="ignore") as scraped:

            final_line = scraped.readlines()[-2]

            valueSplit = str(final_line).split("\t")

            P0 = float(valueSplit[-8])
            P1 = float(valueSplit[-7])
            P2 = float(valueSplit[-6])
            P3 = float(valueSplit[-5])

            P4 = float(valueSplit[-4])
            P5 = float(valueSplit[-3])
            P6 = float(valueSplit[-2])
            P7 = float(valueSplit[-1])

            if(P0 < 0):
                P0 = 0

            if(P1 < 0):
                P1 = 0

            if(P2 < 0):
                P2 = 0

            if(P3 < 0):
                P3 = 0

            if(P4 < 0):
                P4 = 0

            if(P5 < 0):
                P5 = 0

            if(P6 < 0):
                P6 = 0

            if(P7 < 0):
                P7 = 0

            X = float(valueSplit[-16])
            Y = float(valueSplit[-15])

            VEL = float(valueSplit[-14])
            EEG = float(valueSplit[-13])
            EMG1 = float(valueSplit[-12])
            EMG2 = float(valueSplit[-11])
            EMG3 = float(valueSplit[-10])
            EMG4 = float(valueSplit[-9])

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

            ax3.clear() #Limpa o grafico

            lineX = [0, 0, -20, -20, 20, 20, 0]
            lineY = [20, -20, -20, 20, 20, -20, -20]
            ax3.plot(lineX, lineY, color='#A7BBCB')
            ax3.plot(Dados_CopX, Dados_CopY, color='#304462')

            canvasMatplot3.draw() #Desenha o grafico

    except:
        print("Erro Dado")
        
    if(loopColeta) == 1:
        root.after(10, ColetarDados)
    else: 
        ard1.write(str.encode('F,0,0,5\n')) #Interrompe a coleta
        time.sleep(1) #Espera 1 segundo para coletar todos os dados

        ard1.close() #Fecha a conexão com a plataforma
        subprocess.call("taskkill /f /im WindowsTerminal.exe", shell=True) #Fecha programa de coleta
    
    fim = time.time()
    Dados_Tempo = fim - start


#MARK: TELA CARREGAMENTO ---------------------------------------------------------------------------------------------------------------------------

btn_iniciarCarregamento = Button(
    tela_parametros,
    text="COLETAR",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((physical_width * 9.9) / 100)-2,
    height=((physical_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: show_frame(tela_carregamento) #Com o teensy mudar para ManterColeta()
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
    width=((physical_width * 9.9) / 100)-2,
    height=((physical_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: PararColeta()
)
btn_parar.place(relx=0.1042, rely=0.8611)



#MARK: TELA RESULTADO -----------------------------------------------------------------------------------------------------------------------------------------

canvas_resultado = Canvas(tela_resultado, width=physical_width, height=physical_height)
canvas_resultado.grid(row=0, column=0)
canvas_resultado.create_image(0, 0, image=bg_resultado, anchor="nw")

btn_fechar_resultado = Button(
    tela_resultado,
    image=bg_btnfechar,
    width=((physical_width * 5.73) / 100)-2,
    height=((physical_height * 8.33) / 100)-2,
    compound="center",
    bd=0,
    command=lambda: close_app()
)
btn_fechar_resultado.place(relx=0.975, rely=-0.05)

# Canvas Detalhes
canvas_paciente = Canvas(
    tela_resultado,
    width=(physical_width * 46)/100,
    height=(physical_height * 60)/100,
    bg="#ffffff",
    highlightthickness=6,
    highlightcolor="#A7BBCB",
    highlightbackground="#A7BBCB"
    )
canvas_centro_pressao = Canvas(
    tela_resultado, 
    width=(physical_width * 46)/100, 
    height=(physical_height * 60)/100, 
    bg="#ffffff",
    highlightthickness=6,
    highlightcolor="#A7BBCB",
    highlightbackground="#A7BBCB"
    )
canvas_distr_massas = Canvas(
    tela_resultado,
    width=(physical_width * 46)/100,
    height=(physical_height * 60)/100,
    bg="#ffffff",
    highlightthickness=6,
    highlightcolor="#A7BBCB",
    highlightbackground="#A7BBCB"
    )
canvas_emg = Canvas(
    tela_resultado,
    width=(physical_width * 46)/100,
    height=(physical_height * 60)/100,
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
    width=(physical_width * 46)/100, 
    height=(physical_height * 60)/100, 
    bg="#ffffff",
    highlightthickness=6,
    highlightcolor="#A7BBCB",
    highlightbackground="#A7BBCB")
canvas_grafico_leitura.place(relx=0.38, rely=0.5, anchor="center")  # Centralizado na tela

canvasMatplot2 = FigureCanvasTkAgg(fig2, master = canvas_grafico_leitura)
canvasMatplot2.get_tk_widget().pack()

fig4 = matplotlib.figure.Figure()
ax4 = fig4.add_subplot()

canvas_grafico_emg = Canvas(canvas_emg, 
    width=(physical_width * 46)/100, 
    height=(physical_height * 60)/100, 
    bg="#ffffff",
    highlightthickness=6,
    highlightcolor="#A7BBCB",
    highlightbackground="#A7BBCB")
canvas_grafico_emg.place(relx=0.6, rely=0.55, anchor="center")  # Centralizado na tela

canvasMatplot4 = FigureCanvasTkAgg(fig4, master = canvas_grafico_emg)
canvasMatplot4.get_tk_widget().pack()

fig6 = matplotlib.figure.Figure()
ax6 = fig6.add_subplot()

canvas_grafico_massa = Canvas(canvas_distr_massas, 
    width=(physical_width * 46)/100, 
    height=(physical_height * 60)/100, 
    bg="#ffffff",
    highlightthickness=6,
    highlightcolor="#A7BBCB",
    highlightbackground="#A7BBCB")
canvas_grafico_massa.place(relx=0.38, rely=0.5, anchor="center")  # Centralizado na tela

canvasMatplot6 = FigureCanvasTkAgg(fig6, master = canvas_grafico_massa)
canvasMatplot6.get_tk_widget().pack()


#MARK: Ler Arquivo() --------------------------------------------------------------------------------------------------------------------------------------

def LerArquivo():

    global D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11
    global P0, P1, P2, P3, P4, P5, P6, P7
    global allData0, allData1, allData2, allData3, allData4, allData5, allData6, allData7, allData8, allData9, allData10, allData11, allData12, allData13, allData14, allData15, allData16, allData17, allData18, allData19
    global dxMax, dxMin, dyMax, dyMin

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
    ax4.clear()

    list_of_files = glob.glob('*.txt') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)

    with open(latest_file) as file:
        Dados = csv.reader(file)

        for row in Dados:

            valueSplit = str(row).split(",")

            if len(valueSplit) == 20:

                D0 = re.sub("[^A-Z]", "", valueSplit[0])
                D1 = float(re.sub("[^0-9]", "", valueSplit[1]))
                D2 = float(re.sub("[^0-9]", "", valueSplit[2]))
                D3 = float(re.sub("[^0-9]", "", valueSplit[3]))
                
                #Dados EMG
                D4 = float(re.sub("[^0-9]", "", valueSplit[4]))
                D5 = float(re.sub("[^0-9]", "", valueSplit[5]))
                D6 = float(re.sub("[^0-9]", "", valueSplit[6]))
                D7 = float(re.sub("[^0-9]", "", valueSplit[7]))
                D8 = float(re.sub("[^0-9]", "", valueSplit[8]))
                D9 = float(re.sub("[^0-9]", "", valueSplit[9]))
                D10 = float(re.sub("[^0-9]", "", valueSplit[10]))
                D11 = float(re.sub("[^0-9]", "", valueSplit[11]))
                
                #Dados COP
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
                    Dados_CopX.append(CopX)
                
                if (P0+P1+P2+P3+P4+P5+P6+P7) > 0:
                    CopY = (P0*DyP0 + P1*DyP1 + P4*DyP4 + P5*DyP5 - P2*DyP2 - P3*DyP3 - P6*DyP6 - P7*DyP7)/(P0+P1+P2+P3+P4+P5+P6+P7)
                    Dados_CopY.append(CopY)
                    

    dxMax = max(Dados_CopX)
    dxMin = min(Dados_CopX)
    dyMax = max(Dados_CopY)
    dyMin = min(Dados_CopY)

    Dx = dxMax - dxMin
    Dy = dyMax - dyMin
    
    lineX = [0, 0, -20, -20, 20, 20, 0]
    lineY = [20, -20, -20, 20, 20, -20, -20]
    ax2.plot(lineX, lineY, color='#A7BBCB')
    ax2.plot(Dados_CopX, Dados_CopY, color='#304462')

    canvasMatplot2.draw() #Desenha o grafico

    global dados_velocidade_lista

    #MARK: Definindo como 0 para teste sem o teensy
    Dados_Tempo = 5

    n = 0
    Dt = 0

    while n < (len(Dados_CopX))-2:

        x1 = Dados_CopX[(n+1)]
        x2 = Dados_CopX[((n+1) + 1)]

        y1 = Dados_CopY[(n+1)]
        y2 = Dados_CopY[((n+1) + 1)]

        d = math.sqrt((x1-x2) **2 + (y1-y2) **2)

        Dt = Dt + d

        n = n + 1

    vdcp = Dt / Dados_Tempo

    dados_velocidade_lista = [vdcp, Dx, Dy]

    salvar_dados()

#MARK: Ler Arquivo() --------------------------------------------------------------------------------------------------------------------------------------

def AvancarResultados():

    global D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11
    global P0, P1, P2, P3, P4, P5, P6, P7
    global allData0, allData1, allData2, allData3, allData4, allData5, allData6, allData7, allData8, allData9, allData10, allData11, allData12, allData13, allData14, allData15, allData16, allData17, allData18, allData19
    global dxMax, dxMin, dyMax, dyMin

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

    list_of_files = glob.glob('*.txt') #* means all if need specific format then #.csv
    latest_file = max(list_of_files, key= os.path.getctime)

    with open(latest_file) as fd:
        rd = csv.reader(fd,delimiter="\t")

        for row in rd:
###################################################################################################

            try:
                valueSplit = str(row).split(",")

                D0 = re.sub("[^A-Z]", "", valueSplit[-17])
                D1 = float(re.sub("[^0-9]", "", valueSplit[-16]))
                D2 = float(re.sub("[^0-9]", "", valueSplit[-15]))
                D3 = float(re.sub("[^0-9]", "", valueSplit[-14]))
                
                #Dados EMG
                D4 = float(re.sub("[^0-9]", "", valueSplit[-12]))
                D5 = float(re.sub("[^0-9]", "", valueSplit[-11]))
                D6 = float(re.sub("[^0-9]", "", valueSplit[-10]))
                D7 = float(re.sub("[^0-9]", "", valueSplit[-9]))
                
                #Dados COP
                P0 = float(re.sub("[^0-9]", "", valueSplit[-8]))
                P1 = float(re.sub("[^0-9]", "", valueSplit[-7]))
                P2 = float(re.sub("[^0-9]", "", valueSplit[-6]))
                P3 = float(re.sub("[^0-9]", "", valueSplit[-5]))

                P4 = float(re.sub("[^0-9]", "", valueSplit[-4]))
                P5 = float(re.sub("[^0-9]", "", valueSplit[-3]))
                P6 = float(re.sub("[^0-9]", "", valueSplit[-2]))
                P7 = float(re.sub("[^0-9]", "", valueSplit[-1]))

                allData0.append(D0)
                allData1.append(D1)
                allData2.append(D2)
                allData3.append(D3)
                allData4.append(D4)
                allData5.append(D5)
                allData6.append(D6)
                allData7.append(D7)
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
                    Dados_CopX.append(CopX)
                
                if (P0+P1+P2+P3+P4+P5+P6+P7) > 0:
                    CopY = (P0*DyP0 + P1*DyP1 + P4*DyP4 + P5*DyP5 - P2*DyP2 - P3*DyP3 - P6*DyP6 - P7*DyP7)/(P0+P1+P2+P3+P4+P5+P6+P7)
                    Dados_CopY.append(CopY)

            except:
                print("ErroDados")

    dxMax = max(Dados_CopX)
    dxMin = min(Dados_CopX)
    dyMax = max(Dados_CopY)
    dyMin = min(Dados_CopY)

    Dx = dxMax - dxMin
    Dy = dyMax - dyMin

    lineX = [0, 0, -20, -20, 20, 20, 0]
    lineY = [20, -20, -20, 20, 20, -20, -20]
    ax2.plot(lineX, lineY, color='#A7BBCB')
    ax2.plot(Dados_CopX, Dados_CopY, color='#304462')

    canvasMatplot2.draw() #Desenha o grafico

    global dados_velocidade_lista

    #MARK: Definindo como 0 para teste sem o teensy
    Dados_Tempo = 5

    n = 0
    Dt = 0

    while n < (len(Dados_CopX))-2:

        x1 = Dados_CopX[(n+1)]
        x2 = Dados_CopX[((n+1) + 1)]

        y1 = Dados_CopY[(n+1)]
        y2 = Dados_CopY[((n+1) + 1)]

        d = math.sqrt((x1-x2) **2 + (y1-y2) **2)

        Dt = Dt + d

        n = n + 1

    vdcp = Dt / Dados_Tempo

    dados_velocidade_lista = [vdcp, Dx, Dy]

    salvar_dados()


  ##############################################################################################          

btn_avancarResultado = Button(
    tela_carregamento,
    text="RESULTADOS",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((physical_width * 9.9) / 100)-2,
    height=((physical_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    #MARK: Botão para carregar o arquivo do excel
    command=lambda: AvancarResultados()
)
btn_avancarResultado.place(relx=0.7969, rely=0.8611)

# Posicionamento relativo
canvas_paciente.place(relx=0.4688, rely=0.213, anchor='nw')
canvas_centro_pressao.place(relx=0.4688, rely=0.213, anchor='nw')
canvas_distr_massas.place(relx=0.4688, rely=0.213, anchor='nw')
canvas_emg.place(relx=0.4688, rely=0.213, anchor='nw')

# Conteudo Painel PACIENTE

#Botão Pressionado
width_btn_click = int((physical_width * 12.24) / 100)
height_btn_click = int((physical_height * 17.6) / 100)
bg_btn_click1 = Image.open("UI/Resultado/btn_clicked.png")
bg_btn_click1 = bg_btn_click1.resize((width_btn_click, height_btn_click), Image.Resampling.LANCZOS)
bg_btn_click = ImageTk.PhotoImage(bg_btn_click1)

#Fundo Dados do paciente
width_bg_dadospaciente = int((physical_width * 40) / 100)
height_bg_dadospaciente = int((physical_height * 7.59) / 100)
bg_dadospaciente1 = Image.open("UI/Resultado/bg_dados_paciente.png")
bg_dadospaciente1 = bg_dadospaciente1.resize((width_bg_dadospaciente, height_bg_dadospaciente), Image.Resampling.LANCZOS)
bg_dadospaciente = ImageTk.PhotoImage(bg_dadospaciente1)

#Fundo dor/queda
width_bg_dorqueda = int((physical_width * 18.23) / 100)
height_bg_dorqueda = int((physical_height * 9.26) / 100)
bg_dorqueda1 = Image.open("UI/Resultado/bg_dor_queda.png")
bg_dorqueda1 = bg_dorqueda1.resize((width_bg_dorqueda, height_bg_dorqueda), Image.Resampling.LANCZOS)
bg_dorqueda = ImageTk.PhotoImage(bg_dorqueda1)

#Fundo labirintite
width_bg_labirintite = int((physical_width * 18.23) / 100)
height_bg_labirintite = int((physical_height * 32.13) / 100)
bg_labirintite1 = Image.open("UI/Resultado/bg_labirintite.png")
bg_labirintite1 = bg_labirintite1.resize((width_bg_labirintite, height_bg_labirintite), Image.Resampling.LANCZOS)
bg_labirintite = ImageTk.PhotoImage(bg_labirintite1)

#Fundo Dados do paciente
width_bg_minibarra = int((physical_width * 0.104167) / 100)
height_bg_minibarra = int((physical_height * 29.91) / 100)
bg_minibarra1 = Image.open("UI/Resultado/mini_barra.png")
bg_minibarra1 = bg_minibarra1.resize((width_bg_minibarra, height_bg_minibarra), Image.Resampling.LANCZOS)
bg_minibarra = ImageTk.PhotoImage(bg_minibarra1)


#MARK: Exibir dados()
def exibir_dados_paciente():
    canvas_paciente.delete("all")  # Limpa o conteúdo do Canvas antes de exibir novos dados
     # Obtém as dimensões do Canvas
    canvas_width = canvas_paciente.winfo_width()
    canvas_height = canvas_paciente.winfo_height()


    nome, idade, altura, peso, sexo, tem_dor, nivel_dor, tem_queda, qtd_quedas, tem_labirintite, tratamento_labirintite, membroDominante  = dados_paciente_lista



    # Posiciona cada texto usando valores relativos, sem armazenar coordenadas em variáveis
    canvas_paciente.create_text(canvas_width * 0.5, canvas_height * 0.115, 
                                text=f"{nome}", font=("Inter", fontsize22, "bold"), fill="#304462", anchor = "center")
    
    canvas_paciente.create_image(canvas_width * 0.5, canvas_height * 0.25, image = bg_dadospaciente, anchor = 'center')

    canvas_paciente.create_text(canvas_width * 0.5, canvas_height * 0.25, 
                                text=f"Idade: {idade} anos  |  Altura: {altura}cm  |  Peso: {peso}kg  |  Sexo: {sexo}", font=("Inter", fontsize-1), fill="#304462")
 
    canvas_paciente.create_image(canvas_width * 0.267, canvas_height * 0.4569, image = bg_dorqueda, anchor = 'center')

    canvas_paciente.create_image(canvas_width * 0.267, canvas_height * 0.6462, image = bg_dorqueda, anchor = 'center')

    canvas_paciente.create_image(canvas_width * 0.267, canvas_height * 0.8369, image = bg_dorqueda, anchor = 'center')

    canvas_paciente.create_image(canvas_width * 0.733, canvas_height * 0.65, image = bg_labirintite, anchor = 'center')
    
    canvas_paciente.create_image(canvas_width * 0.5, canvas_height * 0.65, image = bg_minibarra, anchor = 'center')


    canvas_paciente.create_text(canvas_width * 0.18, canvas_height * 0.455, 
                                text="Nível da dor", font=("Inter", fontsize22-2, "bold"), fill="#5D6673")
    if tem_dor == "Sim":
        canvas_paciente.create_text(canvas_width * 0.40, canvas_height * 0.455, 
                                text=f"{nivel_dor}", font=("Inter", fontsize22+4, "bold"), fill="#0B2243")
    else:
        canvas_paciente.create_text(canvas_width * 0.40, canvas_height * 0.455, 
                                text=f"0", font=("Inter", fontsize22+4, "bold"), fill="#0B2243")
    
        
    canvas_paciente.create_text(canvas_width * 0.21, canvas_height * 0.6462, 
                                text="Eventos de queda\nno último ano", font=("Inter", fontsize22-4, "bold"), fill="#5D6673", anchor = 'center')
    if tem_queda == "Sim":
        canvas_paciente.create_text(canvas_width * 0.40, canvas_height * 0.6462, 
                                text=f"{qtd_quedas}", font=("Inter", fontsize22+4, "bold"), fill="#0B2243")
    else:
        canvas_paciente.create_text(canvas_width * 0.40, canvas_height * 0.6462, 
                                text=f"0", font=("Inter", fontsize22+4, "bold"), fill="#0B2243")
        
    canvas_paciente.create_text(canvas_width * 0.167, canvas_height * 0.8369, 
                                text="Membro\nDominante", font=("Inter", fontsize22-4, "bold"), fill="#5D6673", anchor = 'center')
    if membroDominante == "Direito":
        canvas_paciente.create_text(canvas_width * 0.38, canvas_height * 0.8369, 
                                text=f"{membroDominante}", font=("Inter", fontsize22, "bold"), fill="#0B2243")
    else:
        canvas_paciente.create_text(canvas_width * 0.36, canvas_height * 0.8369, 
                                text=f"{membroDominante}", font=("Inter", fontsize22, "bold"), fill="#0B2243")



    canvas_paciente.create_text(canvas_width * 0.733, canvas_height * 0.44, 
                                text=f"Crise de labirintite no", font=("Inter", fontsize22-3, "bold"), fill="#5D6673", anchor = 'center')
    canvas_paciente.create_text(canvas_width * 0.733, canvas_height * 0.485, 
                                text=f"último mês", font=("Inter", fontsize22-3, "bold"), fill="#5D6673", anchor = 'center')
    if tem_labirintite == "Sim":
        canvas_paciente.create_text(canvas_width * 0.733, canvas_height * 0.57, 
                                text=f"SIM", font=("Inter", fontsize22, "bold"), fill="#0B2243", anchor = 'center')
    else:
        canvas_paciente.create_text(canvas_width * 0.733, canvas_height * 0.57, 
                                text=f"NÃO", font=("Inter", fontsize22, "bold"), fill="#0B2243", anchor = 'center')

    
    canvas_paciente.create_text(canvas_width * 0.733, canvas_height * 0.69, 
                                text=f"Tratamento utilizado", font=("Inter", fontsize22-3, "bold"), fill="#5D6673", anchor = 'center')
    if tem_labirintite == "Sim":
        linhas = textwrap.wrap(tratamento_labirintite, width=19)[:3]  # Máximo de 3 linhas

    # Ajusta a posição para cada linha
        for i, linha in enumerate(linhas):
            canvas_paciente.create_text(canvas_width * 0.733, canvas_height * (0.76 + i * 0.05), 
                                    text=linha, font=("Inter", fontsize22-2, "bold"), 
                                    fill="#0B2243", anchor='center')
    else:
        canvas_paciente.create_text(canvas_width * 0.733, canvas_height * 0.8, 
                                text=f"SEM TRATAMENTO", font=("Inter", fontsize22-2, "bold"), fill="#0B2243", anchor = 'center')

    

# Função para exibir o canvas correto
def exibir_canvas(canvas):
    canvas_paciente.place_forget()
    canvas_distr_massas.place_forget()
    canvas_emg.place_forget()
    canvas_centro_pressao.place_forget()
    
    #Exibe o canvas selecionado
    canvas.place(relx=0.4688, rely=0.213, anchor='nw')

    if canvas == canvas_paciente:
        exibir_dados_paciente()

        btn_paciente.config(fg="#e0e0e0", image=bg_btn_click)
        btn_centro_pressao.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_distr_massas.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_emg.configure(fg="#0B2243", image=bg_btn_resultado)

#MARK: Função do botão Centro de pressão 
    if canvas == canvas_centro_pressao:

        canvas_width = canvas_centro_pressao.winfo_width()
        canvas_height = canvas_centro_pressao.winfo_height()
        
        canvas_centro_pressao.create_text(canvas_width * 0.5, canvas_height * 0.1,
        text=f"Gráfico do Centro de pressão (CdP)", font=("Inter", fontsize22, "bold"), fill="#304462", anchor = "center")

        vdcp, Dx, Dy = dados_velocidade_lista

        canvas_centro_pressao.create_text(canvas_width * 0.85, canvas_height * 0.40, 
                                text=f"Velocidade CdP:", font=("Inter", fontsize22-2, "bold"), fill="#304462", anchor = "center")
        canvas_centro_pressao.create_text(canvas_width * 0.85, canvas_height * 0.46,
                                text=f"{str(round(vdcp,2))} cm/s", font=("Inter", fontsize22-2, "bold"), fill="#304462", anchor = "center")
        canvas_centro_pressao.create_text(canvas_width * 0.85, canvas_height * 0.56, 
                                text=f"DX: {str(round(Dx,2))}\nDY: {str(round(Dy,2))}", font=("Inter", fontsize-1), fill="#656565")

        btn_paciente.config(fg="#0B2243", image = bg_btn_resultado)
        btn_centro_pressao.configure(fg="#E0E0E0", image=bg_btn_click)
        btn_distr_massas.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_emg.configure(fg="#0B2243", image=bg_btn_resultado)


    if canvas == canvas_distr_massas:
        btn_paciente.config(fg="#0B2243", image = bg_btn_resultado)
        btn_centro_pressao.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_distr_massas.configure(fg="#E0E0E0", image=bg_btn_click)
        btn_emg.configure(fg="#0B2243", image=bg_btn_resultado)

    if canvas == canvas_emg:
        canvas_emg.delete("all")

        canvas_width = canvas_emg.winfo_width()
        canvas_height = canvas_emg.winfo_height()
        
        canvas_emg.create_text(canvas_width * 0.5, canvas_height * 0.1, 
        text=f"Gráfico EMG", font=("Inter", fontsize22, "bold"), fill="#304462", anchor = "center")

        btn_paciente.config(fg="#0B2243", image = bg_btn_resultado)
        btn_centro_pressao.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_distr_massas.configure(fg="#0B2243", image=bg_btn_resultado)
        btn_emg.configure(fg="#E0E0E0", image=bg_btn_click)
        canvas_emg.forget()
        canvasMatplot4.draw()


# Array para armazenar os dados
dados_salvos = []

#MARK: SALVAR DADOS()
def salvar_dados():

    global D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11
    global P0, P1, P2, P3, P4, P5, P6, P7
    global allData0, allData1, allData2, allData3, allData4, allData5, allData6, allData7, allData8, allData9, allData10, allData11, allData12, allData13, allData14, allData15, allData16, allData17, allData18, allData19
    global dxMax, dxMin, dyMax, dyMin
    
    vdcp = dados_velocidade_lista[0]
    Dx = dados_velocidade_lista[1]
    Dy = dados_velocidade_lista[2]
    
    nome = dados_paciente_lista[0]
    idade = dados_paciente_lista[1]
    altura = dados_paciente_lista[2]
    peso = dados_paciente_lista[3]
    sexo = dados_paciente_lista[4]
    tem_dor = dados_paciente_lista[5]
    nivel_dor = dados_paciente_lista[6]
    tem_queda = dados_paciente_lista[7]
    qtd_quedas = dados_paciente_lista[8]
    tem_labirintite = dados_paciente_lista[9]
    tratamento_labirintite = dados_paciente_lista[10]

    data = {
        'Nome': nome,
        'Idade': idade,
        'Altura': altura,
        'Peso': peso,
        'Sexo': sexo,
        'Dor': tem_dor,
        'Nivel_da_dor': nivel_dor,
        'Queda': tem_queda,
        'Quantidade_de_quedas': qtd_quedas,
        'Labirintite': tem_labirintite,
        'Tratamento_de_labirintite': tratamento_labirintite,
        'D0': allData0,
        'D1': allData1,
        'D2': allData2,
        'D3': allData3,
        'D4': allData4,
        'D5': allData5,
        'D6': allData6,
        'D7': allData7,
        'D12': allData12,
        'D13': allData13,
        'D14': allData14,
        'D15': allData15,
        'D16': allData16,
        'D17': allData17,
        'D18': allData18,
        'D19': allData19,
        'Tempo': vdcp,
        'Dx': Dx,
        'Dy': Dy
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

def check_box_event():
    # Identifica a variável associada à CheckBox

    ax4.clear()
    
    if check_vars[0].get() == "on":
        ax4.plot(allData4, color='blue')

    if check_vars[1].get() == "on":
        ax4.plot(allData5, color='red')

    if check_vars[2].get() == "on":
        ax4.plot(allData6, color='yellow')

    if check_vars[3].get() == "on":
        ax4.plot(allData7, color='purple')

    canvasMatplot4.draw() #Desenha o grafico
    
# Variável associada à CheckBox
check_vars = [ctk.StringVar(value="off") for _ in range(8)]

# Lista de textos das CheckBoxes
checkbox_texts = [
    "Sensor 01",
    "Sensor 02",
    "Sensor 03",
    "Sensor 04"
]

# Criação das CheckBoxes
checkboxes = []
for i in range(4):
    checkbox = ctk.CTkCheckBox(
        canvas_emg,
        text=checkbox_texts[i],
        font=("Inter", 14, "bold"),
        text_color="#0B2243",
        corner_radius=5,
        width=50,
        height=50,
        border_color="#A7BBCB",
        checkmark_color="#e0e0e0",
        fg_color="#0B2243",
        bg_color="white",
        hover_color="#A7BBCB",
        variable=check_vars[i],
        onvalue="on",
        offvalue="off",
        command=lambda: check_box_event()  # Passa o índice da checkbox
    )
    checkbox.place(relx=0.12, rely=0.42 + i * 0.08, anchor="center")
    checkboxes.append(checkbox)


#Background Botões

width_btn_resultado = int((physical_width * 12.24) / 100)
height_btn_resultado = int((physical_height * 17.6) / 100)
bg_btn_resultado1 = Image.open("UI/Resultado/btn_neutro.png")
bg_btn_resultado1 = bg_btn_resultado1.resize((width_btn_resultado, height_btn_resultado), Image.Resampling.LANCZOS)
bg_btn_resultado = ImageTk.PhotoImage(bg_btn_resultado1)


# Botões laterais
btn_paciente = Button(
    tela_resultado,
    text="PACIENTE",
    font=("Inter", fontsize22,"bold"),
    fg="#0B2243",
    image=bg_btn_resultado,
    width=(width_btn_resultado-2),
    height=(height_btn_resultado-2),
    compound="center",
    background= "#f8f8f8",
    bd=0,
    activeforeground="#E0E0E0",
    command=lambda: exibir_canvas(canvas_paciente)
)
btn_paciente.place(relx=0.1042, rely=0.32, anchor = 'nw')

btn_centro_pressao = Button(
    tela_resultado,
    text="CENTRO DE\nPRESSÃO",
    font=("Inter", fontsize22,"bold"),
    fg="#0B2243",
    image=bg_btn_resultado,
    width=(width_btn_resultado-2),
    height=(height_btn_resultado-2),
    compound="center",
    background= "#f8f8f8",
    bd=0,
    activeforeground="#E0E0E0",
    command=lambda: exibir_canvas(canvas_centro_pressao)
)
btn_centro_pressao.place(relx=0.1042, rely=0.532, anchor = 'nw')

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
    background= "#f8f8f8",
    activeforeground="#E0E0E0",
    command=lambda: exibir_canvas(canvas_distr_massas)
)
btn_distr_massas.place(relx=0.2474, rely=0.32, anchor = 'nw')

btn_emg = Button(
    tela_resultado,
    text="EMG",
    font=("Inter", fontsize22,"bold"),
    fg="#0B2243",
    image=bg_btn_resultado,
    background= "#f8f8f8",
    width=(width_btn_resultado-2),
    height=(height_btn_resultado-2),
    compound="center",
    bd=0,
    activeforeground="#E0E0E0",
    command=lambda: exibir_canvas(canvas_emg)
)
btn_emg.place(relx=0.2474, rely=0.532, anchor = 'nw')

def restart(frame): 
    frame.tkraise()
    canvas_paciente.delete("all")
    canvas_centro_pressao.delete("all")
    canvas_distr_massas.delete("all")
    canvas_emg.delete("all")

btn_voltarInicial = Button(
    tela_resultado,
    text="VOLTAR",
    font=("Inter", fontsize,"bold"),
    fg="#E0E0E0",
    image=bg_btn,
    width=((physical_width * 9.9) / 100)-2,
    height=((physical_height * 9.26) / 100)-2,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: restart(tela_inicial))
btn_voltarInicial.place(relx= 0.1042, rely=0.8611)

root.mainloop()