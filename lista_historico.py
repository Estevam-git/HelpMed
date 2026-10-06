"""
Módulo Lista de Histórico — Armazena pacientes já atendidos.
Estrutura: lista encadeada simples.

Permite inserir, buscar por nome ou protocolo, e listar todos os atendimentos.
"""


class No:
    """Nó da lista encadeada. Guarda um paciente e aponta para o próximo."""

    def __init__(self, paciente):
        self.paciente = paciente
        self.proximo = None


class ListaHistorico:
    """
    Lista encadeada simples para armazenar o histórico de atendimentos.

    Novos pacientes são inseridos no final da lista (ordem cronológica).
    """

    def __init__(self):
        """Cria uma lista vazia."""
        self.inicio = None
        self.tamanho = 0

    def esta_vazia(self):
        """Retorna True se a lista está vazia."""
        return self.inicio is None

    def inserir(self, paciente):
        """
        Insere um paciente no final da lista (fim do histórico).

        Args:
            paciente (Cliente): Paciente que acabou de ser atendido.
        """
        novo = No(paciente)

        if self.inicio is None:
            self.inicio = novo
        else:
            atual = self.inicio
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo

        self.tamanho += 1

    def buscar_por_protocolo(self, protocolo):
        """
        Busca um paciente pelo número de protocolo.

        Args:
            protocolo (str): Código do protocolo (ex: 'HC-0001').

        Returns:
            Cliente: O paciente encontrado, ou None se não existir.
        """
        atual = self.inicio
        while atual is not None:
            if atual.paciente.protocolo == protocolo:
                return atual.paciente
            atual = atual.proximo
        return None

    def buscar_por_nome(self, nome):
        """
        Busca pacientes pelo nome (busca parcial, ignora maiúsculas).

        Args:
            nome (str): Nome ou parte do nome do paciente.

        Returns:
            list: Lista de pacientes que contêm o nome buscado.
        """
        encontrados = []
        atual = self.inicio
        while atual is not None:
            if nome.lower() in atual.paciente.nome.lower():
                encontrados.append(atual.paciente)
            atual = atual.proximo
        return encontrados

    def remover_por_protocolo(self, protocolo):
        """
        Remove um paciente do histórico pelo protocolo.

        Args:
            protocolo (str): Código do protocolo.

        Returns:
            Cliente: O paciente removido, ou None se não encontrado.
        """
        if self.esta_vazia():
            return None

        # Caso especial: remover o primeiro
        if self.inicio.paciente.protocolo == protocolo:
            paciente = self.inicio.paciente
            self.inicio = self.inicio.proximo
            self.tamanho -= 1
            return paciente

        # Percorrer buscando o anterior ao que será removido
        atual = self.inicio
        while atual.proximo is not None:
            if atual.proximo.paciente.protocolo == protocolo:
                paciente = atual.proximo.paciente
                atual.proximo = atual.proximo.proximo
                self.tamanho -= 1
                return paciente
            atual = atual.proximo

        return None

    def listar_todos(self):
        """Exibe todos os pacientes do histórico em ordem cronológica."""
        if self.esta_vazia():
            print("Histórico vazio — nenhum atendimento registrado.")
            return

        print(f"Histórico de atendimentos ({self.tamanho} registro(s)):\n")
        atual = self.inicio
        posicao = 1
        while atual is not None:
            p = atual.paciente
            cor = p.obter_cor()
            horario = p.horario_chegada.strftime("%H:%M:%S")
            print(f"  {posicao}. [{p.protocolo}] {p.nome} — {cor} — {horario}")
            if p.acoes:
                for acao in p.acoes:
                    print(f"      • {acao}")
            atual = atual.proximo
            posicao += 1

    def contar(self):
        """Retorna o total de pacientes no histórico."""
        return self.tamanho


# ============================================================
# TESTES — rode diretamente: python lista_historico.py
# ============================================================

if __name__ == "__main__":
    from cliente import Cliente

    print("=" * 50)
    print("TESTE — Lista de Histórico")
    print("=" * 50)

    historico = ListaHistorico()

    # Criar pacientes simulando atendimentos finalizados
    print("\n--- Inserindo pacientes no histórico ---\n")
    p1 = Cliente("Ana Costa", 1, "Dor no peito")
    p1.adicionar_acao("Diagnóstico: angina")
    p1.adicionar_acao("Medicação: nitrato sublingual")

    p2 = Cliente("Bruno Lima", 3, "Febre e tosse")
    p2.adicionar_acao("Diagnóstico: gripe")
    p2.adicionar_acao("Medicação: dipirona")

    p3 = Cliente("Carla Dias", 5, "Renovação de receita")
    p3.adicionar_acao("Receita renovada: omeprazol")

    p4 = Cliente("Ana Beatriz", 2, "Queda com fratura")
    p4.adicionar_acao("Raio-X realizado")
    p4.adicionar_acao("Diagnóstico: fratura no punho")

    for p in [p1, p2, p3, p4]:
        historico.inserir(p)
        print(f"  Inserido: {p.nome} ({p.protocolo})")

    # Listar todos
    print("\n--- Histórico completo ---\n")
    historico.listar_todos()

    # Buscar por protocolo
    print("\n--- Busca por protocolo ---\n")
    resultado = historico.buscar_por_protocolo("HC-0002")
    if resultado:
        print(f"  Encontrado: {resultado.nome}")
    else:
        print("  Não encontrado")

    # Buscar por nome (parcial)
    print("\n--- Busca por nome 'Ana' ---\n")
    resultados = historico.buscar_por_nome("Ana")
    for r in resultados:
        print(f"  Encontrado: {r.nome} ({r.protocolo})")

    # Remover por protocolo
    print("\n--- Removendo HC-0003 ---\n")
    removido = historico.remover_por_protocolo("HC-0003")
    if removido:
        print(f"  Removido: {removido.nome}")

    # Listar após remoção
    print(f"\n--- Histórico após remoção ({historico.contar()} registros) ---\n")
    historico.listar_todos()

    # Buscar inexistente
    print("\n--- Busca por protocolo inexistente ---\n")
    resultado = historico.buscar_por_protocolo("HC-9999")
    print(f"  Resultado: {resultado}")

    print("\n" + "=" * 50)
    print("TODOS OS TESTES PASSARAM!")
    print("=" * 50)