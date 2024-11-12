from tkinter import *
from tkinter import PhotoImage
from PIL import Image, ImageTk 
import customtkinter as ctk

root = ctk.CTk()
root.title("Nome do Software")
root.geometry("1280x720")
root.minsize(width=1280, height=720)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.attributes("-fullscreen", True)

# Criação das telas    
tela_inicial = Frame(root)
tela_dados = Frame(root)
tela_parametros = Frame(root)
tela_resultado = Frame(root)

# Função para trazer a tela pra frente
def show_frame(frame): 
    frame.tkraise()

def close_app():
    root.destroy()

is_fullscreen=True
def toogle_fullscreen():
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)

# For para posicionamento das telas
for frame in (tela_inicial, tela_dados, tela_parametros, tela_resultado): 
    frame.grid(row=0, column=0, sticky='nsew')

show_frame(tela_inicial)
bg_image = PhotoImage(file="D:/Kerygma/UI/background.png")

# Tela Inicial
canvas_inicial = Canvas(tela_inicial, width=1920, height=1080)
canvas_inicial.grid(row=0, column=0)

canvas_inicial.create_image(0, 0, image=bg_image, anchor="nw")

btn_fechar = ctk.CTkButton(
    tela_inicial,
    text="X",
    font=("Helvetica",16, "bold"),
    corner_radius=14,
    width=50,
    height=40,
    text_color="#ffffff", 
    fg_color="#3e567c",
    hover_color="#2b3a52",
    command=lambda: close_app())
btn_fechar.place(relx=0.88, rely=0.05)

icon_fullscreen = Image.open("D:/Kerygma/UI/icon_fullscreen.png")  # Abra a imagem original
icon_fullscreen_rezied = icon_fullscreen.resize((40, 40), Image.LANCZOS)
icon_fullscreen = ImageTk.PhotoImage(icon_fullscreen_rezied)
toogle_button = Button(
    tela_inicial,
    image=icon_fullscreen,
    bd=0,
    highlightthickness=0,
    command=toogle_fullscreen
)
toogle_button.place(relx=0.92, rely=0.05)

#Título
canvas_inicial.create_text(
    640, 50,
    text="Tela Inicial", 
    font=('Arial', 24, 'bold'), 
    fill="#3e567c")

# Configuração de Botões Inicial
btn_iniciar = ctk.CTkButton(
    tela_inicial,
    text="Iniciar",
    font=("Helvetica",16, "bold"),
    corner_radius=14,
    width=150,
    height=40,
    text_color="#ffffff", 
    fg_color="#3e567c",
    hover_color="#2b3a52",
    command=lambda: show_frame(tela_dados))
btn_iniciar.place(relx=0.5, rely=0.6, anchor='center')

# Tela Dados
canvas_dados = Canvas(tela_dados, width=1920, height=1080)
canvas_dados.grid(row=0, column=0)
canvas_dados.create_image(0, 0, image=bg_image, anchor="nw")

#Título
canvas_dados.create_text(
    640, 50, 
    text="Dados do Paciente", 
    font=('Arial', 24, 'bold'), 
    fill="#3e567c")

# Configuração de Botões
btn_abrirArquivo = ctk.CTkButton(
    tela_dados,
    text="Ler Laudo",
    font=("Helvetica",16, "bold"),
    corner_radius=14,
    width=150,
    height=40,
    text_color="#ffffff", 
    fg_color="#3e567c",
    hover_color="#2b3a52",
    command=lambda: show_frame(tela_resultado))
btn_abrirArquivo.place(relx=0.08, rely=0.88)

# Tela Resultado
canvas_resultado = Canvas(tela_resultado, width=1920, height=1080)
canvas_resultado.grid(row=0, column=0)
canvas_resultado.create_image(0, 0, image=bg_image, anchor="nw")

#Título
canvas_resultado.create_text(
    640, 50, 
    text="Resultado", 
    font=('Arial', 24, 'bold'), 
    fill="#3e567c")

def exibir_canvas(titulo, caminho_imagem):
    global canvas_detalhe
    canvas_detalhe = Canvas(tela_resultado, width=790, height=380, bg="#ffffff")

    # Posicionando o canvas_detalhe centralizado na tela usando relx e rely
    canvas_detalhe.place(relx=0.5, rely=0.5, anchor='center')  # centraliza na tela
    
    # Adicionando o título dentro do canvas
    canvas_detalhe.create_text(395, 40, text=titulo, font=('Arial', 16, 'bold'), fill="#3e567c")

    # Carregar e exibir a imagem
    img = Image.open(caminho_imagem)
    img_tk = ImageTk.PhotoImage(img)
    
    # Exibir imagem no centro do canvas
    canvas_detalhe.create_image(395, 180, image=img_tk)
    canvas_detalhe.image = img_tk

btn_centro_pressao = ctk.CTkButton(
    tela_resultado,
    text="Centro de Pressão",
    font=("Helvetica",16, "bold"),
    corner_radius=14,
    width=150,
    height=50,
    text_color="#ffffff", 
    fg_color="#3e567c",
    hover_color="#2b3a52",
    command=lambda: exibir_canvas("Centro de Pressão", "F:/Kerygma/UI/button1.png")
)
btn_centro_pressao.place(relx=0.08, rely=0.3)

btn_distr_massas = ctk.CTkButton(
    tela_resultado,
    text="Distribuição de Massas",
    font=("Helvetica",16, "bold"),
    corner_radius=14,
    width=150,
    height=50,
    text_color="#ffffff", 
    fg_color="#3e567c",
    hover_color="#2b3a52",
    command=lambda: exibir_canvas("Distribuição de Massas", "F:/Kerygma/UI/button2.png")
)
btn_distr_massas.place(relx=0.08, rely=0.4)

btn_velocidade = ctk.CTkButton(
    tela_resultado,
    text="Velocidade",
    font=("Helvetica",16, "bold"),
    corner_radius=14,
    width=150,
    height=50,
    text_color="#ffffff", 
    fg_color="#3e567c",
    hover_color="#2b3a52",
    command=lambda: exibir_canvas("Velocidade", "F:/Kerygma/UI/button1.png")
)
btn_velocidade.place(relx=0.08, rely=0.5)

btn_emg = ctk.CTkButton(
    tela_resultado,
    text="EMG",
    font=("Helvetica",16, "bold"),
    corner_radius=14,
    width=150,
    height=50,
    text_color="#ffffff", 
    fg_color="#3e567c",
    hover_color="#2b3a52",
    command=lambda: exibir_canvas("EMG", "F:/Kerygma/UI/button2.png")
)
btn_emg.place(relx=0.08, rely=0.6)

# Configuração de Botões

def restart(frame): 
    frame.tkraise()
    canvas_detalhe.delete("all")

btn_voltarInicial = ctk.CTkButton(
    tela_resultado,
    text="Voltar ao Início",
    font=("Helvetica",16, "bold"),
    corner_radius=14,
    width=150,
    height=40,
    text_color="#ffffff", 
    fg_color="#3e567c",
    hover_color="#2b3a52",
    command=lambda: restart(tela_inicial))
btn_voltarInicial.place(relx= 0.85, rely=0.88)

root.mainloop()
