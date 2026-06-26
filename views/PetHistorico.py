import tkinter as tk
from tkinter import ttk
from datetime import datetime

from controllers.Dados import Dados


class PetHistorico:
    """
    Exibe o histórico de agendamentos/serviços prestados a um pet específico.

    No agendamentos.json, o campo "animal" é apenas o código do pet (string),
    e "servicos" é uma lista de códigos de serviço — não dicts completos.
    Por isso cruzamos com servicos.json para mostrar nome/valor de cada item.
    """

    def __init__(self, master, pet):
        self.master = master
        self.pet = pet
        self.master.title(f"Histórico — {pet.get('nome', '')}")
        self.master.geometry("780x420")

        tk.Label(
            self.master,
            text=f"Histórico de {pet.get('nome', '')} ({pet.get('codigo', '')})",
            font=("Arial", 14)
        ).pack(pady=(12, 4))

        frame_topo = tk.Frame(self.master)
        frame_topo.pack(fill="x", padx=10)
        tk.Button(frame_topo, text="Fechar", bg="#d3d3d3", command=self.master.destroy).pack(side="left")

        colunas = ("Código", "Data/Hora", "Serviços", "Duração", "Valor", "Status")
        self.tabela = ttk.Treeview(self.master, columns=colunas, show="headings")
        larguras = (90, 130, 260, 80, 90, 110)
        for col, largura in zip(colunas, larguras):
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=largura, anchor="center")
        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)

        # Resumo simples no rodapé: total de atendimentos e valor acumulado
        self.resumo_label = tk.Label(self.master, text="", fg="#555")
        self.resumo_label.pack(pady=(0, 10))

        self.carregar()

    def carregar(self):
        agendamentos = Dados.load("agendamentos.json")
        servicos_cadastrados = {s["codigo"]: s for s in Dados.load("servicos.json")}

        codigo_pet = self.pet.get("codigo")
        historico = [a for a in agendamentos if a.get("animal") == codigo_pet]

        # Mais recentes primeiro
        historico.sort(key=lambda a: a.get("data_hora_inicio", ""), reverse=True)

        total_valor = 0.0
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for ag in historico:
            nomes_servicos = [
                servicos_cadastrados[cod]["nome"]
                for cod in ag.get("servicos", [])
                if cod in servicos_cadastrados
            ]

            data_str = self._formatar_data(ag.get("data_hora_inicio"))
            valor = ag.get("valor_total", 0.0) or 0.0
            total_valor += valor

            self.tabela.insert("", "end", values=(
                ag.get("codigo", ""),
                data_str,
                ", ".join(nomes_servicos) if nomes_servicos else "—",
                f"{ag.get('duracao_total', 0)} min",
                f"R$ {valor:.2f}",
                ag.get("status", ""),
            ))

        self.resumo_label.config(
            text=f"{len(historico)} atendimento(s)  •  Total gasto: R$ {total_valor:.2f}"
        )

    @staticmethod
    def _formatar_data(data_iso):
        if not data_iso:
            return "—"
        try:
            return datetime.fromisoformat(data_iso).strftime("%d/%m/%Y %H:%M")
        except ValueError:
            return data_iso