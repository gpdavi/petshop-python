import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from models.pet import Pet, Cachorro, Gato, Ave, Reptil, Roedor
from controllers.Dados import Dados
from views.PetEdit import PetEdit


class PetList:
    def __init__(self, master, parent_window=None):
        self.master = master
        self.parent_window = parent_window
        self.master.title("Lista de Pets")
        self.master.geometry("950x450")

        tk.Label(master, text="Lista de Pets", font=("Arial", 16)).pack(pady=10)

        frame_topo = tk.Frame(master)
        frame_topo.pack(fill="x", padx=10)

        tk.Button(frame_topo, text="Voltar", bg="#d3d3d3", command=self.voltar).pack(side="left")
        tk.Button(frame_topo, text="Editar Selecionado", bg="#80DD83", command=self.abrir_edicao).pack(side="right")

        colunas = ("Código", "Nome", "Espécie", "Raça", "Idade", "Peso", "Tutor CPF", "Status")
        self.tabela = ttk.Treeview(master, columns=colunas, show="headings")

        for col in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=110, anchor="center")

        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabela.bind("<Double-1>", lambda e: self.abrir_edicao())

        self.carregar()

    def calcular_idade(self, data_nascimento_str):
        try:
            partes = data_nascimento_str.split("-")
            nascimento = date(int(partes[0]), int(partes[1]), int(partes[2]))
            hoje = date.today()
            anos = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
            meses = (hoje.month - nascimento.month) % 12
            return f"{anos}a {meses}m"
        except:
            return "?"

    def carregar(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for pet in Dados.load("pets.json"):
            self.tabela.insert("", "end", values=(
                pet.get("codigo"),
                pet.get("nome"),
                pet.get("especie"),
                pet.get("raca"),
                self.calcular_idade(pet.get("data_nascimento", "")),
                pet.get("peso"),
                pet.get("tutor_cpf"),
                pet.get("status"),
            ))

    def abrir_edicao(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um pet para editar.")
            return

        codigo = self.tabela.item(selecionado[0])["values"][0]
        pets = Dados.load("pets.json")
        pet = next((a for a in pets if a["codigo"] == str(codigo)), None)

        if not pet:
            messagebox.showerror("Erro", "Pet não encontrado.")
            return

        top = tk.Toplevel(self.master)
        PetEdit(top, pet, parent_list=self)

    def voltar(self):
        if self.parent_window:
            self.parent_window.deiconify()
        self.master.destroy()