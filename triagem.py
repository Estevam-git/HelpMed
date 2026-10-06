"""
Módulo Triagem — Questionário objetivo que classifica o paciente
automaticamente pelo Protocolo de Manchester.

As perguntas são objetivas (sim/não e escalas numéricas).
O sistema classifica a cor baseado nas respostas, sem achismo.
"""

from cliente import Cliente


# Perguntas do questionário de triagem
PERGUNTAS = [
    {"texto": "O paciente está inconsciente?", "tipo": "sim_nao", "peso": 1},
    {"texto": "O paciente tem dificuldade severa para respirar?", "tipo": "sim_nao", "peso": 1},
    {"texto": "Há hemorragia intensa ou sangramento que não para?", "tipo": "sim_nao", "peso": 1},
    {"texto": "O paciente tem dor no peito?", "tipo": "sim_nao", "peso": 2},
    {"texto": "Há suspeita de fratura exposta ou trauma grave?", "tipo": "sim_nao", "peso": 2},
    {"texto": "O paciente tem febre? Se sim, qual a temperatura?", "tipo": "temperatura", "peso": 3},
    {"texto": "Qual o nível de dor do paciente? (0 a 10)", "tipo": "escala_dor", "peso": 3},
]


def classificar_prioridade(respostas):
    """
    Classifica a prioridade do paciente baseado nas respostas da triagem.

    Args:
        respostas (dict): Dicionário com as respostas do questionário.
            Chaves esperadas:
                - "inconsciente" (bool)
                - "dificuldade_respirar" (bool)
                - "hemorragia" (bool)
                - "dor_peito" (bool)
                - "trauma_grave" (bool)
                - "temperatura" (float)
                - "nivel_dor" (int: 0-10)

    Returns:
        int: Nível de prioridade de 1 (emergência) a 5 (não urgente).
    """

    # VERMELHO (1) — Emergência: risco imediato de vida
    if (respostas.get("inconsciente") or
        respostas.get("dificuldade_respirar") or
        respostas.get("hemorragia")):
        return 1

    # LARANJA (2) — Muito urgente: situação grave
    if (respostas.get("dor_peito") or
        respostas.get("trauma_grave") or
        respostas.get("nivel_dor", 0) >= 8):
        return 2

    # AMARELO (3) — Urgente: precisa de atenção
    if (respostas.get("temperatura", 36.5) >= 38.5 or
        respostas.get("nivel_dor", 0) >= 5):
        return 3

    # VERDE (4) — Pouco urgente
    if (respostas.get("temperatura", 36.5) >= 37.5 or
        respostas.get("nivel_dor", 0) >= 2):
        return 4

    # AZUL (5) — Não urgente
    return 5


def realizar_triagem_terminal():
    """
    Executa a triagem pelo terminal (modo texto).
    Usado apenas para testes — a interface gráfica terá sua própria triagem.

    Returns:
        Cliente: O paciente criado com a prioridade classificada.
    """
    print("\n" + "=" * 50)
    print("TRIAGEM — Protocolo de Manchester")
    print("=" * 50)

    nome = input("\nNome do paciente: ").strip()
    if not nome:
        print("⚠ Nome não pode ser vazio.")
        return None

    print("\nResponda as perguntas abaixo (s = sim / n = não):\n")

    respostas = {}

    # Perguntas sim/não
    respostas["inconsciente"] = input("  O paciente está inconsciente? (s/n): ").lower() == "s"
    respostas["dificuldade_respirar"] = input("  Tem dificuldade severa para respirar? (s/n): ").lower() == "s"
    respostas["hemorragia"] = input("  Há hemorragia intensa? (s/n): ").lower() == "s"
    respostas["dor_peito"] = input("  Tem dor no peito? (s/n): ").lower() == "s"
    respostas["trauma_grave"] = input("  Suspeita de fratura exposta ou trauma grave? (s/n): ").lower() == "s"

    # Temperatura
    try:
        temp = input("  Temperatura corporal (ex: 37.5, ou 0 se não mediu): ")
        respostas["temperatura"] = float(temp) if float(temp) > 0 else 36.5
    except ValueError:
        respostas["temperatura"] = 36.5

    # Nível de dor
    try:
        dor = int(input("  Nível de dor de 0 a 10: "))
        respostas["nivel_dor"] = max(0, min(10, dor))
    except ValueError:
        respostas["nivel_dor"] = 0

    # Sintomas gerais
    sintomas = input("\n  Descreva os sintomas brevemente: ").strip()
    if not sintomas:
        sintomas = "Não informado"

    # Classificar
    prioridade = classificar_prioridade(respostas)
    paciente = Cliente(nome, prioridade, sintomas)

    print(f"\n{'=' * 50}")
    print(f"RESULTADO DA TRIAGEM")
    print(f"{'=' * 50}")
    print(paciente)
    print(f"{'=' * 50}")

    return paciente


# ============================================================
# TESTES — rode diretamente: python triagem.py
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("TESTE — Módulo Triagem")
    print("=" * 50)

    # Teste automático (sem input do usuário)
    print("\n--- Teste 1: Paciente inconsciente → VERMELHO ---")
    r1 = {"inconsciente": True, "dificuldade_respirar": False, "hemorragia": False,
          "dor_peito": False, "trauma_grave": False, "temperatura": 36.5, "nivel_dor": 0}
    p1 = classificar_prioridade(r1)
    print(f"  Prioridade: {p1} (esperado: 1)")
    assert p1 == 1

    print("\n--- Teste 2: Dor no peito → LARANJA ---")
    r2 = {"inconsciente": False, "dificuldade_respirar": False, "hemorragia": False,
          "dor_peito": True, "trauma_grave": False, "temperatura": 36.5, "nivel_dor": 3}
    p2 = classificar_prioridade(r2)
    print(f"  Prioridade: {p2} (esperado: 2)")
    assert p2 == 2

    print("\n--- Teste 3: Febre 39°C + dor 6 → AMARELO ---")
    r3 = {"inconsciente": False, "dificuldade_respirar": False, "hemorragia": False,
          "dor_peito": False, "trauma_grave": False, "temperatura": 39.0, "nivel_dor": 6}
    p3 = classificar_prioridade(r3)
    print(f"  Prioridade: {p3} (esperado: 3)")
    assert p3 == 3

    print("\n--- Teste 4: Febre leve 37.8°C → VERDE ---")
    r4 = {"inconsciente": False, "dificuldade_respirar": False, "hemorragia": False,
          "dor_peito": False, "trauma_grave": False, "temperatura": 37.8, "nivel_dor": 1}
    p4 = classificar_prioridade(r4)
    print(f"  Prioridade: {p4} (esperado: 4)")
    assert p4 == 4

    print("\n--- Teste 5: Tudo normal → AZUL ---")
    r5 = {"inconsciente": False, "dificuldade_respirar": False, "hemorragia": False,
          "dor_peito": False, "trauma_grave": False, "temperatura": 36.5, "nivel_dor": 0}
    p5 = classificar_prioridade(r5)
    print(f"  Prioridade: {p5} (esperado: 5)")
    assert p5 == 5

    print("\n--- Teste 6: Dor nível 9 → LARANJA ---")
    r6 = {"inconsciente": False, "dificuldade_respirar": False, "hemorragia": False,
          "dor_peito": False, "trauma_grave": False, "temperatura": 36.5, "nivel_dor": 9}
    p6 = classificar_prioridade(r6)
    print(f"  Prioridade: {p6} (esperado: 2)")
    assert p6 == 2

    print("\n" + "=" * 50)
    print("TODOS OS TESTES PASSARAM!")
    print("=" * 50)