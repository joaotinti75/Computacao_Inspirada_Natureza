import numpy as np
import random

# --- Parâmetros do AG ---
POP_SIZE = 100
N_BITS = 10
MAX_GEN = 100
TOURN_SIZE = 3
CROSS_RATE = 0.9
MUT_RATE = 0.1

# --- Função de fitness ---
def fitness(x):
    return 2 ** (-2 * (((x - 0.1) / 0.9) ** 2)) * (np.sin(5 * np.pi * x) ** 6)

# --- Decodificar bitstring para número real ---
def decode(bitstring):
    int_val = int(bitstring, 2)
    return int_val / 1023

# --- Inicializar população ---
def init_population():
    return [''.join(random.choice('01') for _ in range(N_BITS)) for _ in range(POP_SIZE)]

# --- Seleção por torneio ---
def tournament_selection(pop, scores):
    selected = random.sample(list(zip(pop, scores)), TOURN_SIZE)
    return max(selected, key=lambda x: x[1])[0]

# --- Crossover ---
def crossover(p1, p2):
    if random.random() < CROSS_RATE:
        point = random.randint(1, N_BITS - 1)
        return p1[:point] + p2[point:], p2[:point] + p1[point:]
    return p1, p2

# --- Mutação ---
def mutate(bitstring):
    return ''.join(
        bit if random.random() > MUT_RATE else ('1' if bit == '0' else '0')
        for bit in bitstring
    )

# --- Algoritmo Genético ---
def genetic_algorithm():
    population = init_population()
    best, best_fit = None, 0
    avg_history = []  # ⬅️ Aqui vamos armazenar a média da população em cada geração

    for gen in range(MAX_GEN):
        decoded = [decode(ind) for ind in population]
        scores = [fitness(x) for x in decoded]

        # ⬅️ Salvar a média da população atual
        avg_history.append(np.mean(scores))
        
        # Atualizar melhor indivíduo
        for i in range(POP_SIZE):
            if scores[i] > best_fit:
                best, best_fit = population[i], scores[i]
        
        # Criar nova geração
        new_pop = []
        for _ in range(POP_SIZE // 2):
            p1 = tournament_selection(population, scores)
            p2 = tournament_selection(population, scores)
            c1, c2 = crossover(p1, p2)
            new_pop.extend([mutate(c1), mutate(c2)])
        
        population = new_pop

    best_x = decode(best)
    return best_x, best_fit, avg_history  # ⬅️ Retornamos também o histórico de médias

# --- Executar ---
best_x, best_fit, avg_history = genetic_algorithm()

# Exemplo de saída
print(f"Melhor solução: x = {best_x:.5f}, fitness = {best_fit:.5f}")
print("Histórico da média populacional nas gerações:")
print(avg_history)
