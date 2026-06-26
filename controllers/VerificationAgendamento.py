from datetime import datetime


class VerificationAgendamento:

    @staticmethod
    def validar(agendamento, agendamentos_salvos, tempo_extra=0):
        """
        Valida se o agendamento pode ser salvo sem conflitos de horário.
        Retorna (True, None) se válido, ou (False, mensagem_de_erro) se inválido.
        """
        inicio = agendamento.data_hora_inicio
        termino = agendamento.data_hora_termino

        codigo_animal = VerificationAgendamento._codigo(agendamento.animal)
        tutores_novos = getattr(agendamento, "tutores_por_servico", {})

        for ag in agendamentos_salvos:
            # Ignora o próprio agendamento (útil para edições futuras)
            if ag.get("codigo") == agendamento.codigo:
                continue

            # Ignora cancelados e não compareceu — não ocupam horário
            if ag.get("status") in {"cancelado", "não compareceu"}:
                continue

            ag_inicio = VerificationAgendamento._parse_dt(ag.get("data_hora_inicio"))
            ag_termino = VerificationAgendamento._parse_dt(ag.get("data_hora_termino"))

            if not ag_inicio or not ag_termino:
                continue

            if not VerificationAgendamento._sobrepostos(inicio, termino, ag_inicio, ag_termino):
                continue