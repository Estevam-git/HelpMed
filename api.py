"""
API — Ponte entre a interface (JavaScript) e o sistema (Python).
O PyWebView expõe essa classe pro JS chamar os métodos diretamente.
"""

from sistema import Sistema


class Api:
    """Classe exposta para o JavaScript via PyWebView."""

    def __init__(self):
        self.sistema = Sistema()

    # =====================
    # TRIAGEM E FILA
    # =====================

    def registrar_paciente(self, nome, sintomas, respostas):
        """Registra paciente e retorna seus dados."""
        paciente = self.sistema.registrar_paciente(nome, sintomas, respostas)
        return {
            "protocolo": paciente.protocolo,
            "nome": paciente.nome,
            "cor": paciente.obter_cor(),
            "descricao": paciente.obter_descricao_prioridade(),
            "tempo_max": paciente.obter_tempo_maximo(),
            "sintomas": paciente.sintomas,
        }

    def ver_fila(self):
        """Retorna a fila de espera."""
        return self.sistema.ver_fila()

    def total_fila(self):
        """Retorna o total de pacientes na fila."""
        return self.sistema.total_fila()

    # =====================
    # ATENDIMENTO
    # =====================

    def chamar_proximo(self):
        """Chama o próximo paciente."""
        return self.sistema.chamar_proximo()

    def paciente_em_atendimento(self):
        """Retorna dados do paciente em atendimento."""
        return self.sistema.paciente_em_atendimento()

    def registrar_acao(self, acao):
        """Registra uma ação no atendimento."""
        return self.sistema.registrar_acao(acao)

    def desfazer_acao(self):
        """Desfaz a última ação."""
        return self.sistema.desfazer_acao()

    def ver_acoes(self):
        """Retorna as ações do atendimento atual."""
        return self.sistema.ver_acoes()

    def finalizar_atendimento(self):
        """Finaliza o atendimento e move pro histórico."""
        return self.sistema.finalizar_atendimento()

    # =====================
    # HISTÓRICO
    # =====================

    def buscar_historico_protocolo(self, protocolo):
        """Busca no histórico por protocolo."""
        return self.sistema.buscar_historico_protocolo(protocolo)

    def buscar_historico_nome(self, nome):
        """Busca no histórico por nome."""
        return self.sistema.buscar_historico_nome(nome)

    def ver_historico(self):
        """Retorna todo o histórico."""
        return self.sistema.ver_historico()

    def total_historico(self):
        """Total de pacientes no histórico."""
        return self.sistema.total_historico()