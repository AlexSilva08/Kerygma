import customtkinter as ctk
from tkinter import *
from tkinter import PhotoImage
from PIL import Image, ImageTk 
import customtkinter as ctk


############################################################################  SPIN BOX
entrada = []

class CustomSpinbox(ctk.CTkFrame):
    def __init__(self, master, min_value, max_value, step=1, screen_width=1920, screen_height=1080, new_value=0, **kwargs):
        super().__init__(master, fg_color="#0b2243", border_width=0, **kwargs)

        # Atributos da Spinbox
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_value = IntVar(value=new_value)

        fontsize = int((self.screen_height * 1.7) / 100)  # Fonte padrão
        fontsize_large = int((self.screen_height * 1.7) / 100)  # Fonte maior para "+" e "-"

        # Personalizações
        self.btn_color = "#0b2243"  
        self.btn_text_color = "#e0e0e0"  
        self.font = ("Intern", fontsize, "bold")  # Fonte normal
        self.font_large = ("Intern", fontsize_large, "bold")  # Fonte maior para "+" e "-"
        self.border_color = "#a7bbcb"  
        self._border_width = 0  
        self.btn_hover_color = "#304462"  
        self.columnconfigure((0, 1, 2, 3, 4), weight=1)

        button_width = int(self.screen_width * 1.5 / 100)  
        button_height = int(screen_height * 2.7 / 100)  
        entry_width = int(self.screen_width * 2.1 / 100)  

        # Botão "<" (diminuir -10)
        self.decrement_by_10_button = ctk.CTkButton(
            self, text="<<", width=button_width, height=button_height,
            fg_color=self.btn_color, text_color=self.btn_text_color, font=self.font, hover_color=self.btn_hover_color,
            command=self.decrement_by_10)
        self.decrement_by_10_button.grid(row=0, column=0, padx=1, pady=5)

        # Botão "-" (diminuir 1) - Fonte maior
        self.decrement_button = ctk.CTkButton(
            self, text="<", width=button_width, height=button_height,
            fg_color=self.btn_color, text_color=self.btn_text_color, font=self.font_large, hover_color=self.btn_hover_color,
            command=self.decrement)
        self.decrement_button.grid(row=0, column=1, padx=1, pady=5)

        # Entrada de valor
        self.entry = ctk.CTkEntry(
            self, textvariable=self.current_value, width=entry_width, height=(screen_height * 3 / 100),
            font=self.font, justify="center", border_color=self.border_color, border_width=self._border_width,
            fg_color="#FFFFFF", text_color="#2F2F2F")
        self.entry.grid(row=0, column=2, padx=2, pady=5)
        self.entry.bind("<FocusOut>", self.validate_value)

        # Botão "+" (aumentar 1) - Fonte maior
        self.increment_button = ctk.CTkButton(
            self, text=">", width=button_width, height=button_height,
            fg_color=self.btn_color, text_color=self.btn_text_color, font=self.font_large, hover_color=self.btn_hover_color,
            command=self.increment)
        self.increment_button.grid(row=0, column=3, padx=1, pady=5)

        # Botão ">" (aumentar +10)
        self.increment_by_10_button = ctk.CTkButton(
            self, text=">>", width=button_width, height=button_height,
            fg_color=self.btn_color, text_color=self.btn_text_color, font=self.font, hover_color=self.btn_hover_color,
            command=self.increment_by_10)
        self.increment_by_10_button.grid(row=0, column=4, padx=1, pady=5)

    def increment(self):
        value = self.current_value.get()
        if value < self.max_value:
            self.current_value.set(value + self.step)
        if self.current_value.get() > self.max_value:
            self.current_value.set(self.max_value)

    def decrement(self):
        value = self.current_value.get()
        if value > self.min_value:
            self.current_value.set(value - self.step)
        if self.current_value.get() < self.min_value:
            self.current_value.set(self.min_value)

    def increment_by_10(self):
        value = self.current_value.get()
        if value + 10 <= self.max_value:
            self.current_value.set(value + 10)
        else:
            self.current_value.set(self.max_value)

    def decrement_by_10(self):
        value = self.current_value.get()
        if value - 10 >= self.min_value:
            self.current_value.set(value - 10)
        else:
            self.current_value.set(self.min_value)

    def validate_value(self, event=None):
        try:
            value = int(self.entry.get())
            if value < self.min_value:
                self.current_value.set(self.min_value)
            elif value > self.max_value:
                self.current_value.set(self.max_value)
        except ValueError:
            self.current_value.set(self.min_value)

    def set(self, new_value):
        self.current_value.set(new_value)

    def get(self):
        return self.current_value.get()



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

    def reset_button_text(self):
        self.button.configure(text="Escolha uma opção")
        
    def get(self):
        return self.button.cget("text")
    