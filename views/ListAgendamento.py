import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date

from controllers.Dados import Dados
from views.CreateAgendamento import CreateAgendamento


class ListAgendamento:
    def __init__(self, master, parent_window=None):
        self.master = master
        self.parent_window = parent_window
        self.master.title("Listagem de Agendamentos")
        self.master.geometry("1050x560")

        self.agendamentos = []
        self.servicos = []
        self.STATUS_EDITAVEIS = ["agendado", "em andamento", "cancelado", "concluído"]

        self._build_header()
        self._build_toolbar()
        self._build_table()
        self._build_footer()

        self.carregar_dados()

    # ------------------------------------------------------------------ #
    #  Build                                                               #
    # ------------------------------------------------------------------ #

    def _build_header(self):
        tk.Label(self.master, text="Agendamentos", font=("Arial", 16)).grid(
            row=0, column=0, columnspan=6, pady=(12, 2))
        tk.Button(self.master, text="Voltar", bg="#d3d3d3", command=self.voltar).grid(
            row=0, column=0, sticky="w", padx=10)

    def _build_toolbar(self):
        frame = tk.Frame(self.master)
        frame.grid(row=1, column=0, columnspan=6, padx=10, pady=6, sticky="ew")
        self.master.columnconfigure(0, weight=1)

        # Busca pet
        tk.Label(frame, text="Pet:").pack(side="left")
        self.pet_var = tk.StringVar()
        self.pet_var.trace_add("write", lambda *_: self.filtrar())
        tk.Entry(frame, textvariable=self.pet_var, width=16).pack(side="left", padx=(4, 10))

        # Filtro serviço
        tk.Label(frame, text="Serviço:").pack(side="left")
        self.servico_var = tk.StringVar(value="Todos")
        self.combo_servico = ttk.Combobox(
            frame, textvariable=self.servico_var,
            state="readonly", width=18
        )
        self.combo_servico.pack(side="left", padx=(4, 10))
        self.servico_var.trace_add("write", lambda *_: self.filtrar())

        # Filtro status
        tk.Label(frame, text="Status:").pack(side="left")
        self.status_var = tk.StringVar(value="Todos")
        ttk.Combobox(
            frame, textvariable=self.status_var,
            values=["Todos", "agendado", "em andamento", "concluído", "cancelado", "não compareceu"],
            state="readonly", width=16
        ).pack(side="left", padx=(4, 10))
        self.status_var.trace_add("write", lambda *_: self.filtrar())

        # Filtro data
        tk.Label(frame, text="De:").pack(side="left")
        self.data_ini = DateEntry(frame, date_pattern="dd/mm/yyyy", width=10)
        self.data_ini.set_date(date.today().replace(day=1))
        self.data_ini.pack(side="left", padx=(4, 4))
        self.data_ini.bind("<<DateEntrySelected>>", lambda _: self.filtrar())

        tk.Label(frame, text="Até:").pack(side="left")
        self.data_fim = DateEntry(frame, date_pattern="dd/mm/yyyy", width=10)
        self.data_fim.pack(side="left", padx=(4, 10))
        self.data_fim.bind("<<DateEntrySelected>>", lambda _: self.filtrar())

        tk.Button(frame, text="Limpar filtros", bg="#d3d3d3",
                  command=self.limpar_filtros).pack(side="left", padx=(0, 10))

        tk.Button(frame, text="+ Novo Agendamento", bg="#80DD83",
                  command=self.abrir_cadastro).pack(side="right")

    def _build_table(self):
        frame = tk.Frame(self.master)
        frame.grid(row=2, column=0, columnspan=6, padx=10, pady=4, sticky="nsew")
        self.master.rowconfigure(2, weight=1)

        colunas = ("codigo", "pet", "servicos", "inicio", "termino",
                   "duracao", "valor", "fds", "status")
        self.tree = ttk.Treeview(frame, columns=colunas, show="headings", selectmode="browse")

        headers = {
            "codigo":   ("Código",     70),
            "pet":      ("Pet",       130),
            "servicos": ("Serviços",  180),
            "inicio":   ("Início",    120),
            "termino":  ("Término",   120),
            "duracao":  ("Duração",    70),
            "valor":    ("Valor",       85),
            "fds":      ("FDS",         40),
            "status":   ("Status",     110),
        }
        for col, (label, width) in headers.items():
            self.tree.heading(col, text=label,
                              command=lambda c=col: self.ordenar(c))
            self.tree.column(col, width=width, anchor="w")

        self.tree.column("valor", anchor="e")
        self.tree.column("duracao", anchor="center")
        self.tree.column("fds", anchor="center")

        # Tags de cor por status
        self.tree.tag_configure("agendado",        background="#EBF5FB")
        self.tree.tag_configure("em andamento",    background="#EAFAF1")
        self.tree.tag_configure("concluído",       background="#F2F3F4")
        self.tree.tag_configure("cancelado",       background="#FDEDEC")
        self.tree.tag_configure("não compareceu",  background="#FEF9E7")

        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.tree.bind("<Double-1>", lambda _: self.editar_status())

        # Botões de ação
        btn_frame = tk.Frame(self.master)
        btn_frame.grid(row=3, column=0, columnspan=6, padx=10, pady=6, sticky="w")
        tk.Button(btn_frame, text="Alterar Status", bg="#80DD83",
                  command=self.editar_status).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Excluir", bg="#f28b82",
                  command=self.excluir_selecionado).pack(side="left", padx=4)

    def _build_footer(self):
        self.status_bar = tk.StringVar(value="")
        tk.Label(self.master, textvariable=self.status_bar, fg="gray").grid(
            row=4, column=0, columnspan=6, pady=(0, 6))

    # ------------------------------------------------------------------ #
    #  Dados                                                               #
    # ------------------------------------------------------------------ #

    def carregar_dados(self):
        self.agendamentos = Dados.load("agendamentos.json")
        self.servicos = Dados.load("servicos.json")

        nomes_servicos = ["Todos"] + sorted({
            s.get("nome", "") for s in self.servicos if s.get("nome")
        })
        self.combo_servico["values"] = nomes_servicos

        self.filtrar()

    def _nome_servicos(self, codigos):
        """Retorna string com os nomes dos serviços a partir dos códigos."""
        mapa = {s["codigo"]: s.get("nome", s["codigo"]) for s in self.servicos}
        return ", ".join(mapa.get(c, c) for c in codigos)

    # ------------------------------------------------------------------ #
    #  Filtro e exibição                                                   #
    # ------------------------------------------------------------------ #

    def filtrar(self):
        query_pet = self.pet_var.get().lower()
        filtro_status = self.status_var.get()
        filtro_servico = self.servico_var.get()
        d_ini = self.data_ini.get_date()
        d_fim = self.data_fim.get_date()

        resultado = []
        for ag in self.agendamentos:
            # Pet
            pet_nome = ag.get("animal", {})
            if isinstance(pet_nome, dict):
                pet_nome = pet_nome.get("nome", "")
            if query_pet and query_pet not in pet_nome.lower():
                continue

            # Status
            if filtro_status != "Todos" and ag.get("status") != filtro_status:
                continue

            # Serviço — verifica se algum dos serviços do agendamento bate
            if filtro_servico != "Todos":
                codigos = ag.get("servicos", [])
                nomes = self._nome_servicos(codigos)
                if filtro_servico not in nomes:
                    continue

            # Data
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(ag.get("data_hora_inicio", "")).date()
                if not (d_ini <= dt <= d_fim):
                    continue
            except (ValueError, TypeError):
                pass

            resultado.append(ag)

        self._popular_tree(resultado)
        total = len(resultado)
        self.status_bar.set(
            f"{total} agendamento{'s' if total != 1 else ''} encontrado{'s' if total != 1 else ''}"
        )

    def _popular_tree(self, lista):
        self.tree.delete(*self.tree.get_children())
        for ag in lista:
            # Pet
            animal = ag.get("animal", {})
            pet_nome = animal.get("nome", str(animal)) if isinstance(animal, dict) else str(animal)

            # Serviços
            codigos = ag.get("servicos", [])
            svcs_str = self._nome_servicos(codigos)

            # Datas
            def fmt_dt(iso):
                try:
                    from datetime import datetime
                    return datetime.fromisoformat(iso).strftime("%d/%m/%Y %H:%M")
                except Exception:
                    return iso or "—"

            fds = "✓" if ag.get("eh_fim_de_semana") else ""
            valor = f"R$ {float(ag.get('valor_total', 0)):.2f}"
            duracao = f"{ag.get('duracao_total', 0)} min"
            status = ag.get("status", "")

            self.tree.insert("", "end", values=(
                ag.get("codigo", ""),
                pet_nome,
                svcs_str,
                fmt_dt(ag.get("data_hora_inicio")),
                fmt_dt(ag.get("data_hora_termino")),
                duracao,
                valor,
                fds,
                status,
            ), tags=(status,))

    # ------------------------------------------------------------------ #
    #  Ações                                                               #
    # ------------------------------------------------------------------ #

    def _agendamento_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um agendamento.")
            self.master.lift()
            return None
        codigo = self.tree.item(sel[0], "values")[0]
        return next((ag for ag in self.agendamentos if ag.get("codigo") == codigo), None)

    def editar_status(self):
        ag = self._agendamento_selecionado()
        if not ag:
            return

        modal = tk.Toplevel(self.master)
        modal.title("Alterar Status")
        modal.geometry("300x160")
        modal.grab_set()
        modal.resizable(False, False)

        tk.Label(modal, text=f"Agendamento: {ag['codigo']}", font=("Arial", 11)).pack(pady=(14, 2))
        tk.Label(modal, text="Novo status:").pack()

        novo_status = tk.StringVar(value=ag.get("status", "agendado"))
        ttk.Combobox(
            modal,
            textvariable=novo_status,
            values=self.STATUS_EDITAVEIS,
            state="readonly",
            width=20
        ).pack(pady=6)

        def confirmar():
            ag["status"] = novo_status.get()
            Dados.save("agendamentos.json", self.agendamentos)
            modal.destroy()
            self.filtrar()
            messagebox.showinfo("Sucesso", "Status atualizado.")
            self.master.lift()

        tk.Button(modal, text="Confirmar", bg="#80DD83", command=confirmar).pack(pady=6)

    def excluir_selecionado(self):
        ag = self._agendamento_selecionado()
        if not ag:
            return
        if not messagebox.askyesno(
            "Confirmar exclusão",
            f"Excluir o agendamento '{ag['codigo']}'?"
        ):
            return
        self.agendamentos = [a for a in self.agendamentos if a.get("codigo") != ag["codigo"]]
        Dados.save("agendamentos.json", self.agendamentos)
        self.filtrar()
        messagebox.showinfo("Sucesso", "Agendamento excluído.")
        self.master.lift()

    def limpar_filtros(self):
        self.pet_var.set("")
        self.status_var.set("Todos")
        self.servico_var.set("Todos")
        self.data_ini.set_date(date.today().replace(day=1))
        self.data_fim.set_date(date.today())
        self.filtrar()

    def abrir_cadastro(self):
        self.master.withdraw()
        nova = tk.Toplevel()
        CreateAgendamento(nova, parent_window=self.master)
        nova.protocol("WM_DELETE_WINDOW", lambda: (
            nova.destroy(),
            self.master.deiconify(),
            self.carregar_dados()
        ))

    def ordenar(self, coluna):
        items = [(self.tree.set(k, coluna), k) for k in self.tree.get_children("")]
        items.sort()
        for i, (_, k) in enumerate(items):
            self.tree.move(k, "", i)

    def voltar(self):
        if self.parent_window:
            self.parent_window.deiconify()
        self.master.destroy()