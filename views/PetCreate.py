import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from models.pet import Pet, Cachorro, Gato, Ave, Reptil, Roedor
from controllers.Dados import Dados


class PetCreate:
    def __init__(self, master, parent_window=None):
        self.master = master
        self.parent_window = parent_window
        self.tutor_cpf_selecionado = None
        self.master.title("Cadastro de Pet")
        self.master.geometry("900x700")

        tk.Label(master, text="Cadastro de Pet", font=("Arial", 16)).grid(row=0, column=2, columnspan=2, pady=10)
        tk.Button(master, text="Voltar", bg="#d3d3d3", command=self.voltar).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        tk.Label(master, text="Código/Microchip:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.codigo_entry = tk.Entry(master)
        self.codigo_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(master, text="Nome:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.nome_entry = tk.Entry(master)
        self.nome_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(master, text="Raça:").grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.raca_entry = tk.Entry(master)
        self.raca_entry.grid(row=2, column=3, padx=10, pady=5)

        tk.Label(master, text="Peso (kg):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.peso_entry = tk.Entry(master)
        self.peso_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(master, text="Data de Nascimento:").grid(row=3, column=2, padx=10, pady=5, sticky="e")
        self.data_entry = DateEntry(master, date_pattern="dd/mm/yyyy")
        self.data_entry.grid(row=3, column=3, padx=10, pady=5)

        tk.Label(master, text="Tutor:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.tutor_cpf_var = tk.StringVar(value="Nenhum selecionado")
        tk.Label(master, textvariable=self.tutor_cpf_var, fg="gray").grid(row=4, column=1, padx=10, pady=5, sticky="w")
        tk.Button(master, text="Buscar Tutor", command=self.buscar_tutor).grid(row=4, column=2, padx=10)

        tk.Label(master, text="Status:").grid(row=4, column=3, padx=10, pady=5, sticky="e")
        self.status_var = tk.StringVar(value="ativo")
        frame_status = tk.Frame(master)
        frame_status.grid(row=4, column=4, pady=5)
        tk.Radiobutton(frame_status, text="Ativo", variable=self.status_var, value="ativo").pack(side="left")
        tk.Radiobutton(frame_status, text="Inativo", variable=self.status_var, value="inativo").pack(side="left")

        tk.Label(master, text="Espécie:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.especie_var = tk.StringVar()
        frame_especie = tk.Frame(master)
        frame_especie.grid(row=5, column=1, columnspan=3, pady=5)
        for esp in ["Cachorro", "Gato", "Ave", "Réptil", "Roedor"]:
            tk.Radiobutton(frame_especie, text=esp, variable=self.especie_var, value=esp,
                           font=("Arial", 10), cursor="hand2",
                           command=self.atualizar_campos_extras).pack(side="left", padx=8)

        self.frame_extras = tk.Frame(master)
        self.frame_extras.grid(row=6, column=0, columnspan=4, pady=5)

        tk.Button(master, text="Cadastrar", bg="#80DD83", command=self.submit).grid(row=7, column=0, columnspan=2, pady=10)

    def buscar_tutor(self):
        top = tk.Toplevel(self.master)
        top.title("Buscar Tutor")
        top.geometry("600x300")

        tk.Label(top, text="Selecione um tutor:", font=("Arial", 12)).pack(pady=10)

        colunas = ("CPF", "Nome", "Telefone")
        tabela = ttk.Treeview(top, columns=colunas, show="headings")
        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, width=180, anchor="center")
        tabela.pack(fill="both", expand=True, padx=10)

        for t in Dados.load("tutores.json"):
            tabela.insert("", "end", values=(t.get("CPF"), t.get("name"), t.get("telefone")))

        def selecionar():
            selecionado = tabela.selection()
            if not selecionado:
                return
            cpf = tabela.item(selecionado[0])["values"][0]
            nome = tabela.item(selecionado[0])["values"][1]
            self.tutor_cpf_selecionado = cpf
            self.tutor_cpf_var.set(f"{cpf} — {nome}")
            top.destroy()
            self.master.lift()

        tk.Button(top, text="Selecionar", bg="#80DD83", command=selecionar).pack(pady=10)
        tabela.bind("<Double-1>", lambda e: selecionar())

    def atualizar_campos_extras(self):
        for widget in self.frame_extras.winfo_children():
            widget.destroy()

        especie = self.especie_var.get()

        if especie == "Cachorro":
            tk.Label(self.frame_extras, text="Porte:").grid(row=0, column=0, padx=10, sticky="e")
            self.porte_var = tk.StringVar(value="pequeno")
            for i, porte in enumerate(["pequeno", "médio", "grande"]):
                tk.Radiobutton(self.frame_extras, text=porte.capitalize(), variable=self.porte_var,
                               value=porte, cursor="hand2").grid(row=0, column=i+1)

            tk.Label(self.frame_extras, text="Vacina Raiva:").grid(row=1, column=0, padx=10, sticky="e")
            self.vacina_raiva_var = tk.BooleanVar(value=False)
            tk.Checkbutton(self.frame_extras, text="Sim", variable=self.vacina_raiva_var).grid(row=1, column=1)

        elif especie == "Gato":
            tk.Label(self.frame_extras, text="Castrado:").grid(row=0, column=0, padx=10, sticky="e")
            self.castrado_var = tk.BooleanVar(value=False)
            tk.Checkbutton(self.frame_extras, text="Sim", variable=self.castrado_var).grid(row=0, column=1)

            tk.Label(self.frame_extras, text="Tipo de Pelo:").grid(row=1, column=0, padx=10, sticky="e")
            self.tipo_pelo_var = tk.StringVar(value="curto")
            tk.Radiobutton(self.frame_extras, text="Curto", variable=self.tipo_pelo_var, value="curto").grid(row=1, column=1)
            tk.Radiobutton(self.frame_extras, text="Longo", variable=self.tipo_pelo_var, value="longo").grid(row=1, column=2)

        elif especie == "Ave":
            tk.Label(self.frame_extras, text="Anilha:").grid(row=0, column=0, padx=10, sticky="e")
            self.anilha_entry = tk.Entry(self.frame_extras)
            self.anilha_entry.grid(row=0, column=1, padx=10)

            tk.Label(self.frame_extras, text="Espécie Exótica:").grid(row=0, column=2, padx=10, sticky="e")
            self.exotica_var = tk.BooleanVar(value=False)
            tk.Checkbutton(self.frame_extras, text="Sim", variable=self.exotica_var).grid(row=0, column=3)

    def submit(self):
        codigo = self.codigo_entry.get().strip()
        nome = self.nome_entry.get().strip()
        raca = self.raca_entry.get().strip()
        peso = self.peso_entry.get().strip()
        tutor_cpf = self.tutor_cpf_selecionado
        status = self.status_var.get()
        especie = self.especie_var.get()
        data_nascimento = self.data_entry.get_date()

        if not all([codigo, nome, raca, peso, especie]):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            self.master.lift()
            return

        if not tutor_cpf:
            messagebox.showerror("Erro", "Selecione um tutor.")
            self.master.lift()
            return

        try:
            peso = float(peso)
        except ValueError:
            messagebox.showerror("Erro", "Peso deve ser um número.")
            self.master.lift()
            return

        if especie == "Cachorro":
            pet = Cachorro(codigo, nome, raca, data_nascimento, peso, tutor_cpf,
                           self.porte_var.get(), self.vacina_raiva_var.get(), status)
        elif especie == "Gato":
            pet = Gato(codigo, nome, raca, data_nascimento, peso, tutor_cpf,
                       self.castrado_var.get(), self.tipo_pelo_var.get(), status)
        elif especie == "Ave":
            pet = Ave(codigo, nome, raca, data_nascimento, peso, tutor_cpf,
                      self.anilha_entry.get().strip(), self.exotica_var.get(), status)
        elif especie == "Réptil":
            pet = Reptil(codigo, nome, raca, data_nascimento, peso, tutor_cpf, status)
        elif especie == "Roedor":
            pet = Roedor(codigo, nome, raca, data_nascimento, peso, tutor_cpf, status)

        animais = Dados.load("pets.json")
        animais.append(pet.to_dict())
        Dados.save("pets.json", animais)

        messagebox.showinfo("Sucesso", "Pet cadastrado com sucesso!")
        self.master.destroy()
        if self.parent_window:
            self.parent_window.deiconify()

    def voltar(self):
        if self.parent_window:
            self.parent_window.deiconify()
        self.master.destroy()