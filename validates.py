import re
import customtkinter as ctk
from tkinter import *
from tkinter import PhotoImage
from PIL import Image, ImageTk 
import customtkinter as ctk

# -------------------- Validações --------------------

def validar_nome(texto):
    if texto == "":  # Permitir campo vazio
        return True
    if texto.replace(" ", "").isalpha():  # Verifica se contém apenas letras e espaços
        return True
    return False

def validar_idade(valor):
    """ Permite apenas números entre 0 e 100 para idade. """
    if not valor:
        return True  # Permite campo vazio
    return valor.isdigit() and 0 <= int(valor) <= 100

def validar_altura(valor):
    """ Permite altura no formato 1.75 ou 175 cm. """
    if not valor:
        return True  # Permite campo vazio
    # Permite 1.75 ou 175 (sem letras)
    if re.match(r"^\d{1,3}(\.\d{0,2})?$", valor):
        return True
    
    return False

def validar_peso(valor):
    """ Permite peso no formato 50, 70.5, 120.3. """
    if not valor:
        return True  # Permite campo vazio
    try:
        peso = float(valor)
        return 1 <= peso <= 300  # Limita peso entre 1 e 300 kg
    except ValueError:
        return False
    
def validar_dor(valor, placeholder):
    if valor == "":
        return True  
    if valor.isdigit() and 0 <= int(valor) <= 10:  
        placeholder.place_forget()  # Esconde o placeholder ao digitar um número válido
        return True  
    return False  # Bloqueia entrada inválida

def validar_queda(valor, placeholder):
    if valor == "":
        return True
    else:
        placeholder.place_forget()  # Esconde o placeholder quando há texto
        return valor.isdigit() and 0 <= int(valor) <= 100  # Valida números entre 0 e 100

def validar_labirintite(texto, placeholder):
    if texto == "":  # Se estiver vazio, exibe o placeholder
        return True
    if texto.replace(" ", "").isalpha():  # Verifica se contém apenas letras e espaços
        placeholder.place_forget()  # Esconde o placeholder ao digitar um texto válido
        return True
    return False


def validar_parametros(valor):
    if not valor:
        return True  # Permite campo vazio
    return valor.isdigit()


# -------------------- Formatações --------------------

def formatar_altura(valor):
    """
    Converte altura para o formato padronizado:
    - "1.75" -> "1.75 m"
    - "175"  -> "1.75 m"
    """
    if not valor:
        return ""
    
    try:
        altura = float(valor.replace(",", "."))  # Permite vírgula também
        if altura >= 100:  # Se for em cm, converte para metros
            altura = altura / 100
        return f"{altura:.2f} m"
    except ValueError:
        return valor  # Retorna sem formatar caso não seja um número válido

def formatar_peso(valor):
    """
    Converte peso para o formato padronizado:
    - "70" -> "70 kg"
    - "70.5" -> "70.5 kg"
    """
    if not valor:
        return ""
    
    try:
        peso = float(valor.replace(",", "."))  # Permite vírgula também
        return f"{peso:.1f} kg"
    except ValueError:
        return valor  # Retorna sem formatar caso não seja um número válido