from random import randint, random, sample
import numpy as np
import math 
import time
import pandas as pd
from termcolor import colored, cprint

def gerar_populacao_inicial_aleatoria(TOTAL_DE_INDIVIDUOS, TOTAL_DE_GENES):
    '''
    Retorna uma lista de listas, onde cada lista representa um indivíduo da população
    '''
    populacao = []
    for i in range(TOTAL_DE_INDIVIDUOS):
        individuo = [randint(0,1) for i in range(TOTAL_DE_GENES)]
        populacao.append(individuo)

    return populacao

def decodificar_bitstring_individuo(individuo_binarizado):
    '''
    Retorna o número decimal correspondente à bitstring do indivíduo
    '''
    cromossomo_string = ''.join(str(i) for i in individuo_binarizado)
    parte1 = cromossomo_string[:5]
    parte2 = cromossomo_string[5:]
    base_10_parte1 = int(parte1, 2) #conversao de binario para base 10
    base_10_parte2 = int(parte2, 2) #conversao de binario para base 10

    base_10_normalizado_parte1 = base_10_parte1 / ((2**(TOTAL_DE_GENES//2)) - 1)
    base_10_normalizado_parte2 = base_10_parte2 / ((2**(TOTAL_DE_GENES//2)) - 1)

    return base_10_normalizado_parte1, base_10_normalizado_parte2

def calcular_z(x, y):
    '''
    Retorna o valor de z do indivíduo
    '''
    termo1 = (1-x)**2
    termo2 = 100 * ((y-x**2))**2
    z = termo1 + termo2

    return z


def gerar_vetor_de_decimais(populacao):
    '''
    Retorna uma lista contendo os números decimais de cada indivíduo da população
    '''
    vetor_de_decimais_parte1 = []
    vetor_de_decimais_parte2 = []

    for individuo in populacao:
        decimal_parte1, decimal_parte2 = decodificar_bitstring_individuo(individuo)
        vetor_de_decimais_parte1.append(decimal_parte1)
        vetor_de_decimais_parte2.append(decimal_parte2)

    return vetor_de_decimais_parte1, vetor_de_decimais_parte2

def gerar_vetor_de_aptidao(vetor_de_decimais_parte1, vetor_de_decimais_parte2):
    '''
    Retorna uma lista contendo os valores de aptidão de cada indivíduo da população
    '''
    vetor_de_aptidao = []
    for decimal_parte1, decimal_parte2 in zip(vetor_de_decimais_parte1, vetor_de_decimais_parte2):
        aptidao = calcular_z(decimal_parte1, decimal_parte2)
        vetor_de_aptidao.append(aptidao)

    vetor_de_aptidao_positivo = [abs(i) for i in vetor_de_aptidao]
    soma_vetor_de_aptidao = sum(vetor_de_aptidao_positivo)
    if soma_vetor_de_aptidao == 0:
        vetor_de_aptidao = [1 - 0 for i in vetor_de_aptidao]
    else:
        vetor_de_aptidao = [1 - (i/soma_vetor_de_aptidao) for i in vetor_de_aptidao]

    print(vetor_de_aptidao)
    return vetor_de_aptidao

def selecionar_por_torneio(populacao, N=3):
    '''
    Retorna uma lista de indivíduos selecionados por torneio
    n = 3 por padrão
    '''
    vencedores_selecionados = []
    N = COMPETIDORES_POR_TORNEIO
    print(f'Selecionando por torneio com N={N}')

    for i in range(TOTAL_DE_INDIVIDUOS):
        print(f'Torneio {i}')
        competidores = sample(populacao, N)
        notas_dos_competidores = []
        for competidor in competidores:

            decimal_parte1, decimal_parte2 = decodificar_bitstring_individuo(competidor)
            nota = calcular_z(decimal_parte1, decimal_parte2)
            notas_dos_competidores.append(nota)
            print('competidor: ', competidor, ' nota: ', nota)

        vetor_de_aptidao_positivo = [abs(i) for i in vetor_de_aptidao]
        soma_nota_dos_competidores = sum(vetor_de_aptidao_positivo)
        if soma_nota_dos_competidores == 0:
            notas_dos_competidores = [1 - 0 for i in notas_dos_competidores]
        else:
            notas_dos_competidores = [1 - (i/soma_nota_dos_competidores) for i in notas_dos_competidores]

        indice_do_maior = notas_dos_competidores.index(max(notas_dos_competidores))
        vencedor = competidores[indice_do_maior]
        print('vencedor: ', vencedor)
        vencedores_selecionados.append(vencedor)
        print(20*'=')

    print('Total de vencedores: ', len(vencedores_selecionados))
    return vencedores_selecionados

def selecionar_por_amostragem_universal_estocastica(dicionario_de_geracoes, num_geracao):
    '''
    Seleciona os indivíduos por amostragem universal estocastica
    '''
    posicoes_das_agulhas = [i for i in range(1, 360, 360//TOTAL_DE_INDIVIDUOS)]
    
    individuos_selecionados = []
    for agulha in posicoes_das_agulhas:
        intervalos_minimos = dicionario_de_geracoes[num_geracao]['min']
        intervalos_maximos = dicionario_de_geracoes[num_geracao]['max']
        populacoes = dicionario_de_geracoes[num_geracao]['pop']
        for min, max, individuo in zip(intervalos_minimos, intervalos_maximos, populacoes):
            if agulha > min and agulha <= max:
                cprint(f'{min} - {max} {individuo} {agulha} --> escolhido', 'green')
                individuos_selecionados.append(individuo)
            else:
                print(min, ' - ',max, individuo, agulha)
        print(50 * '*')

    return individuos_selecionados


def gerar_intervalo_da_roleta(populacao, vetor_de_aptidao):
    '''
    Retorna uma lista com os intervalos que cada indivíduo da população ocupa na roleta de seleção
    '''
    if APTIDAO_POR_RANKING:
        #Função de aptidão por ranking
        ranking_individuos = []
        probabilidade_do_ranking = []
        probabilidades_top_5 = [0.4, 0.2, 0.15, 0.1, 0.05]
        probabilidades_dos_restantes = 1 - sum(probabilidades_top_5)
        
        copia_populacao = populacao.copy()
        copia_vetor_de_aptidao = vetor_de_aptidao.copy()

        for prob in probabilidades_top_5:
            probabilidade_do_ranking.append(float(prob*360)) 
            index = copia_vetor_de_aptidao.index(max(copia_vetor_de_aptidao))
            copia_vetor_de_aptidao.pop(index)            
            individuo = copia_populacao.pop(index)
            ranking_individuos.append(individuo)

        total_de_individuos_restantes = TOTAL_DE_INDIVIDUOS - len(ranking_individuos)
        
        probabilidades_dos_restantes = [(probabilidades_dos_restantes / total_de_individuos_restantes) * 360 for i in range(total_de_individuos_restantes)]

        ranking_individuos.extend(copia_populacao)
        probabilidade_do_ranking.extend(probabilidades_dos_restantes)

        intervalos = []
        somas_parciais = 0
        #print('Populacao ordenada dentro da funcao: ')
        for ind, prob in zip(ranking_individuos, probabilidade_do_ranking):
            somas_parciais += prob
            intervalos.append(float(somas_parciais))
            #print(ind, prob, calcular_z(decodificar_bitstring_individuo(ind)))

        return ranking_individuos, intervalos

    else:
        #Função de aptidão padrão
        soma_das_aptidoes = sum(vetor_de_aptidao)
        intervalos = []
        somas_parciais = 0 
        for aptidao in vetor_de_aptidao:
            graus = (aptidao * 360) / soma_das_aptidoes
            somas_parciais += graus
            intervalos.append(float(somas_parciais))

        return intervalos

def gerar_vetores_numeros_roleta():
    '''
    Retorna uma lista com os numeros sorteados na roleta
    '''
    numeros_sorteados = []
    for i in range(TOTAL_DE_INDIVIDUOS):
        numero = randint(1,360)
        numeros_sorteados.append(numero)

    return numeros_sorteados

def salvar_geracao_em_dicionario(num_geracao):
    '''
    Popula o dicionario de geracoes com seus individuos, aptidoes e outros atributos
    '''
    num_geracao = str(num_geracao)
    dicionario_de_geracoes[num_geracao] = {}
    dicionario_de_geracoes[num_geracao]['pop'] = populacao
    dicionario_de_geracoes[num_geracao]['vet_dec_pt1'] = vetor_de_decimais_parte1
    dicionario_de_geracoes[num_geracao]['vet_dec_pt2'] = vetor_de_decimais_parte2

    
    dicionario_de_geracoes[num_geracao]['apt'] = vetor_de_aptidao
    
    dicionario_de_geracoes[num_geracao]['inter_roleta'] = intervalo_roleta
    dicionario_de_geracoes[num_geracao]['media'] = sum(dicionario_de_geracoes[num_geracao]['apt']) / len(dicionario_de_geracoes[num_geracao]['apt'])
    
    dicionario_de_geracoes[num_geracao]['mais_apto'] = max(dicionario_de_geracoes[num_geracao]['apt'])

    lista_inter_minimo = []
    lista_inter_maximo = []
    for i in range(len(intervalo_roleta)):
        if i == 0:
            intervalo_min = 0
        else:
            intervalo_min = intervalo_roleta[i-1]
        
        intervalo_max = intervalo_roleta[i]

        lista_inter_minimo.append(round(intervalo_min))
        lista_inter_maximo.append(round(intervalo_max))

    dicionario_de_geracoes[num_geracao]['min'] = lista_inter_minimo
    dicionario_de_geracoes[num_geracao]['max'] = lista_inter_maximo

    print(f"Média da população {num_geracao}: {dicionario_de_geracoes[num_geracao]['media']}")
    print(f"Melhor aptidão da população {num_geracao}: {dicionario_de_geracoes[num_geracao]['mais_apto']}")

def selecionar_individuos_na_roleta(numeros_sorteados, dicionario_de_geracoes, num_geracao):
    '''
    Retorna uma lista com os individuos escolhidos na roleta
    '''
    individuos_selecionados = []
    for sorteado in numeros_sorteados:
        intervalos_minimos = dicionario_de_geracoes[num_geracao]['min']
        intervalos_maximos = dicionario_de_geracoes[num_geracao]['max']
        populacoes = dicionario_de_geracoes[num_geracao]['pop']
        for min, max, individuo in zip(intervalos_minimos, intervalos_maximos, populacoes):
            if sorteado > min and sorteado <= max:
                cprint(f'{min} - {max} {individuo} {sorteado} --> escolhido', 'green')
                individuos_selecionados.append(individuo)
            else:
                print(min, ' - ',max, individuo, sorteado)
        print(50 * '*')

    return individuos_selecionados

def reproduzir_individuos_selecionados(individuos_selecionados):
    '''
    Retorna uma lista contendo os indivíduos da nova população
    '''
    nova_populacao = []
    for i in range(0, len(individuos_selecionados), 2):
        print(' ')
        print(f'Par de acasalamento {i}')   
        pares_de_acasalamento = individuos_selecionados[i:i+2]

        individuo_pai = pares_de_acasalamento[0]
        print(colored(individuo_pai, 'green'))

        if len(pares_de_acasalamento) == 2:
        
            individuo_mae = pares_de_acasalamento[1]
            print(colored(individuo_mae, 'red'))

            numero_aleatorio_0_1 = random()
            print('numero aleatorio 0-1: ', numero_aleatorio_0_1)
            if numero_aleatorio_0_1 <= PROBABILIDADE_CROSSSING_OVER:
                #Realizar cruzamento
                print('Realizando cruzamento')
                ponto_do_crossing_over = randint(1, TOTAL_DE_GENES - 1)
                print('Ponto Crossing Over: ', ponto_do_crossing_over)

                filho_1 = individuo_pai[:ponto_do_crossing_over] + individuo_mae[ponto_do_crossing_over:]
                filho_2 = individuo_mae[:ponto_do_crossing_over] + individuo_pai[ponto_do_crossing_over:]

                print('filho 1: ', colored(individuo_pai[:ponto_do_crossing_over],'green'), colored(individuo_mae[ponto_do_crossing_over:],'red'))
                print('filho 2: ', colored(individuo_mae[:ponto_do_crossing_over],'red'), colored(individuo_pai[ponto_do_crossing_over:],'green'))

                #Adicionando os filhos na próxima geração
                nova_populacao.append(filho_1)
                nova_populacao.append(filho_2)

            else:
                #Pais originais são repetidos na próxima geração
                print('Não realizando o cruzamento')
                nova_populacao.append(individuo_pai)
                nova_populacao.append(individuo_mae)

        else:
            #Se pai não tiver mãe para acasalar, repetir pai
            print('Pai solteiro')
            nova_populacao.append(individuo_pai)        
        
    print('NOVA POPULACAO')
    for i, individuo in enumerate(nova_populacao):
        print(f'INDIVIDUO {i}: {individuo}')

    return nova_populacao

def aplicar_mutacao_na_populacao(populacao):
    '''
    Aplica uma mutação na populacao de acordo com uma probabilidade e retorna uma lista com os novos indivíduos 
    '''
    populacao_mutada = []
    individuo_mutado = []
    for individuo in populacao:
        for gene in individuo:
            numero_aleatorio_0_1 = random()
            if numero_aleatorio_0_1 <= PROBABILIDADE_MUTACAO:
                #Aplicar mutacao
                print('Aplicando a mutação')
                if gene == 0:
                    gene = 1
                else:
                    gene = 0 
            individuo_mutado.append(gene)
        populacao_mutada.append(individuo_mutado)
        individuo_mutado = []

    print('')
    print('População mutada')
    for ind in populacao_mutada:
        print(ind)

    return populacao_mutada

TOTAL_DE_INDIVIDUOS = 100
TOTAL_DE_GENES = 10
PROBABILIDADE_CROSSSING_OVER = 0.9
PROBABILIDADE_MUTACAO = 0.02
COMPETIDORES_POR_TORNEIO = 3
TOTAL_DE_GERACOES = 100
APTIDAO_POR_RANKING = False
METODO_DE_SELECAO = 'roleta' #roleta, sus ou competicao

dicionario_de_geracoes = {}

historico_medias = []

for ger in range(TOTAL_DE_GERACOES):
    if ger == 0:
        print('População gerada aleatoriamente')
        populacao = gerar_populacao_inicial_aleatoria(TOTAL_DE_INDIVIDUOS, TOTAL_DE_GENES)
    else:
        print('População anterior mutada')
        populacao = populacao_mutada

    numero_da_geracao = str(ger)

    #populacao = gerar_populacao_inicial_aleatoria(TOTAL_DE_INDIVIDUOS, TOTAL_DE_GENES)
    vetor_de_decimais_parte1, vetor_de_decimais_parte2 = gerar_vetor_de_decimais(populacao)
    vetor_de_aptidao = gerar_vetor_de_aptidao(vetor_de_decimais_parte1, vetor_de_decimais_parte2)

    media = sum(vetor_de_aptidao) / TOTAL_DE_INDIVIDUOS
    historico_medias.append(media)

    for ind, x, y, aptidao in zip(populacao, vetor_de_decimais_parte1, vetor_de_decimais_parte2, vetor_de_aptidao):
        print(ind, x, y, aptidao)

    print('')

    #Para seleção por roleta    
    if APTIDAO_POR_RANKING:
        populacao, intervalo_roleta = gerar_intervalo_da_roleta(populacao, vetor_de_aptidao)
    else:
        intervalo_roleta = gerar_intervalo_da_roleta(populacao, vetor_de_aptidao)

    numeros_sorteados = gerar_vetores_numeros_roleta()

    #Salvando e avaliando a população
    salvar_geracao_em_dicionario(numero_da_geracao)
    #individuos_selecionados = selecionar_individuos_na_roleta(numeros_sorteados, dicionario_de_geracoes, numero_da_geracao)

    #Para seleção por amostragem universal estocástica
    #individuos_selecionados = selecionar_por_amostragem_universal_estocastica(dicionario_de_geracoes, numero_da_geracao)

    #Para seleção por competição
    if METODO_DE_SELECAO == 'competicao':
        individuos_selecionados = selecionar_por_torneio(populacao)
    elif METODO_DE_SELECAO == 'roleta':
        individuos_selecionados = selecionar_individuos_na_roleta(numeros_sorteados, dicionario_de_geracoes, numero_da_geracao)
    elif METODO_DE_SELECAO == 'sus':
        individuos_selecionados = selecionar_por_amostragem_universal_estocastica(dicionario_de_geracoes, numero_da_geracao)
    else:
        print('Metodo de seleção incorreto ou indefinido')
        break

    nova_populacao = reproduzir_individuos_selecionados(individuos_selecionados)
    populacao_mutada = aplicar_mutacao_na_populacao(nova_populacao)
    print(50 * '=')


    