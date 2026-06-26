from datetime import timedelta


class AgendamentoCalculator:
    ACRESCIMO_FDS = 1.20

    @staticmethod
    def calcular(agendamento, tempo_extra=0):
        AgendamentoCalculator._calcular_duracao(agendamento, tempo_extra)
        AgendamentoCalculator._calcular_termino(agendamento)
        AgendamentoCalculator._calcular_valor(agendamento, tempo_extra)
        return agendamento

    @staticmethod
    def _calcular_duracao(agendamento, tempo_extra=0):
        base = sum(
            s.get("duracao", 0) if isinstance(s, dict) else s.duracao
            for s in agendamento.servicos
        )
        agendamento.duracao_total = base + max(0, tempo_extra)

    @staticmethod
    def _calcular_termino(agendamento):
        agendamento.data_hora_termino = (
            agendamento.data_hora_inicio + timedelta(minutes=agendamento.duracao_total)
        )

    @staticmethod
    def _calcular_valor(agendamento, tempo_extra=0):
        agendamento.eh_fim_de_semana = agendamento.data_hora_inicio.weekday() >= 5

        duracao_base = sum(
            s.get("duracao", 0) if isinstance(s, dict) else s.duracao
            for s in agendamento.servicos
        )
        valor_servicos = sum(
            s.get("valor_base", 0) if isinstance(s, dict) else s.valor_base
            for s in agendamento.servicos
        )

        tempo_extra = max(0, tempo_extra)

        # Valor/minuto médio dos serviços escolhidos, usado para precificar
        # o tempo extra proporcionalmente. Se duracao_base for 0 (não deveria
        # ocorrer com serviços válidos), não há base de rateio, então o
        # tempo extra não é cobrado para evitar ZeroDivisionError.
        if duracao_base > 0:
            valor_por_minuto = valor_servicos / duracao_base
            valor_extra = valor_por_minuto * tempo_extra
        else:
            valor_extra = 0

        agendamento.valor_extra = round(valor_extra, 2)

        total = valor_servicos + valor_extra
        if agendamento.eh_fim_de_semana:
            total *= AgendamentoCalculator.ACRESCIMO_FDS

        agendamento.valor_total = round(total, 2)