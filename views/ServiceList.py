import tkinter as tk
from tkinter import ttk, messagebox

from controllers.Dados import Dados


class ServiceList:
    def __init__(self, master, parent_window=None):
        self.master = master
        self.parent_window = parent_window
        self.master.title("Listagem de Serviços")
        self.master.geometry("900x520")

        self._build_header()
        self._build_toolbar()
        self._build_table()
        self._build_footer()

        self.carregar_servicos()

    def _build_header(self):
        tk.Label(
            self.master,
            text="Serviços",
            font=("Arial", 16)
        ).grid(row=0, column=0, columnspan=4, pady=(12, 2))

        tk.Button(
            self.master,
            text="Voltar",
            bg="#d3d3d3",
            command=self.voltar
        ).grid(row=0, column=0, sticky="w", padx=10)

    def _build_toolbar(self):
        frame = tk.Frame(self.master)
        frame.grid(row=1, column=0, columnspan=4, padx=10, pady=6, sticky="ew")
        self.master.columnconfigure(0, weight=1)

        tk.Label(frame, text="Buscar:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.filtrar())
        tk.Entry(frame, textvariable=self.search_var, width=28).pack(side="left", padx=(4, 12))

        tk.Label(frame, text="Tipo:").pack(side="left")
        self.tipo_var = tk.StringVar(value="Todos")
        tipos = ["Todos", "consulta veterinária", "banho e tosa", "vacinação", "hospedagem"]
        ttk.Combobox(
            frame,
            textvariable=self.tipo_var,
            values=tipos,
            state="readonly",
            width=18
        ).pack(side="left", padx=(4, 12))
        self.tipo_var.trace_add("write", lambda *_: self.filtrar())

        tk.Button(
            frame,
            text="+ Novo Serviço",
            bg="#80DD83",
            command=self.abrir_cadastro
        ).pack(side="right")

    def _build_table(self):
        frame = tk.Frame(self.master)
        frame.grid(row=2, column=0, columnspan=4, padx=10, pady=4, sticky="nsew")
        self.master.rowconfigure(2, weight=1)

        colunas = ("codigo", "nome", "tipo", "descricao", "valor_base", "duracao", "agendamento")
        self.tree = ttk.Treeview(frame, columns=colunas, show="headings", selectmode="browse")

        headers = {
            "codigo":       ("Código",        70),
            "nome":         ("Nome",          160),
            "tipo":         ("Tipo",          130),
            "descricao":    ("Descrição",     180),
            "valor_base":   ("Valor Base",     90),
            "duracao":      ("Duração (min)",  90),
            "agendamento":  ("Agendamento",    90),
        }
        for col, (label, width) in headers.items():
            self.tree.heading(col, text=label, command=lambda c=col: self.ordenar(c))
            self.tree.column(col, width=width, anchor="w")

        self.tree.column("valor_base", anchor="e")
        self.tree.column("duracao", anchor="center")
        self.tree.column("agendamento", anchor="center")

        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", self.on_double_click)

        btn_frame = tk.Frame(self.master)
        btn_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=6, sticky="w")
        tk.Button(btn_frame, text="Ver / Editar", command=self.editar_selecionado).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Excluir", bg="#f28b82", command=self.excluir_selecionado).pack(side="left", padx=4)

    def _build_footer(self):
        self.status_var = tk.StringVar(value="")
        tk.Label(self.master, textvariable=self.status_var, fg="gray").grid(
            row=4, column=0, columnspan=4, pady=(0, 8)
        )

    def carregar_servicos(self):
        self.servicos = Dados.load("servicos.json")
        self.filtrar()

    def filtrar(self):
        query = self.search_var.get().lower()
        tipo_filtro = self.tipo_var.get()

        resultado = [
            s for s in self.servicos
            if (query in s.get("codigo", "").lower() or query in s.get("nome", "").lower())
            and (tipo_filtro == "Todos" or s.get("tipo") == tipo_filtro)
        ]

        self.tree.delete(*self.tree.get_children())
        for s in resultado:
            agendamento = "Sim" if s.get("requer_agendamento") else "Não"
            valor = f"R$ {float(s.get('valor_base', 0)):.2f}"
            self.tree.insert("", "end", values=(
                s.get("codigo", ""),
                s.get("nome", ""),
                s.get("tipo", ""),
                s.get("descricao", ""),
                valor,
                s.get("duracao", ""),
                agendamento,
            ))

        total = len(resultado)
        self.status_var.set(f"{total} serviço{'s' if total != 1 else ''} encontrado{'s' if total != 1 else ''}")

    def ordenar(self, coluna):
        items = [(self.tree.set(k, coluna), k) for k in self.tree.get_children("")]
        items.sort()
        for index, (_, k) in enumerate(items):
            self.tree.move(k, "", index)

    def _item_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um serviço.")
            self.master.lift()
            return None
        valores = self.tree.item(sel[0], "values")
        codigo = valores[0]
        return next((s for s in self.servicos if s.get("codigo") == codigo), None)

    def on_double_click(self, event):
        self.editar_selecionado()

    def editar_selecionado(self):
        servico = self._item_selecionado()
        if servico:
            # Abrir janela de edição passando os dados do serviço
            messagebox.showinfo("Editar", f"Editar serviço: {servico['nome']}")
            self.master.lift()

    def excluir_selecionado(self):
        servico = self._item_selecionado()
        if not servico:
            return
        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Excluir o serviço '{servico['nome']}' ({servico['codigo']})?",
        )
        if confirmar:
            self.servicos = [s for s in self.servicos if s.get("codigo") != servico["codigo"]]
            Dados.save("servicos.json", self.servicos)
            self.filtrar()
            messagebox.showinfo("Sucesso", "Serviço excluído.")
            self.master.lift()

    def abrir_cadastro(self):
        from views.ServiceCreate import ServiceCreate
        self.master.withdraw()
        nova = tk.Toplevel()
        ServiceCreate(nova, parent_window=self.master)
        nova.protocol("WM_DELETE_WINDOW", lambda: (nova.destroy(), self.master.deiconify(), self.carregar_servicos()))

    def voltar(self):
        if self.parent_window:
            self.parent_window.deiconify()
        self.master.destroy()