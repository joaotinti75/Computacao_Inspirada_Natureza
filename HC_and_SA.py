import numpy as np
import math
import os
import random
import time
import pandas as pd

xs = list(np.arange(0, 1, 0.001))
ys = []

for x in xs:
    x = float(x)
    y = 2.**(-2.*((((x-0.1) / 0.9))**2))*((np.sin(5.*np.pi*x))**6)
    ys.append(y)

def calculate_y(x):
    return 2.**(-2.*((((x-0.1) / 0.9))**2))*((np.sin(5.*np.pi*x))**6)

def hill_climbing(max_it, g):
    #x = np.random.rand() #valor aleatorio entre 0 e 1, pois o problema possui esse range
    x = 1 #pior cenário possível
    inicio_execucao = time.time()  # marca o tempo de início
    t = 1

    historico_x_melhor = []
    historico_x_melhor.append(x)

    historico_y_melhor = []
    historico_y_melhor.append(calculate_y(x))
    
    historico_x = []
    historico_x.append(x)
    
    historico_y = []
    historico_y.append(calculate_y(x))

    historico_t = []
    historico_t.append(t)
    
    while t <= max_it and calculate_y(x) < g:
        t += 1
        delta = np.random.normal(loc=0, scale=0.1)
        x_linha = x + delta
        if x_linha < 0 or x_linha > 1: #Condição para não sair do intervalo do problema
            continue
        if calculate_y(x_linha) > calculate_y(x):
            x = x_linha
            historico_x_melhor.append(x)
            historico_y_melhor.append(calculate_y(x))
            if calculate_y(x) == g:
                print(f'Solução encontrada na iteração {t}')
                break


        historico_x.append(x_linha)
        historico_y.append(calculate_y(x_linha))
        historico_t.append(t)
    
    parada_execucao = time.time()
    diferenca = parada_execucao - inicio_execucao
    tempo_da_execucao = diferenca

    return historico_x_melhor, historico_y_melhor, historico_x, historico_y, historico_t, tempo_da_execucao

#Parâmetros da subida da colina
max_it = 1000
g = 1
TOTAL_DE_EXECUCOES = 100
melhor_x_da_execucao = []
melhor_y_da_execucao = []
tempos_de_execucoes = []
for i in range(TOTAL_DE_EXECUCOES):
    historico_x_melhor, historico_y_melhor, historico_x, historico_y, historico_t, tempo_da_execucao = hill_climbing(max_it=max_it, g=g)
    melhor_x_da_execucao.append(historico_x_melhor[-1])
    melhor_y_da_execucao.append(historico_y_melhor[-1])
    tempos_de_execucoes.append(tempo_da_execucao)

media_x_melhor = sum(melhor_x_da_execucao) / len(melhor_x_da_execucao)
media_y_melhor = sum(melhor_y_da_execucao) / len(melhor_y_da_execucao)
desvio_padrao_x = math.sqrt(sum([(i-media_x_melhor)**2  for i in melhor_x_da_execucao]) / len(melhor_x_da_execucao))
desvio_padrao_y = math.sqrt(sum([(i-media_y_melhor)**2  for i in melhor_y_da_execucao]) / len(melhor_y_da_execucao))
media_do_tempo_de_execucao = sum(tempos_de_execucoes) / len(tempos_de_execucoes)

print('HILL CLIMBING')
print(f'Melhor X: {melhor_x_da_execucao[melhor_y_da_execucao.index(max(melhor_y_da_execucao))]}')
print(f'Melhor Y: {max(melhor_y_da_execucao)}')
print(f'Média de {TOTAL_DE_EXECUCOES} execucoes')
print(' ')
print(f'Média de x: {media_x_melhor}')
print(f'Média de y: {media_y_melhor}')
print(f'Desvio padrão de x: {desvio_padrao_x}')
print(f'Desvio padrão de y: {desvio_padrao_y}')
print(f'Média do tempo de execução: {media_do_tempo_de_execucao}')
print('')

def decrease_temperature(T):
    beta = 0.95
    return beta * T

def calculate_y(x):
    return 2.**(-2.*((((x-0.1) / 0.9))**2))*((np.sin(5.*np.pi*x))**6)

def simulated_annealing(g, max_it, T, T_min):
    T_minima = T_min
    x = 1 #pior cenário possível
    inicio_execucao = time.time()  # marca o tempo de início
    t = 1

    historico_x_melhor = []
    historico_x_melhor.append(x)

    historico_y_melhor = []
    historico_y_melhor.append(calculate_y(x))
    
    historico_x = []
    historico_x.append(x)
    
    historico_y = []
    historico_y.append(calculate_y(x))

    historico_t = []
    historico_t.append(t)

    historico_T = []
    historico_T.append(T)
    
    while calculate_y(x) < g and t < max_it and T >= T_minima:
        t += 1
        delta = np.random.normal(loc=0, scale=0.1)
        x_linha = x + delta
        if x_linha < 0 or x_linha > 1: #Condição para não sair do intervalo do problema
            continue
        if calculate_y(x_linha) > calculate_y(x):
            x = x_linha
            historico_x_melhor.append(x)
            historico_y_melhor.append(calculate_y(x_linha))
        else:
            aleatorio_0_1 = np.random.rand()
            #if aleatorio_0_1 < np.exp( ((calculate_y(x_linha) - calculate_y(x)) / T) ):
            diff = calculate_y(x_linha) - calculate_y(x)
            if aleatorio_0_1 < pow(math.e, (diff / T)):
                x = x_linha
                historico_x_melhor.append(x)
                historico_y_melhor.append(calculate_y(x_linha))

        historico_x.append(x_linha)
        historico_y.append(calculate_y(x_linha))
        historico_t.append(t)
        historico_T.append(T)
        
        T = decrease_temperature(T)
    
    parada_execucao = time.time()
    diferenca = parada_execucao - inicio_execucao
    tempo_da_execucao = diferenca
    
    return historico_x_melhor, historico_y_melhor, historico_x, historico_y, historico_t, historico_T, tempo_da_execucao


print(100*'=')
#Parâmetros do recozimento simulado
g = 1
max_it = 1000
Ts = [0.1,0.5,1,2,3,4,5]
T_mins = [1e-7, 1e-4, 1e-2, 0.01, 1]

TOTAL_DE_EXECUCOES = 100

dicionario_de_parametros_testados = {}
contador_de_testes = 0
for T in Ts:
    for T_min in T_mins:
        melhor_x_da_execucao = []
        melhor_y_da_execucao = []
        tempos_de_execucoes = []
        for i in range(TOTAL_DE_EXECUCOES):
            historico_x_melhor, historico_y_melhor, historico_x, historico_y, historico_t, historico_T, tempo_da_execucao = simulated_annealing(g, max_it, T, T_min)
            melhor_x_da_execucao.append(historico_x_melhor[-1])
            melhor_y_da_execucao.append(historico_y_melhor[-1])
            tempos_de_execucoes.append(tempo_da_execucao)
            
        
        media_x_melhor = sum(melhor_x_da_execucao) / len(melhor_x_da_execucao)
        media_y_melhor = sum(melhor_y_da_execucao) / len(melhor_y_da_execucao)
        desvio_padrao_x = math.sqrt(sum([(i-media_x_melhor)**2  for i in melhor_x_da_execucao]) / len(melhor_x_da_execucao))
        desvio_padrao_y = math.sqrt(sum([(i-media_y_melhor)**2  for i in melhor_y_da_execucao]) / len(melhor_y_da_execucao))
        media_do_tempo_de_execucao = sum(tempos_de_execucoes) / len(tempos_de_execucoes)
        
        dicionario_de_parametros_testados[str(contador_de_testes)] = {}
        dicionario_de_parametros_testados[str(contador_de_testes)]['T'] = T
        dicionario_de_parametros_testados[str(contador_de_testes)]['T_min'] = T_min
        dicionario_de_parametros_testados[str(contador_de_testes)]['melhor_x'] = melhor_x_da_execucao[melhor_y_da_execucao.index(max(melhor_y_da_execucao))]
        dicionario_de_parametros_testados[str(contador_de_testes)]['melhor_y'] = max(melhor_y_da_execucao)
        dicionario_de_parametros_testados[str(contador_de_testes)]['media_melhor_x'] = media_x_melhor
        dicionario_de_parametros_testados[str(contador_de_testes)]['media_melhor_y'] = media_y_melhor
        dicionario_de_parametros_testados[str(contador_de_testes)]['dp_x'] = desvio_padrao_x
        dicionario_de_parametros_testados[str(contador_de_testes)]['dp_y'] = desvio_padrao_y
        dicionario_de_parametros_testados[str(contador_de_testes)]['media_tempo'] = media_do_tempo_de_execucao
        
        print('SIMULATED ANNEALING')
        print(f'Melhor X: {melhor_x_da_execucao[melhor_y_da_execucao.index(max(melhor_y_da_execucao))]}')
        print(f'Melhor Y: {max(melhor_y_da_execucao)}')
        print(f'Média de {TOTAL_DE_EXECUCOES} execucoes')
        print(f'Parâmetros => T: {T}, T_min: {T_min}')
        print(f'Média de x: {media_x_melhor}')
        print(f'Média de y: {media_y_melhor}')
        print(f'Desvio padrão de x: {desvio_padrao_x}')
        print(f'Desvio padrão de y: {desvio_padrao_y}')
        print(f'Média do tempo de execução: {media_do_tempo_de_execucao}')
        print('')
        contador_de_testes += 1

#Salvando os resultados dos testes em um CSV
df = pd.DataFrame.from_dict(dicionario_de_parametros_testados, orient="index")
df.to_csv("resultados_algoritmo_genetico_exercicio_2.1.csv")