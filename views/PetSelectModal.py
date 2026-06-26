import tkinter as tk
from tkinter import ttk, messagebox

from controllers.Dados import Dados


class PetSelectModal:
    def __init__(self, master, on_select):
        """
        on_select: callback chamado com o dict do pet selecionado
        """
        self.on_select = on_select
        self.top = tk.Toplevel(master)
        self.top.title("Selecionar Pet")
        self.top.geometry("620x420")
        self.top.grab_set()  # bloqueia a janela pai enquanto está aberta

        self._build()
        self.carregar_pets()

    def _build(self):
        tk.Label(self.top, text="Selecionar Pet", font=("Arial", 14)).pack(pady=(12, 4))

        frame_busca = tk.Frame(self.top)
        frame_busca.pack(fill="x", padx=12, pady=4)
        tk.Label(frame_busca, text="Buscar:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.filtrar())
        tk.Entry(frame_busca, textvariable=self.search_var, width=30).pack(side="left", padx=6)

        frame_tree = tk.Frame(self.top)
        frame_tree.pack(fill="both", expand=True, padx=12, pady=4)

        colunas = ("codigo", "nome", "especie", "raca", "tutor")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", selectmode="browse")

        headers = {
            "codigo":  ("Código",  70),
            "nome":    ("Nome",   140),
            "especie": ("Espécie", 90),
            "raca":    ("Raça",   120),
            "tutor":   ("Tutor",  150),
        }
        for col, (label, width) in headers.items():
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, anchor="w")

        scroll = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda _: self.confirmar())

        frame_btn = tk.Frame(self.top)
        frame_btn.pack(pady=8)
        tk.Button(frame_btn, text="Selecionar", bg="#80DD83", command=self.confirmar).pack(side="left", padx=6)
        tk.Button(frame_btn, text="Cancelar", bg="#d3d3d3", command=self.top.destroy).pack(side="left", padx=6)

    def carregar_pets(self):
        self.pets = [p for p in Dados.load("pets.json") if p.get("ativo", True)]
        self.filtrar()

    def filtrar(self):
        query = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        for p in self.pets:
            if query in p.get("codigo", "").lower() or query in p.get("nome", "").lower():
                self.tree.insert("", "end", values=(
                    p.get("codigo", ""),
                    p.get("nome", ""),
                    p.get("especie", ""),
                    p.get("raca", ""),
                    p.get("tutor", ""),
                ))

    def confirmar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um pet.", parent=self.top)
            return
        codigo = self.tree.item(sel[0], "values")[0]
        pet = next((p for p in self.pets if p["codigo"] == codigo), None)
        if pet:
            self.on_select(pet)
            self.top.destroy()