import tkinter as tk
from tkinter import ttk
from controllers.Dados import Dados


class TutorList:
    def __init__(self, master, parent_window=None):
        self.master = master
        self.parent_window = parent_window
        self.master.title("Lista de Tutores")
        self.master.geometry("900x400")

        tk.Label(master, text="Lista de Tutores", font=("Arial", 16)).pack(pady=10)

        self.back_button = tk.Button(master, text="Voltar", bg="#d3d3d3", command=self.voltar)
        self.back_button.pack(anchor="w", padx=10)

        # Tabela
        colunas = ("CPF", "Nome", "Telefone", "Email", "Endereço", "Tipo")
        self.tabela = ttk.Treeview(master, columns=colunas, show="headings")

        for col in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=140, anchor="center")

        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)

        self.carregar()

    def carregar(self):
        # Limpa a tabela antes de carregar
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        tutores = Dados.load("tutores.json")
        for tutor in tutores:
            self.tabela.insert("", "end", values=(
                tutor.get("CPF"),
                tutor.get("name"),
                tutor.get("telefone"),
                tutor.get("email"),
                tutor.get("address"),
                tutor.get("tipo"),
            ))

    def voltar(self):
        if self.parent_window:
            self.parent_window.deiconify()
        self.master.destroy()