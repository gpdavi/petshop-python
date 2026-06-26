from datetime import datetime


class Agendamento:
    STATUS_VALIDOS = {"agendado", "em andamento", "concluído", "cancelado", "não compareceu"}

    def __init__(self, codigo, animal, servicos, data_hora_inicio,
                 status="agendado", observacoes=""):
        self.codigo = codigo
        self.animal = animal      
        self.servicos = servicos  
        
        if isinstance(data_hora_inicio, str):
            data_hora_inicio = datetime.fromisoformat(data_hora_inicio)
        self.data_hora_inicio = data_hora_inicio

        if status not in self.STATUS_VALIDOS:
            raise ValueError(f"Status inválido: '{status}'. Use: {self.STATUS_VALIDOS}")
        self.status = status
        self.observacoes = observacoes

        # preenchidos pelo AgendamentoCalculator antes de salvar
        self.duracao_total = 0
        self.data_hora_termino = None
        self.valor_total = 0.0
        self.eh_fim_de_semana = False

    def alterar_status(self, novo_status):
        if novo_status not in self.STATUS_VALIDOS:
            raise ValueError(f"Status inválido: '{novo_status}'.")
        self.status = novo_status

    def to_dict(self):
        animal_ref = (
            self.animal.get("codigo") if isinstance(self.animal, dict)
            else self.animal.codigo
        )
        servicos_refs = [
            (s.get("codigo") if isinstance(s, dict) else s.codigo)
            for s in self.servicos
        ]
        return {
            "codigo":            self.codigo,
            "animal":            animal_ref,
            "servicos":          servicos_refs,
            "data_hora_inicio":  self.data_hora_inicio.isoformat(),
            "data_hora_termino": self.data_hora_termino.isoformat() if self.data_hora_termino else None,
            "duracao_total":     self.duracao_total,
            "valor_total":       self.valor_total,
            "eh_fim_de_semana":  self.eh_fim_de_semana,
            "status":            self.status,
            "observacoes":       self.observacoes,
        }

    @classmethod
    def from_dict(cls, data, animais, servicos):
        animal = next((a for a in animais if a["codigo"] == data["animal"]), None)
        svcs = [s for s in servicos if s["codigo"] in data["servicos"]]
        obj = cls(
            codigo=data["codigo"],
            animal=animal,
            servicos=svcs,
            data_hora_inicio=data["data_hora_inicio"],
            status=data.get("status", "agendado"),
            observacoes=data.get("observacoes", ""),
        )
        obj.duracao_total = data.get("duracao_total", 0)
        obj.data_hora_termino = (
            datetime.fromisoformat(data["data_hora_termino"])
            if data.get("data_hora_termino") else None
        )
        obj.valor_total = data.get("valor_total", 0.0)
        obj.eh_fim_de_semana = data.get("eh_fim_de_semana", False)
        return obj

    def __repr__(self):
        animal_nome = (
            self.animal.get("nome") if isinstance(self.animal, dict)
            else self.animal.nome
        )
        return (
            f"<Agendamento {self.codigo} | {animal_nome} | "
            f"{self.data_hora_inicio:%d/%m/%Y %H:%M} | "
            f"R$ {self.valor_total:.2f} | {self.status}>"
        )