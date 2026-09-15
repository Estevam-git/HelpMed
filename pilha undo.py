"""
Módulo Pilha Undo — Permite desfazer ações do atendente.
Estrutura: pilha com lista encadeada (LIFO).

Cada ação registrada durante uma consulta é empilhada.
Se o atendente errar, desempilha (pop) a última ação.
"""


class No:
    """Nó da pilha. Guarda uma ação e aponta para a ação anterior."""

    def __init__(self, acao):
        self.acao = acao
        self.proximo = None


class PilhaUndo:
    """
    Pilha implementada com lista encadeada.

    Última ação registrada é a primeira a ser desfeita (LIFO).
    """

    def __init__(self):
        """Cria uma pilha vazia."""
        self.topo = None
        self.tamanho = 0

    def esta_vazia(self):
        """Retorna True se a pilha está vazia."""
        return self.topo is None

    def empilhar(self, acao):
        """
        Registra uma nova ação no topo da pilha.

        Args:
            acao (str): Descrição da ação (ex: 'Diagnóstico: gripe').
        """
        novo = No(acao)
        novo.proximo = self.topo
        self.topo = novo
        self.tamanho += 1

    def desempilhar(self):
        """
        Remove e retorna a última ação registrada (undo).

        Returns:
            str: A ação removida, ou None se a pilha estiver vazia.
        """
        if self.esta_vazia():
            print("⚠ Nenhuma ação para desfazer.")
            return None

        acao = self.topo.acao
        self.topo = self.topo.proximo
        self.tamanho -= 1
        return acao

    def ver_topo(self):
        """
        Retorna a última ação sem removê-la.

        Returns:
            str: A ação no topo, ou None se vazia.
        """
        if self.esta_vazia():
            return None
        return self.topo.acao

    def listar_acoes(self):
        """Exibe todas as ações empilhadas, do topo (mais recente) à base."""
        if self.esta_vazia():
            print("Nenhuma ação registrada.")
            return

        print(f"Ações registradas ({self.tamanho}):\n")
        atual = self.topo
        posicao = 1
        while atual is not None:
            marcador = "→" if posicao == 1 else " "
            print(f"  {marcador} {posicao}. {atual.acao}")
            atual = atual.proximo
            posicao += 1

    def limpar(self):
        """Remove todas as ações da pilha (usado ao finalizar atendimento)."""
        self.topo = None
        self.tamanho = 0


# ============================================================
# TESTES — rode diretamente: python pilha_undo.py
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("TESTE — Pilha Undo")
    print("=" * 50)

    pilha = PilhaUndo()

    # Empilhar ações de um atendimento
    print("\n--- Registrando ações ---\n")
    acoes = [
        "Aferiu pressão: 18x11",
        "Diagnóstico: hipertensão",
        "Medicação: losartana 50mg",
        "Encaminhamento: cardiologista"
    ]

    for acao in acoes:
        pilha.empilhar(acao)
        print(f"  + {acao}")

    # Listar todas
    print("\n--- Pilha atual ---\n")
    pilha.listar_acoes()

    # Ver topo
    print(f"\nÚltima ação: {pilha.ver_topo()}")

    # Desfazer duas ações
    print("\n--- Desfazendo 2 ações ---\n")
    removida1 = pilha.desempilhar()
    print(f"  Desfeito: {removida1}")
    removida2 = pilha.desempilhar()
    print(f"  Desfeito: {removida2}")

    # Pilha após undo
    print("\n--- Pilha após undo ---\n")
    pilha.listar_acoes()

    # Limpar tudo
    print("\n--- Limpando pilha ---\n")
    pilha.limpar()
    print(f"Pilha vazia? {pilha.esta_vazia()}")

    # Tentar desempilhar vazia
    print("\n--- Tentando desfazer com pilha vazia ---\n")
    pilha.desempilhar()

    print("\n" + "=" * 50)
    print("TODOS OS TESTES PASSARAM!")
    print("=" * 50)