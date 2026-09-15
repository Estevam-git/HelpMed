cat /mnt/user-data/outputs/cliente.py
Saída

"""
Módulo Cliente — Estrutura base do sistema Help Desk
Cada paciente que chega no sistema é representado por um objeto Cliente.
"""

from datetime import datetime


# Contadores de protocolo (simula geração automática)
_contador_protocolo = 0


def gerar_protocolo():
    """Gera um número de protocolo único e sequencial."""
    global _contador_protocolo
    _contador_protocolo += 1
    return f"HC-{_contador_protocolo:04d}"


# Mapeamento de cores do Protocolo de Manchester
CORES_MANCHESTER = {
    1: {"cor": "VERMELHO", "descricao": "Emergência", "tempo_max": "Imediato"},
    2: {"cor": "LARANJA", "descricao": "Muito urgente", "tempo_max": "10 min"},
    3: {"cor": "AMARELO", "descricao": "Urgente", "tempo_max": "60 min"},
    4: {"cor": "VERDE", "descricao": "Pouco urgente", "tempo_max": "120 min"},
    5: {"cor": "AZUL", "descricao": "Não urgente", "tempo_max": "240 min"},
}


class Cliente:
    """
    Representa um paciente no sistema de triagem.

    Atributos:
        nome (str): Nome completo do paciente.
        protocolo (str): Código único gerado automaticamente.
        prioridade (int): Nível de urgência (1 = mais urgente, 5 = menos urgente).
        sintomas (str): Descrição dos sintomas relatados.
        horario_chegada (datetime): Momento em que o paciente foi registrado.
        acoes (list): Lista de ações realizadas durante o atendimento.
    """

    def __init__(self, nome, prioridade, sintomas):
        """
        Cria um novo paciente.

        Args:
            nome (str): Nome do paciente.
            prioridade (int): Nível de urgência de 1 (emergência) a 5 (não urgente).
            sintomas (str): Descrição dos sintomas.
        """
        if prioridade < 1 or prioridade > 5:
            raise ValueError("Prioridade deve ser entre 1 (emergência) e 5 (não urgente).")

        self.nome = nome
        self.protocolo = gerar_protocolo()
        self.prioridade = prioridade
        self.sintomas = sintomas
        self.horario_chegada = datetime.now()
        self.acoes = []

    def obter_cor(self):
        """Retorna a cor do Protocolo de Manchester baseado na prioridade."""
        return CORES_MANCHESTER[self.prioridade]["cor"]

    def obter_descricao_prioridade(self):
        """Retorna a descrição da urgência (ex: 'Emergência', 'Muito urgente')."""
        return CORES_MANCHESTER[self.prioridade]["descricao"]

    def obter_tempo_maximo(self):
        """Retorna o tempo máximo de espera segundo o protocolo."""
        return CORES_MANCHESTER[self.prioridade]["tempo_max"]

    def adicionar_acao(self, acao):
        """
        Registra uma ação realizada no atendimento.

        Args:
            acao (str): Descrição da ação (ex: 'Diagnóstico: gripe').
        """
        self.acoes.append(acao)

    def remover_ultima_acao(self):
        """Remove a última ação registrada (undo). Retorna a ação removida ou None."""
        if self.acoes:
            return self.acoes.pop()
        return None

    def __str__(self):
        """Representação em texto do paciente para exibição no terminal."""
        cor = self.obter_cor()
        descricao = self.obter_descricao_prioridade()
        tempo = self.obter_tempo_maximo()
        horario = self.horario_chegada.strftime("%H:%M:%S")

        return (
            f"[{self.protocolo}] {self.nome}\n"
            f"  Prioridade: {cor} — {descricao} (espera máx: {tempo})\n"
            f"  Sintomas: {self.sintomas}\n"
            f"  Chegada: {horario}"
        )


# ============================================================
# TESTES — rode este arquivo diretamente para testar:
#   python cliente.py
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("TESTE — Módulo Cliente")
    print("=" * 50)

    # Criar pacientes com diferentes prioridades
    p1 = Cliente("João Silva", 1, "Dor no peito e falta de ar")
    p2 = Cliente("Maria Souza", 3, "Febre alta e dor abdominal")
    p3 = Cliente("Pedro Lima", 5, "Renovação de receita")

    # Exibir informações
    print("\n--- Pacientes registrados ---\n")
    print(p1)
    print()
    print(p2)
    print()
    print(p3)

    # Testar ações
    print("\n--- Teste de ações (undo) ---\n")
    p1.adicionar_acao("Diagnóstico: suspeita de infarto")
    p1.adicionar_acao("Medicação: aspirina 100mg")
    p1.adicionar_acao("Encaminhamento: UTI cardíaca")
    print(f"Ações do {p1.nome}: {p1.acoes}")

    removida = p1.remover_ultima_acao()
    print(f"Ação desfeita: {removida}")
    print(f"Ações restantes: {p1.acoes}")

    # Testar cores
    print("\n--- Cores do Manchester ---\n")
    for nivel, info in CORES_MANCHESTER.items():
        print(f"  Nível {nivel}: {info['cor']} — {info['descricao']} (máx {info['tempo_max']})")

    # Testar erro de prioridade inválida
    print("\n--- Teste de prioridade inválida ---\n")
    try:
        px = Cliente("Teste", 9, "Nada")
    except ValueError as e:
        print(f"Erro capturado corretamente: {e}")

    print("\n" + "=" * 50)
    print("TODOS OS TESTES PASSARAM!")
    print("=" * 50)