from datetime import date

class Servico:
    def __init__(self, codigo, nome, tipo, descricao, valor_base, duracao, requer_agendamento):
        self.codigo = codigo
        self.nome = nome
        self.tipo = tipo
        self.descricao = descricao
        self.valor_base = valor_base
        self.duracao = duracao  # em minutos
        self.requer_agendamento = requer_agendamento  # bool

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "tipo": self.tipo,
            "descricao": self.descricao,
            "valor_base": self.valor_base,
            "duracao": self.duracao,
            "requer_agendamento": self.requer_agendamento,
        }


class Consulta(Servico):
    def __init__(self, codigo, nome, descricao, valor_base, duracao,
                 veterinario, especialidade):
        super().__init__(codigo, nome, "consulta veterinária", descricao,
                         valor_base, duracao, requer_agendamento=True)
        self.veterinario = veterinario
        self.especialidade = especialidade

    def to_dict(self):
        d = super().to_dict()
        d.update({"veterinario": self.veterinario, "especialidade": self.especialidade})
        return d


class BanhoTosa(Servico):
    def __init__(self, codigo, nome, descricao, valor_base, duracao,
                 corte_unhas, perfume):
        super().__init__(codigo, nome, "banho e tosa", descricao,
                         valor_base, duracao, requer_agendamento=True)
        self.corte_unhas = corte_unhas  # bool
        self.perfume = perfume          # str com o nome do perfume, ou None

    def to_dict(self):
        d = super().to_dict()
        d.update({"corte_unhas": self.corte_unhas, "perfume": self.perfume})
        return d


class Vacinacao(Servico):
    def __init__(self, codigo, nome, descricao, valor_base, duracao,
                 lote, data_validade, laboratorio):
        super().__init__(codigo, nome, "vacinação", descricao,
                         valor_base, duracao, requer_agendamento=False)
        self.lote = lote
        self.data_validade = data_validade  # date
        self.laboratorio = laboratorio

    def to_dict(self):
        d = super().to_dict()
        d.update({
            "lote": self.lote,
            "data_validade": self.data_validade.isoformat(),
            "laboratorio": self.laboratorio
        })
        return d


class Hospedagem(Servico):
    def __init__(self, codigo, nome, descricao, valor_base, duracao,
                 valor_diaria, capacidade_acompanhamento):
        super().__init__(codigo, nome, "hospedagem", descricao,
                         valor_base, duracao, requer_agendamento=True)
        self.valor_diaria = valor_diaria
        self.capacidade_acompanhamento = capacidade_acompanhamento  # int, nº de animais

    def to_dict(self):
        d = super().to_dict()
        d.update({
            "valor_diaria": self.valor_diaria,
            "capacidade_acompanhamento": self.capacidade_acompanhamento
        })
        return 