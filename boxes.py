import customtkinter as ctk
from tkinter import *
from tkinter import PhotoImage
from PIL import Image, ImageTk 
import customtkinter as ctk

############################################################################  SPIN BOX
entrada = []

# Spinbox customizada
class CustomSpinbox(ctk.CTkFrame):
    def __init__(self, master, min_value=0, max_value=100, **kwargs):
        super().__init__(master,fg_color="#0b2243", border_width=0, **kwargs)
        
        # Atributos da Spinbox
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = IntVar(value=min_value)
        
        # Personalizações
        self.btn_color = "#0b2243"               # Cor de fundo dos botões
        self.btn_text_color = "#e0e0e0"           # Cor do texto dos botões
        self.entry_width = 50                  # Largura do campo de entrada
        self.font = ("Intern", 14, "bold")       # Fonte e estilo do texto
        self.border_color="#a7bbcb"                 # Cor da borda
        self._border_width=0                        # Tamanho da borda
        self.btn_hover_color = "#304462"            # Hover do botão


        self.columnconfigure((0, 2), weight=1)
        
        # Botão para diminuir o valor
        self.decrement_button = ctk.CTkButton(
            self, text="-", width =28, fg_color=self.btn_color, 
            text_color=self.btn_text_color, font=self.font, hover_color=self.btn_hover_color,
            command=self.decrement)
        self.decrement_button.grid(row=0, column=0, padx=2, pady=5)
        
        # Entrada para mostrar e editar o valor
        self.entry = ctk.CTkEntry(
            self, textvariable=self.current_value, width=self.entry_width,
            font=self.font, justify="center", border_color=self.border_color, border_width=self._border_width)
        self.entry.grid(row=0, column=1, padx=2, pady=5)
        self.entry.bind("<FocusOut>", self.validate_value)
        entrada.append(self.entry)

        # Botão para aumentar o valor
        self.increment_button = ctk.CTkButton(
            self, text="+", width=28, fg_color=self.btn_color, 
            text_color=self.btn_text_color, font=self.font, hover_color=self.btn_hover_color,
            command=self.increment)
        self.increment_button.grid(row=0, column=2, padx=2, pady=5)
    
    def increment(self):
        value = self.current_value.get()
        if value < self.max_value:
            self.current_value.set(value + 1)
            if value < self.min_value:
                self.current_value.set(self.min_value)
        if value > self.max_value:
            self.current_value.set(self.max_value)

    def decrement(self):
        value = self.current_value.get()
        if value > self.min_value:
            self.current_value.set(value - 1)
            if value > self.max_value:
                self.current_value.set(self.max_value)
        if value < self.min_value:
                self.current_value.set(self.min_value)
    
    def validate_value(self, event=None):
        try:
            value = int(self.entry.get())
            if value < self.min_value:
                self.current_value.set(self.min_value)
            elif value > self.max_value:
                self.current_value.set(self.max_value)
        except ValueError:
            self.current_value.set(self.min_value)  # Volta ao mínimo se valor inválido


############################################################################################# COMBO BOX

class CustomComboBox:
    def __init__(self, master, values, width, height, font, button_color, dropdown_fg_color, dropdown_text_color, bg_color,
                 img_seta, text_color, button_hover_color, dropdown_hover_color,border_color, border_width, corner_radius):
        
        self.master = master
        self.values = values
        self.width = width
        self.height = height
        self.font = font
        self.button_color = button_color
        self.dropdown_fg_color = dropdown_fg_color
        self.dropdown_text_color = dropdown_text_color
        self.text_color = text_color
        self.button_hover_color = button_hover_color
        self.dropdown_hover_color = dropdown_hover_color
        self.arrow_image = img_seta
        self.border_color = border_color
        self.border_width = border_width
        self.corner_radius = corner_radius
        self.bg_color = bg_color

        # Combobox Button (campo principal)
        self.button = ctk.CTkButton(
            master,
            text="Escolha uma opção",
            width=self.width,
            height=self.height,
            font=self.font,
            fg_color=self.button_color,
            text_color=self.text_color,
            hover_color=self.button_hover_color,
            image=self.arrow_image,
            compound="right",
            border_color= self.border_color, 
            border_width= self.border_width,
            corner_radius= self.corner_radius,
            bg_color= self.bg_color,
            command=self.toggle_dropdown
        )
        
        # Dropdown Menu
        self.dropdown_frame = ctk.CTkFrame(
            master,
            fg_color=self.dropdown_fg_color,
            width=self.width
        )
        
        self.buttons = []
        for i, value in enumerate(self.values):
            btn = ctk.CTkButton(
                self.dropdown_frame,
                text=value,
                width=self.width,
                height=self.height,
                font=self.font,
                fg_color=self.dropdown_fg_color,
                text_color=self.dropdown_text_color,
                hover_color=self.dropdown_hover_color,
                command=lambda v=value: self.select_item(v)
            )
            self.buttons.append(btn)
        
        for i, btn in enumerate(self.buttons):
            btn.grid(row=i, padx=5, pady=5)

        self.dropdown_visible = False

    def grid (self, **kwargs):
        self.button.grid(**kwargs)

    def pack (self, **kwargs):
        self.button.pack(**kwargs)

    def place(self, **kwargs):
        self.button.place(**kwargs)

    def toggle_dropdown(self):
        if self.dropdown_visible:
            self.dropdown_frame.place_forget()
        else:
            button_x = self.button.winfo_x()
            button_y = self.button.winfo_y() + self.button.winfo_height()
            self.dropdown_frame.place(x=button_x, y=button_y)
        
        self.dropdown_visible = not self.dropdown_visible

    def select_item(self, value):
        self.button.configure(text=value)
        self.toggle_dropdown()

    def get(self):
        return self.button.cget("text")