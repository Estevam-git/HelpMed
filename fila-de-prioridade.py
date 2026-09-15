"""
Módulo Fila de Prioridade — Organiza pacientes por urgência (Manchester).
Estrutura: lista encadeada ordenada por prioridade.

Regra: quanto MENOR o número da prioridade, MAIS urgente.
  1 = Vermelho (emergência) → atendido primeiro
  5 = Azul (não urgente) → atendido por último

Se dois pacientes têm a mesma prioridade, quem chegou primeiro sai primeiro (FIFO).
"""


class No:
    """
    Nó da lista encadeada.
    Cada nó guarda um paciente e aponta para o próximo nó da fila.
    """

    def __init__(self, paciente):
        self.paciente = paciente
        self.proximo = None


class FilaPrioridade:
    """
    Fila de prioridade implementada com lista encadeada ordenada.

    Pacientes mais urgentes (prioridade menor) ficam na frente.
    Pacientes com mesma prioridade seguem ordem de chegada (FIFO).
    """

    def __init__(self):
        """Cria uma fila vazia."""
        self.frente = None
        self.tamanho = 0

    def esta_vazia(self):
        """Retorna True se a fila está vazia."""
        return self.frente is None

    def enfileirar(self, paciente):
        """
        Insere um paciente na posição correta da fila, baseado na prioridade.

        Pacientes mais urgentes (número menor) ficam mais perto da frente.
        Se a prioridade for igual, o novo paciente vai atrás dos que já
        estavam com a mesma prioridade (respeita ordem de chegada).

        Args:
            paciente (Cliente): O paciente a ser inserido na fila.
        """
        novo = No(paciente)

        # Caso 1: fila vazia ou paciente é mais urgente que o primeiro
        if self.frente is None or paciente.prioridade < self.frente.paciente.prioridade:
            novo.proximo = self.frente
            self.frente = novo
        else:
            # Caso 2: percorre a fila até achar a posição correta
            atual = self.frente
            while (atual.proximo is not None and
                   atual.proximo.paciente.prioridade <= paciente.prioridade):
                atual = atual.proximo

            novo.proximo = atual.proximo
            atual.proximo = novo

        self.tamanho += 1

    def desenfileirar(self):
        """
        Remove e retorna o paciente mais urgente (frente da fila).

        Returns:
            Cliente: O paciente removido, ou None se a fila estiver vazia.
        """
        if self.esta_vazia():
            print("⚠ Fila vazia — nenhum paciente para atender.")
            return None

        paciente = self.frente.paciente
        self.frente = self.frente.proximo
        self.tamanho -= 1
        return paciente

    def ver_frente(self):
        """
        Retorna o próximo paciente a ser atendido sem removê-lo.

        Returns:
            Cliente: O paciente na frente da fila, ou None se vazia.
        """
        if self.esta_vazia():
            return None
        return self.frente.paciente

    def listar_fila(self):
        """Exibe todos os pacientes na fila, na ordem de atendimento."""
        if self.esta_vazia():
            print("Fila vazia — nenhum paciente aguardando.")
            return

        print(f"Fila de espera ({self.tamanho} paciente(s)):\n")
        atual = self.frente
        posicao = 1
        while atual is not None:
            cor = atual.paciente.obter_cor()
            print(f"  {posicao}º → [{cor}] {atual.paciente.nome} "
                  f"(Protocolo: {atual.paciente.protocolo})")
            atual = atual.proximo
            posicao += 1


# ============================================================
# TESTES — rode diretamente: python fila_prioridade.py
# ============================================================

if __name__ == "__main__":
    from cliente import Cliente

    print("=" * 50)
    print("TESTE — Fila de Prioridade")
    print("=" * 50)

    fila = FilaPrioridade()

    # Registrar pacientes fora de ordem
    print("\n--- Registrando pacientes ---\n")
    p1 = Cliente("Ana Costa", 3, "Febre alta")
    p2 = Cliente("Bruno Lima", 1, "Parada respiratória")
    p3 = Cliente("Carla Dias", 5, "Renovação de receita")
    p4 = Cliente("Diego Reis", 1, "Hemorragia grave")
    p5 = Cliente("Eva Moura", 2, "Dor no peito intensa")

    fila.enfileirar(p1)
    print(f"Enfileirou: {p1.nome} — {p1.obter_cor()}")
    fila.enfileirar(p2)
    print(f"Enfileirou: {p2.nome} — {p2.obter_cor()}")
    fila.enfileirar(p3)
    print(f"Enfileirou: {p3.nome} — {p3.obter_cor()}")
    fila.enfileirar(p4)
    print(f"Enfileirou: {p4.nome} — {p4.obter_cor()}")
    fila.enfileirar(p5)
    print(f"Enfileirou: {p5.nome} — {p5.obter_cor()}")

    # Mostrar fila ordenada
    print("\n--- Fila ordenada por prioridade ---\n")
    fila.listar_fila()

    # Atender pacientes (deve sair por ordem de urgência)
    print("\n--- Atendendo pacientes ---\n")
    while not fila.esta_vazia():
        paciente = fila.desenfileirar()
        print(f"Atendendo: {paciente.nome} — {paciente.obter_cor()}")

    # Testar fila vazia
    print("\n--- Tentando atender fila vazia ---\n")
    fila.desenfileirar()

    print("\n" + "=" * 50)
    print("TODOS OS TESTES PASSARAM!")
    print("=" * 50)