import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

from controllers.Dados import Dados
from controllers.AgendamentoLogic import AgendamentoCalculator
from models.Agendamento import Agendamento
from views.PetSelectModal import PetSelectModal
from controllers.VerificationAgendamento import VerificationAgendamento

class CreateAgendamento:
    def __init__(self, master, parent_window=None):
        self.master = master
        self.parent_window = parent_window
        self.master.title("Cadastro de Agendamento")
        self.master.geometry("700x680")

        self.pet_selecionado = None
        self.check_vars = {}        # codigo -> BooleanVar
        self.tutor_vars = {}        # codigo -> StringVar
        self.tutor_combos = {}      # codigo -> Combobox widget
        self.funcionarios = []

        self._build()
        self.carregar_dados()
        self.atualizar_preview()  # garante que o resumo nasça consistente com o estado inicial

    # ------------------------------------------------------------------ #
    #  Build                                                               #
    # ------------------------------------------------------------------ #

    def _build(self):
        tk.Label(self.master, text="Cadastro de Agendamento", font=("Arial", 16)).grid(
            row=0, column=0, columnspan=4, pady=(12, 4))
        tk.Button(self.master, text="Voltar", bg="#d3d3d3", command=self.voltar).grid(
            row=0, column=0, sticky="w", padx=10)

        # Código
        tk.Label(self.master, text="Código:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.codigo_entry = tk.Entry(self.master)
        self.codigo_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Pet
        tk.Label(self.master, text="Pet:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        frame_pet = tk.Frame(self.master)
        frame_pet.grid(row=2, column=1, columnspan=3, sticky="w", padx=10, pady=5)
        self.pet_label = tk.Label(frame_pet, text="Nenhum pet selecionado", fg="gray", width=35, anchor="w")
        self.pet_label.pack(side="left")
        tk.Button(frame_pet, text="Selecionar Pet", command=self.abrir_selecao_pet).pack(side="left", padx=6)

        # Data e hora início
        tk.Label(self.master, text="Data início:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.data_entry = DateEntry(self.master, date_pattern="dd/mm/yyyy")
        self.data_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        self.data_entry.bind("<<DateEntrySelected>>", lambda _: self.atualizar_preview())

        tk.Label(self.master, text="Hora início:").grid(row=3, column=2, sticky="e", padx=10, pady=5)
        frame_hora = tk.Frame(self.master)
        frame_hora.grid(row=3, column=3, sticky="w", padx=10, pady=5)
        self.hora_var = tk.StringVar(value="08")
        self.min_var = tk.StringVar(value="00")

        spin_hora = ttk.Spinbox(
            frame_hora, from_=0, to=23, width=4, textvariable=self.hora_var,
            format="%02.0f", command=self.atualizar_preview
        )
        spin_hora.pack(side="left")
        tk.Label(frame_hora, text=":").pack(side="left")
        spin_min = ttk.Spinbox(
            frame_hora, from_=0, to=59, width=4, textvariable=self.min_var,
            format="%02.0f", command=self.atualizar_preview
        )
        spin_min.pack(side="left")

        # command do Spinbox só dispara ao clicar nas setinhas; bind cobre
        # digitação manual e setas do teclado, que são os casos mais comuns.
        for spin in (spin_hora, spin_min):
            spin.bind("<KeyRelease>", lambda _: self.atualizar_preview())
            spin.bind("<FocusOut>", lambda _: self.atualizar_preview())

        # Tempo extra
        tk.Label(self.master, text="Tempo extra:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        frame_extra = tk.Frame(self.master)
        frame_extra.grid(row=4, column=1, sticky="w", padx=10, pady=5)
        self.tempo_extra_var = tk.StringVar(value="0")
        spin_extra = ttk.Spinbox(
            frame_extra, from_=0, to=600, increment=5, width=6,
            textvariable=self.tempo_extra_var,
            command=self.atualizar_preview
        )
        spin_extra.pack(side="left")
        spin_extra.bind("<KeyRelease>", lambda _: self.atualizar_preview())
        spin_extra.bind("<FocusOut>", lambda _: self.atualizar_preview())
        tk.Label(frame_extra, text="min adicionais ao término", fg="gray").pack(side="left", padx=6)

        # Serviços
        tk.Label(self.master, text="Serviços:").grid(row=5, column=0, sticky="ne", padx=10, pady=5)
        frame_svcs_outer = tk.Frame(self.master, bd=1, relief="sunken")
        frame_svcs_outer.grid(row=5, column=1, columnspan=3, sticky="ew", padx=10, pady=5)

        self.canvas = tk.Canvas(frame_svcs_outer, height=180, highlightthickness=0)
        scroll = ttk.Scrollbar(frame_svcs_outer, orient="vertical", command=self.canvas.yview)
        self.frame_servicos = tk.Frame(self.canvas)
        self.frame_servicos.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.frame_servicos, anchor="nw")
        self.canvas.configure(yscrollcommand=scroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Resumo
        frame_preview = tk.LabelFrame(self.master, text="Resumo", padx=8, pady=6)
        frame_preview.grid(row=6, column=0, columnspan=4, sticky="ew", padx=12, pady=6)
        frame_preview.columnconfigure(1, weight=1)
        frame_preview.columnconfigure(3, weight=1)

        tk.Label(frame_preview, text="Término previsto:").grid(row=0, column=0, sticky="e", padx=6)
        self.termino_label = tk.Label(frame_preview, text="—", fg="#555")
        self.termino_label.grid(row=0, column=1, sticky="w")

        tk.Label(frame_preview, text="Duração total:").grid(row=0, column=2, sticky="e", padx=6)
        self.duracao_label = tk.Label(frame_preview, text="—", fg="#555")
        self.duracao_label.grid(row=0, column=3, sticky="w")

        tk.Label(frame_preview, text="Valor total:").grid(row=1, column=0, sticky="e", padx=6)
        self.valor_label = tk.Label(frame_preview, text="—", fg="#555")
        self.valor_label.grid(row=1, column=1, sticky="w")

        tk.Label(frame_preview, text="Fim de semana:").grid(row=1, column=2, sticky="e", padx=6)
        self.fds_label = tk.Label(frame_preview, text="—", fg="#555")
        self.fds_label.grid(row=1, column=3, sticky="w")

        # Status e observações
        tk.Label(self.master, text="Status:").grid(row=7, column=0, sticky="e", padx=10, pady=5)
        self.status_var = tk.StringVar(value="agendado")
        ttk.Combobox(
            self.master, textvariable=self.status_var,
            values=list(Agendamento.STATUS_VALIDOS),
            state="readonly", width=20
        ).grid(row=7, column=1, sticky="w", padx=10, pady=5)

        tk.Label(self.master, text="Observações:").grid(row=8, column=0, sticky="ne", padx=10, pady=5)
        self.obs_text = tk.Text(self.master, height=3, width=45)
        self.obs_text.grid(row=8, column=1, columnspan=3, padx=10, pady=5, sticky="ew")

        tk.Button(self.master, text="Cadastrar", bg="#80DD83", command=self.submit).grid(
            row=9, column=0, columnspan=4, pady=14)

    # ------------------------------------------------------------------ #
    #  Dados                                                               #
    # ------------------------------------------------------------------ #

    def carregar_dados(self):
        self.funcionarios = Dados.load("funcionarios.json")
        self.servicos = Dados.load("servicos.json")
        self._popular_servicos()

    def _nomes_funcionarios(self):
        """Retorna lista de strings 'codigo — nome' para os dropdowns."""
        return ["— Nenhum —"] + [
            f"{f.get('codigo', '')} — {f.get('nome', '')}"
            for f in self.funcionarios
        ]

    def _popular_servicos(self):
        for widget in self.frame_servicos.winfo_children():
            widget.destroy()
        self.check_vars.clear()
        self.tutor_vars.clear()
        self.tutor_combos.clear()

        nomes_func = self._nomes_funcionarios()

        for s in self.servicos:
            codigo = s["codigo"]
            row = tk.Frame(self.frame_servicos)
            row.pack(fill="x", padx=6, pady=2)

            # Checkbox do serviço
            var = tk.BooleanVar(value=False)
            self.check_vars[codigo] = var
            texto = f"{codigo} — {s['nome']}  ({s['tipo']})  R$ {float(s['valor_base']):.2f}  {s['duracao']}min"
            cb = tk.Checkbutton(
                row, text=texto, variable=var, anchor="w",
                command=lambda c=codigo: self._on_check(c)
            )
            cb.pack(side="left")

            # Dropdown de funcionário (começa desabilitado)
            tutor_var = tk.StringVar(value="— Nenhum —")
            self.tutor_vars[codigo] = tutor_var
            combo = ttk.Combobox(
                row, textvariable=tutor_var,
                values=nomes_func, state="disabled", width=24
            )
            combo.pack(side="left", padx=(10, 0))
            self.tutor_combos[codigo] = combo

        # Após repopular a lista, o resumo precisa refletir o estado (tudo desmarcado)
        self.atualizar_preview()

    def _on_check(self, codigo):
        """Habilita/desabilita o dropdown do serviço marcado."""
        marcado = self.check_vars[codigo].get()
        self.tutor_combos[codigo].config(state="readonly" if marcado else "disabled")
        if not marcado:
            self.tutor_vars[codigo].set("— Nenhum —")
        self.atualizar_preview()

    # ------------------------------------------------------------------ #
    #  Pet                                                                 #
    # ------------------------------------------------------------------ #

    def abrir_selecao_pet(self):
        PetSelectModal(self.master, on_select=self._on_pet_selecionado)

    def _on_pet_selecionado(self, pet):
        self.pet_selecionado = pet
        self.pet_label.config(
            text=f"{pet['codigo']} — {pet['nome']} ({pet.get('especie', '')})",
            fg="black"
        )

    # ------------------------------------------------------------------ #
    #  Preview                                                             #
    # ------------------------------------------------------------------ #

    def _servicos_selecionados(self):
        return [s for s in self.servicos if self.check_vars[s["codigo"]].get()]

    def _data_hora_inicio(self):
        data = self.data_entry.get_date()
        hora, minuto = self._hora_minuto_validados()
        return datetime(data.year, data.month, data.day, hora, minuto)

    def _hora_minuto_validados(self):
        """
        Lê hora_var/min_var com validação de faixa, já que o usuário pode
        digitar valores fora do intervalo (ex.: 25, -3, texto vazio).
        """
        try:
            hora = int(self.hora_var.get())
        except ValueError:
            hora = 8
        try:
            minuto = int(self.min_var.get())
        except ValueError:
            minuto = 0

        hora = min(max(hora, 0), 23)
        minuto = min(max(minuto, 0), 59)
        return hora, minuto

    def _tempo_extra(self):
        try:
            return max(0, int(self.tempo_extra_var.get()))
        except ValueError:
            return 0

    def atualizar_preview(self):
        servicos = self._servicos_selecionados()
        if not servicos:
            for label in (self.termino_label, self.duracao_label, self.valor_label, self.fds_label):
                label.config(text="—", fg="#555")
            return

        ag_temp = Agendamento(
            codigo="__preview__",
            animal=self.pet_selecionado or {"codigo": "?", "nome": "?"},
            servicos=servicos,
            data_hora_inicio=self._data_hora_inicio(),
        )
        AgendamentoCalculator.calcular(ag_temp, tempo_extra=self._tempo_extra())

        self.termino_label.config(text=ag_temp.data_hora_termino.strftime("%d/%m/%Y %H:%M"))

        duracao_str = f"{ag_temp.duracao_total} min"
        if self._tempo_extra():
            duracao_str += f"  (+{self._tempo_extra()} min extra)"
        self.duracao_label.config(text=duracao_str)

        self.valor_label.config(
            text=f"R$ {ag_temp.valor_total:.2f}" +
                 (" (+20% FDS)" if ag_temp.eh_fim_de_semana else "")
        )
        self.fds_label.config(
            text="Sim" if ag_temp.eh_fim_de_semana else "Não",
            fg="#c0392b" if ag_temp.eh_fim_de_semana else "#27ae60"
        )

    # ------------------------------------------------------------------ #
    #  Submit                                                              #
    # ------------------------------------------------------------------ #

    def _tutores_por_servico(self):
        """
        Retorna dict {codigo_servico: codigo_funcionario}
        apenas para os serviços marcados com funcionário escolhido.
        """
        resultado = {}
        for codigo, var in self.check_vars.items():
            if var.get():
                valor = self.tutor_vars[codigo].get()
                if valor and valor != "— Nenhum —":
                    cod_func = valor.split(" — ")[0].strip()
                    resultado[codigo] = cod_func
                else:
                    resultado[codigo] = None
        return resultado

    def submit(self):
        codigo = self.codigo_entry.get().strip()
        servicos = self._servicos_selecionados()

        if not codigo:
            messagebox.showerror("Erro", "Informe o código do agendamento.", parent=self.master)
            return
        if not self.pet_selecionado:
            messagebox.showerror("Erro", "Selecione um pet.", parent=self.master)
            return
        if not servicos:
            messagebox.showerror("Erro", "Selecione ao menos um serviço.", parent=self.master)
            return

        ag = Agendamento(
            codigo=codigo,
            animal=self.pet_selecionado,
            servicos=servicos,
            data_hora_inicio=self._data_hora_inicio(),
            status=self.status_var.get(),
            observacoes=self.obs_text.get("1.0", "end").strip(),
        )
        tempo_extra = self._tempo_extra()
        AgendamentoCalculator.calcular(ag, tempo_extra=tempo_extra)

        # Anexa tutores antes de validar (validator precisa deles)
        ag.tutores_por_servico = self._tutores_por_servico()

        agendamentos_salvos = Dados.load("agendamentos.json")

        valido, erro = VerificationAgendamento.validar(ag, agendamentos_salvos)
        if not valido:
            messagebox.showerror("Conflito de horário", erro, parent=self.master)
            return

        ag_dict = ag.to_dict()
        ag_dict["tutores_por_servico"] = ag.tutores_por_servico
        ag_dict["tempo_extra"] = tempo_extra

        agendamentos_salvos.append(ag_dict)
        Dados.save("agendamentos.json", agendamentos_salvos)

        messagebox.showinfo("Sucesso", "Agendamento cadastrado com sucesso!", parent=self.master)
        self.master.destroy()
        if self.parent_window:
            self.parent_window.deiconify()

    def voltar(self):
        if self.parent_window:
            self.parent_window.deiconify()
        self.master.destroy()