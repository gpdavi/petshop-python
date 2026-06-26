import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

from models.Serviços import Servico, Consulta, BanhoTosa, Vacinacao, Hospedagem
from controllers.Dados import Dados


class ServiceCreate:
    def __init__(self, master, parent_window=None):
        self.master = master
        self.parent_window = parent_window
        self.master.title("Cadastro de Serviço")
        self.master.geometry("700x550")

        tk.Label(master, text="Cadastro de Serviço", font=("Arial", 16)).grid(row=0, column=2, columnspan=2, pady=10)
        tk.Button(master, text="Voltar", bg="#d3d3d3", command=self.voltar).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        tk.Label(master, text="Código:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.codigo_entry = tk.Entry(master)
        self.codigo_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(master, text="Nome:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.nome_entry = tk.Entry(master)
        self.nome_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(master, text="Descrição:").grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.descricao_entry = tk.Entry(master)
        self.descricao_entry.grid(row=2, column=3, padx=10, pady=5)

        tk.Label(master, text="Valor Base (R$):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.valor_entry = tk.Entry(master)
        self.valor_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(master, text="Duração (min):").grid(row=3, column=2, padx=10, pady=5, sticky="e")
        self.duracao_entry = tk.Entry(master)
        self.duracao_entry.grid(row=3, column=3, padx=10, pady=5)

        tk.Label(master, text="Requer Agendamento:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.agendamento_var = tk.BooleanVar(value=True)
        frame_agendamento = tk.Frame(master)
        frame_agendamento.grid(row=4, column=1, pady=5)
        tk.Radiobutton(frame_agendamento, text="Sim", variable=self.agendamento_var, value=True).pack(side="left")
        tk.Radiobutton(frame_agendamento, text="Não", variable=self.agendamento_var, value=False).pack(side="left")

        tk.Label(master, text="Tipo:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.tipo_var = tk.StringVar()
        frame_tipo = tk.Frame(master)
        frame_tipo.grid(row=5, column=1, columnspan=3, pady=5)
        for tipo in ["Consulta", "BanhoTosa", "Vacinação", "Hospedagem"]:
            tk.Radiobutton(frame_tipo, text=tipo, variable=self.tipo_var, value=tipo,
                           font=("Arial", 10), cursor="hand2",
                           command=self.atualizar_campos_extras).pack(side="left", padx=8)

        self.frame_extras = tk.Frame(master)
        self.frame_extras.grid(row=6, column=0, columnspan=4, pady=5)

        tk.Button(master, text="Cadastrar", bg="#80DD83", command=self.submit).grid(row=7, column=0, columnspan=2, pady=10)

    def atualizar_campos_extras(self):
        for widget in self.frame_extras.winfo_children():
            widget.destroy()

        tipo = self.tipo_var.get()

        if tipo == "Consulta":
            tk.Label(self.frame_extras, text="Veterinário:").grid(row=0, column=0, padx=10, sticky="e")
            self.veterinario_entry = tk.Entry(self.frame_extras)
            self.veterinario_entry.grid(row=0, column=1, padx=10)

            tk.Label(self.frame_extras, text="Especialidade:").grid(row=0, column=2, padx=10, sticky="e")
            self.especialidade_entry = tk.Entry(self.frame_extras)
            self.especialidade_entry.grid(row=0, column=3, padx=10)

        elif tipo == "BanhoTosa":
            tk.Label(self.frame_extras, text="Corte de Unhas:").grid(row=0, column=0, padx=10, sticky="e")
            self.corte_unhas_var = tk.BooleanVar(value=False)
            tk.Checkbutton(self.frame_extras, text="Sim", variable=self.corte_unhas_var).grid(row=0, column=1)

            tk.Label(self.frame_extras, text="Perfume:").grid(row=0, column=2, padx=10, sticky="e")
            self.perfume_entry = tk.Entry(self.frame_extras)
            self.perfume_entry.grid(row=0, column=3, padx=10)

        elif tipo == "Vacinação":
            tk.Label(self.frame_extras, text="Lote:").grid(row=0, column=0, padx=10, sticky="e")
            self.lote_entry = tk.Entry(self.frame_extras)
            self.lote_entry.grid(row=0, column=1, padx=10)

            tk.Label(self.frame_extras, text="Laboratório:").grid(row=0, column=2, padx=10, sticky="e")
            self.laboratorio_entry = tk.Entry(self.frame_extras)
            self.laboratorio_entry.grid(row=0, column=3, padx=10)

            tk.Label(self.frame_extras, text="Data de Validade:").grid(row=1, column=0, padx=10, sticky="e")
            self.data_validade_entry = DateEntry(self.frame_extras, date_pattern="dd/mm/yyyy")
            self.data_validade_entry.grid(row=1, column=1, padx=10)

        elif tipo == "Hospedagem":
            tk.Label(self.frame_extras, text="Valor Diária (R$):").grid(row=0, column=0, padx=10, sticky="e")
            self.valor_diaria_entry = tk.Entry(self.frame_extras)
            self.valor_diaria_entry.grid(row=0, column=1, padx=10)

            tk.Label(self.frame_extras, text="Capacidade:").grid(row=0, column=2, padx=10, sticky="e")
            self.capacidade_entry = tk.Entry(self.frame_extras)
            self.capacidade_entry.grid(row=0, column=3, padx=10)

    def submit(self):
        codigo = self.codigo_entry.get().strip()
        nome = self.nome_entry.get().strip()
        descricao = self.descricao_entry.get().strip()
        valor_base = self.valor_entry.get().strip()
        duracao = self.duracao_entry.get().strip()
        requer_agendamento = self.agendamento_var.get()
        tipo = self.tipo_var.get()

        if not all([codigo, nome, descricao, valor_base, duracao, tipo]):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            self.master.lift()
            return

        try:
            valor_base = float(valor_base)
        except ValueError:
            messagebox.showerror("Erro", "Valor base deve ser um número.")
            self.master.lift()
            return

        try:
            duracao = int(duracao)
        except ValueError:
            messagebox.showerror("Erro", "Duração deve ser um número inteiro.")
            self.master.lift()
            return

        if tipo == "Consulta":
            veterinario = self.veterinario_entry.get().strip()
            especialidade = self.especialidade_entry.get().strip()
            if not all([veterinario, especialidade]):
                messagebox.showerror("Erro", "Preencha todos os campos da consulta.")
                self.master.lift()
                return
            servico = Consulta(codigo, nome, descricao, valor_base, duracao, veterinario, especialidade)

        elif tipo == "BanhoTosa":
            perfume = self.perfume_entry.get().strip()
            servico = BanhoTosa(codigo, nome, descricao, valor_base, duracao,
                                self.corte_unhas_var.get(), perfume or None)

        elif tipo == "Vacinação":
            lote = self.lote_entry.get().strip()
            laboratorio = self.laboratorio_entry.get().strip()
            data_validade = self.data_validade_entry.get_date()
            if not all([lote, laboratorio]):
                messagebox.showerror("Erro", "Preencha todos os campos da vacinação.")
                self.master.lift()
                return
            servico = Vacinacao(codigo, nome, descricao, valor_base, duracao,
                                lote, data_validade, laboratorio)

        elif tipo == "Hospedagem":
            capacidade = self.capacidade_entry.get().strip()
            valor_diaria = self.valor_diaria_entry.get().strip()
            try:
                valor_diaria = float(valor_diaria)
                capacidade = int(capacidade)
            except ValueError:
                messagebox.showerror("Erro", "Valor diária e capacidade devem ser números.")
                self.master.lift()
                return
            servico = Hospedagem(codigo, nome, descricao, valor_base, duracao,
                                 valor_diaria, capacidade)

        servicos = Dados.load("servicos.json")
        servicos.append(servico.to_dict())
        Dados.save("servicos.json", servicos)

        messagebox.showinfo("Sucesso", "Serviço cadastrado com sucesso!")
        self.master.destroy()
        if self.parent_window:
            self.parent_window.deiconify()

    def voltar(self):
        if self.parent_window:
            self.parent_window.deiconify()
        self.master.destroy()