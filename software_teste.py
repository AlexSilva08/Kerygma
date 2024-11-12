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

is_fullscreen = True
def toogle_fullscreen():
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)

# For para posicionamento das telas
for frame in (tela_inicial, tela_dados, tela_parametros, tela_resultado): 
    frame.grid(row=0, column=0, sticky='nsew')

show_frame(tela_inicial)
bg_image = PhotoImage(file="UI/background.png")

#Bg botão geral
bg_buttons = Image.open("UI/btn_bg.png")
bg_buttons = bg_buttons.resize((150, 50), Image.LANCZOS)
bg_buttons_ctk = ImageTk.PhotoImage(bg_buttons)

# Tela Inicial
canvas_inicial = Canvas(tela_inicial, width=1920, height=1080)
canvas_inicial.grid(row=0, column=0)
canvas_inicial.create_image(0, 0, image=bg_image, anchor="nw")

# Botão de fechar
btn_fechar = ctk.CTkButton(
    tela_inicial,
    text="X",
    font=("Helvetica", 16, "bold"),
    corner_radius=14,
    width=50,
    height=40,
    text_color="#ffffff", 
    fg_color="#3e567c",
    hover_color="#2b3a52",
    command=lambda: close_app()
)
btn_fechar.place(relx=0.88, rely=0.05)

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
toogle_button.place(relx=0.92, rely=0.05)

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
    text="Iniciar",
    font=("Helvetica", 16,"bold"),
    fg="#D9D9D9",
    image=bg_buttons_ctk,
    width=150,
    height=50,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: show_frame(tela_dados) 
)
btn_iniciar.place(relx=0.5, rely=0.6, anchor='center')

# Tela Dados
canvas_dados = Canvas(tela_dados, width=1920, height=1080)
canvas_dados.grid(row=0, column=0)
canvas_dados.create_image(0, 0, image=bg_image, anchor="nw")

# Título
canvas_dados.create_text(
    640, 50,
    text="Dados do Paciente", 
    font=('Arial', 24, 'bold'),
    fill="#3e567c"
)

# Entradas de dados do paciente
entradas = []

nome_paciente = ctk.CTkEntry(tela_dados, width=200, placeholder_text="Nome")
nome_paciente.place(relx=0.08, rely=0.3)
entradas.append(nome_paciente)

idade_paciente = ctk.CTkEntry(tela_dados, width=200, placeholder_text="Idade")
idade_paciente.place(relx=0.08, rely=0.35)
entradas.append(idade_paciente)

altura_paciente = ctk.CTkEntry(tela_dados, width=200, placeholder_text="Altura")
altura_paciente.place(relx=0.08, rely=0.40)
entradas.append(altura_paciente)

peso_paciente = ctk.CTkEntry(tela_dados, width=200, placeholder_text="Peso")
peso_paciente.place(relx=0.08, rely=0.45)
entradas.append(peso_paciente)

btn_armazenardados = Button(
    tela_dados,
    text="Salvar",
    font=("Helveticsa", 17,"bold"),
    fg="#D9D9D9",
    image=bg_buttons_ctk,
    width=150,
    height=50,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: armazenar_dados()
)
btn_armazenardados.place(relx=0.08, rely=0.55)

# Função para armazenar os dados em uma lista
dados_paciente_lista = []
def armazenar_dados():
    global dados_paciente_lista
    dados_paciente_lista = [entrada.get() for entrada in entradas]
    for entrada in entradas:
        entrada.delete(0, END)

# Função para exibir os dados salvos na tela de resultado
def dados_paciente(tela_resultado):
    show_frame(tela_resultado)
    exibir_canvas(canvas_centro_pressao)
    canvas_dadospaciente = Canvas(tela_resultado, width=1115, height= 90, bg= "#3e567c")
    canvas_dadospaciente.place(relx=0.48, rely=0.2, anchor='center')

    canvas_dadospaciente.create_text(120, 45, text=f"Nome: {dados_paciente_lista[0]}", font=("Calibri", 18), fill="#ffffff")
    canvas_dadospaciente.create_text(350, 45, text=f"Idade: {dados_paciente_lista[1]}", font=("Calibri", 18), fill="#ffffff")
    canvas_dadospaciente.create_text(500, 45, text=f"Altura: {dados_paciente_lista[2]}", font=("Calibri", 18), fill="#ffffff")
    canvas_dadospaciente.create_text(650, 45, text=f"Peso: {dados_paciente_lista[3]}", font=("Calibri", 18), fill="#ffffff")

# Botão Ler Laudo
btn_abrirArquivo = Button(
    tela_dados,
    text="Ler Laudo",
    font=("Helveticsa", 17,"bold"),
    fg="#D9D9D9",
    image=bg_buttons_ctk,
    width=150,
    height=50,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: dados_paciente(tela_resultado)
)
btn_abrirArquivo.place(relx=0.08, rely=0.88)

# Tela Resultado
canvas_resultado = Canvas(tela_resultado, width=1920, height=1080)
canvas_resultado.grid(row=0, column=0)
canvas_resultado.create_image(0, 0, image=bg_image, anchor="nw")

# Título
canvas_resultado.create_text(
    640, 50, 
    text="Resultado", 
    font=('Arial', 24, 'bold'), 
    fill="#3e567c"
)

# Canvas Detalhes
canvas_centro_pressao = Canvas(tela_resultado, width=790, height=380, bg="#ffffff")
canvas_distr_massas = Canvas(tela_resultado, width=790, height=380, bg="#ffffff")
canvas_velocidade = Canvas(tela_resultado, width=790, height=380, bg="#ffffff")
canvas_emg = Canvas(tela_resultado, width=790, height=380, bg="#ffffff")

# Posicionamento relativo
canvas_centro_pressao.place(relx=0.6, rely=0.55, anchor='center')
canvas_distr_massas.place(relx=0.6, rely=0.55, anchor='center')
canvas_velocidade.place(relx=0.6, rely=0.55, anchor='center')
canvas_emg.place(relx=0.6, rely=0.55, anchor='center')


# Texto
canvas_centro_pressao.create_text(395, 100, text="Centro de Pressão", font=("Arial", 20, "bold"), fill="#000000")
canvas_distr_massas.create_text(395, 100, text="Distribuição de Massa", font=("Arial", 20, "bold"), fill="#000000")
canvas_velocidade.create_text(395, 100, text="Velocidade", font=("Arial", 20, "bold"), fill="#000000")
canvas_emg.create_text(395, 100, text="EMG", font=("Arial", 20, "bold"), fill="#000000")


# Função para exibir o canvas correto
def exibir_canvas(canvas):
    canvas_distr_massas.place_forget()
    canvas_velocidade.place_forget()
    canvas_emg.place_forget()
    canvas_centro_pressao.place_forget()
    
    canvas.place(relx=0.6, rely=0.55, anchor='center')

# Botões laterais
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
    command=lambda: exibir_canvas(canvas_centro_pressao)
)
btn_centro_pressao.place(relx=0.08, rely=0.35)

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
    command=lambda: exibir_canvas(canvas_distr_massas)
)
btn_distr_massas.place(relx=0.08, rely=0.45)

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
    command=lambda: exibir_canvas(canvas_velocidade)
)
btn_velocidade.place(relx=0.08, rely=0.55)

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
    command=lambda: exibir_canvas(canvas_emg)
)
btn_emg.place(relx=0.08, rely=0.65)

def restart(frame): 
    frame.tkraise()
    canvas_centro_pressao.delete("all")
    canvas_distr_massas.delete("all")
    canvas_velocidade.delete("all")
    canvas_emg.delete("all")

btn_voltarInicial = Button(
    tela_resultado,
    text="Voltar ao Início",
    font=("Helveticsa", 16,"bold"),
    fg="#D9D9D9",
    image=bg_buttons_ctk,
    width=150,
    height=50,
    compound="center",
    bd=0,
    activeforeground="#f7c360",
    command=lambda: restart(tela_inicial))
btn_voltarInicial.place(relx= 0.85, rely=0.88)


root.mainloop()