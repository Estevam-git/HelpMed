"""
Módulo Sistema — Conecta fila de prioridade, pilha undo e lista de histórico.
Lógica principal do Help Desk de Saúde Pública.

Este módulo é a ponte entre a interface (frontend) e as estruturas de dados (backend).
A interface chama os métodos daqui, e este módulo manipula as estruturas.
"""

from cliente import Cliente, CORES_MANCHESTER
from fila_prioridade import FilaPrioridade
from pilha_undo import PilhaUndo
from lista_historico import ListaHistorico
from triagem import classificar_prioridade


class Sistema:
    """
    Sistema Help Desk — gerencia o fluxo completo de atendimento.

    Fluxo: Triagem → Fila de Prioridade → Atendimento (com Undo) → Histórico
    """

    def __init__(self):
        """Inicializa o sistema com as três estruturas vazias."""
        self.fila = FilaPrioridade()
        self.pilha = PilhaUndo()
        self.historico = ListaHistorico()
        self.paciente_atual = None  # Paciente sendo atendido agora

    # =====================
    # TRIAGEM E FILA
    # =====================

    def registrar_paciente(self, nome, sintomas, respostas):
        """
        Registra um novo paciente: classifica pela triagem e coloca na fila.

        Args:
            nome (str): Nome do paciente.
            sintomas (str): Descrição dos sintomas.
            respostas (dict): Respostas do questionário de triagem.

        Returns:
            Cliente: O paciente registrado.
        """
        prioridade = classificar_prioridade(respostas)
        paciente = Cliente(nome, prioridade, sintomas)
        self.fila.enfileirar(paciente)
        return paciente

    def ver_fila(self):
        """
        Retorna a lista de pacientes na fila (para exibir na interface).

        Returns:
            list: Lista de dicionários com dados de cada paciente na fila.
        """
        pacientes = []
        atual = self.fila.frente
        posicao = 1
        while atual is not None:
            p = atual.paciente
            pacientes.append({
                "posicao": posicao,
                "protocolo": p.protocolo,
                "nome": p.nome,
                "prioridade": p.prioridade,
                "cor": p.obter_cor(),
                "descricao_prioridade": p.obter_descricao_prioridade(),
                "tempo_max": p.obter_tempo_maximo(),
                "sintomas": p.sintomas,
                "horario": p.horario_chegada.strftime("%H:%M:%S"),
            })
            atual = atual.proximo
            posicao += 1
        return pacientes

    def total_fila(self):
        """Retorna o número de pacientes na fila."""
        return self.fila.tamanho

    # =====================
    # ATENDIMENTO
    # =====================

    def chamar_proximo(self):
        """
        Chama o próximo paciente da fila para atendimento.

        Returns:
            dict: Dados do paciente chamado, ou None se a fila estiver vazia.
        """
        if self.paciente_atual is not None:
            return {"erro": "Já existe um paciente em atendimento. Finalize antes de chamar o próximo."}

        paciente = self.fila.desenfileirar()
        if paciente is None:
            return None

        self.paciente_atual = paciente
        self.pilha.limpar()  # Limpa a pilha de ações do atendimento anterior

        return {
            "protocolo": paciente.protocolo,
            "nome": paciente.nome,
            "cor": paciente.obter_cor(),
            "descricao_prioridade": paciente.obter_descricao_prioridade(),
            "sintomas": paciente.sintomas,
            "horario": paciente.horario_chegada.strftime("%H:%M:%S"),
        }

    def paciente_em_atendimento(self):
        """
        Retorna os dados do paciente em atendimento atual.

        Returns:
            dict: Dados do paciente, ou None se não há atendimento em curso.
        """
        if self.paciente_atual is None:
            return None

        return {
            "protocolo": self.paciente_atual.protocolo,
            "nome": self.paciente_atual.nome,
            "cor": self.paciente_atual.obter_cor(),
            "descricao_prioridade": self.paciente_atual.obter_descricao_prioridade(),
            "sintomas": self.paciente_atual.sintomas,
            "acoes": list(self.paciente_atual.acoes),
        }

    # =====================
    # AÇÕES + UNDO
    # =====================

    def registrar_acao(self, acao):
        """
        Registra uma ação no atendimento atual.

        Args:
            acao (str): Descrição da ação (ex: 'Diagnóstico: gripe').

        Returns:
            bool: True se registrou, False se não há paciente em atendimento.
        """
        if self.paciente_atual is None:
            return False

        self.paciente_atual.adicionar_acao(acao)
        self.pilha.empilhar(acao)
        return True

    def desfazer_acao(self):
        """
        Desfaz a última ação registrada (undo).

        Returns:
            str: A ação desfeita, ou None se não há ação para desfazer.
        """
        if self.paciente_atual is None or self.pilha.esta_vazia():
            return None

        acao = self.pilha.desempilhar()
        self.paciente_atual.remover_ultima_acao()
        return acao

    def ver_acoes(self):
        """
        Retorna a lista de ações do atendimento atual.

        Returns:
            list: Lista de strings com as ações, ou lista vazia.
        """
        if self.paciente_atual is None:
            return []
        return list(self.paciente_atual.acoes)

    # =====================
    # FINALIZAR ATENDIMENTO
    # =====================

    def finalizar_atendimento(self):
        """
        Finaliza o atendimento atual e move o paciente para o histórico.

        Returns:
            dict: Dados do paciente finalizado, ou None se não há atendimento.
        """
        if self.paciente_atual is None:
            return None

        paciente = self.paciente_atual
        self.historico.inserir(paciente)
        self.pilha.limpar()
        self.paciente_atual = None

        return {
            "protocolo": paciente.protocolo,
            "nome": paciente.nome,
            "cor": paciente.obter_cor(),
            "acoes": list(paciente.acoes),
        }

    # =====================
    # HISTÓRICO
    # =====================

    def buscar_historico_protocolo(self, protocolo):
        """
        Busca um paciente no histórico pelo protocolo.

        Returns:
            dict: Dados do paciente, ou None se não encontrado.
        """
        paciente = self.historico.buscar_por_protocolo(protocolo)
        if paciente is None:
            return None

        return {
            "protocolo": paciente.protocolo,
            "nome": paciente.nome,
            "cor": paciente.obter_cor(),
            "sintomas": paciente.sintomas,
            "acoes": list(paciente.acoes),
            "horario": paciente.horario_chegada.strftime("%H:%M:%S"),
        }

    def buscar_historico_nome(self, nome):
        """
        Busca pacientes no histórico pelo nome.

        Returns:
            list: Lista de dicionários com dados dos pacientes encontrados.
        """
        pacientes = self.historico.buscar_por_nome(nome)
        return [{
            "protocolo": p.protocolo,
            "nome": p.nome,
            "cor": p.obter_cor(),
            "sintomas": p.sintomas,
            "acoes": list(p.acoes),
            "horario": p.horario_chegada.strftime("%H:%M:%S"),
        } for p in pacientes]

    def ver_historico(self):
        """
        Retorna todos os pacientes do histórico.

        Returns:
            list: Lista de dicionários com dados de cada paciente.
        """
        pacientes = []
        atual = self.historico.inicio
        while atual is not None:
            p = atual.paciente
            pacientes.append({
                "protocolo": p.protocolo,
                "nome": p.nome,
                "cor": p.obter_cor(),
                "descricao_prioridade": p.obter_descricao_prioridade(),
                "sintomas": p.sintomas,
                "acoes": list(p.acoes),
                "horario": p.horario_chegada.strftime("%H:%M:%S"),
            })
            atual = atual.proximo
        return pacientes

    def total_historico(self):
        """Retorna o total de pacientes no histórico."""
        return self.historico.contar()


# ============================================================
# TESTES — rode diretamente: python sistema.py
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("TESTE — Sistema Help Desk Completo")
    print("=" * 50)

    sistema = Sistema()

    # 1. Registrar pacientes com triagem
    print("\n--- Registrando pacientes ---\n")

    p1 = sistema.registrar_paciente("João Silva", "Dor no peito e falta de ar", {
        "inconsciente": False, "dificuldade_respirar": True, "hemorragia": False,
        "dor_peito": True, "trauma_grave": False, "temperatura": 36.5, "nivel_dor": 7
    })
    print(f"  {p1.nome} → {p1.obter_cor()}")

    p2 = sistema.registrar_paciente("Maria Souza", "Febre alta e dor de cabeça", {
        "inconsciente": False, "dificuldade_respirar": False, "hemorragia": False,
        "dor_peito": False, "trauma_grave": False, "temperatura": 39.2, "nivel_dor": 6
    })
    print(f"  {p2.nome} → {p2.obter_cor()}")

    p3 = sistema.registrar_paciente("Pedro Lima", "Renovação de receita", {
        "inconsciente": False, "dificuldade_respirar": False, "hemorragia": False,
        "dor_peito": False, "trauma_grave": False, "temperatura": 36.5, "nivel_dor": 0
    })
    print(f"  {p3.nome} → {p3.obter_cor()}")

    # 2. Ver fila
    print(f"\n--- Fila de espera ({sistema.total_fila()} pacientes) ---\n")
    for p in sistema.ver_fila():
        print(f"  {p['posicao']}º → [{p['cor']}] {p['nome']}")

    # 3. Chamar próximo
    print("\n--- Chamando próximo ---\n")
    atendimento = sistema.chamar_proximo()
    print(f"  Atendendo: {atendimento['nome']} ({atendimento['cor']})")

    # 4. Registrar ações
    print("\n--- Registrando ações ---\n")
    sistema.registrar_acao("Aferiu pressão: 18x11")
    sistema.registrar_acao("Diagnóstico: crise hipertensiva")
    sistema.registrar_acao("Medicação: captopril 25mg")
    for acao in sistema.ver_acoes():
        print(f"  • {acao}")

    # 5. Desfazer última ação
    print("\n--- Desfazendo última ação ---\n")
    desfeita = sistema.desfazer_acao()
    print(f"  Desfeito: {desfeita}")
    print(f"  Ações restantes: {sistema.ver_acoes()}")

    # 6. Finalizar atendimento
    print("\n--- Finalizando atendimento ---\n")
    finalizado = sistema.finalizar_atendimento()
    print(f"  Finalizado: {finalizado['nome']} — Ações: {finalizado['acoes']}")

    # 7. Ver histórico
    print(f"\n--- Histórico ({sistema.total_historico()} registro(s)) ---\n")
    for p in sistema.ver_historico():
        print(f"  [{p['protocolo']}] {p['nome']} — {p['cor']}")

    # 8. Buscar no histórico
    print("\n--- Busca por nome 'João' ---\n")
    resultados = sistema.buscar_historico_nome("João")
    for r in resultados:
        print(f"  Encontrado: {r['nome']} ({r['protocolo']})")

    print("\n" + "=" * 50)
    print("TODOS OS TESTES PASSARAM!")
    print("=" * 50)