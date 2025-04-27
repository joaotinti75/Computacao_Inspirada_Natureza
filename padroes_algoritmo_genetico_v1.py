from random import randint, random
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

def calcular_distancia_de_hamming(vetor_alvo, vetor_individuo):
    '''
    Retorna um número inteiro com o valor da distância de hamming entre um vetor alvo e um vetor indivíduo
    '''
    distancia = 0
    for alvo, individuo in zip(vetor_alvo, vetor_individuo):
        if alvo != individuo:
            distancia += 1

    return distancia

def gerar_vetor_de_distancias_hamming(populacao):
    '''
    Retorna uma lista contendo as distâcias de hamming para cada indivíduo da população
    '''
    vetor_de_distancias = []
    for individuo in populacao:
        distancia = calcular_distancia_de_hamming(BITSTRING_ALVO, individuo)
        vetor_de_distancias.append(distancia)
    return vetor_de_distancias

def gerar_vetor_de_aptidao(vetor_distancia_hamming):
    '''
    Retorna uma lista contendo os valores de aptidão de cada indivíduo da população
    '''
    vetor_de_aptidao = []
    for distancia in vetor_distancia_hamming:
        aptidao = TOTAL_DE_GENES - distancia
        vetor_de_aptidao.append(aptidao)
    return vetor_de_aptidao

def gerar_intervalo_da_roleta(vetor_de_aptidao):
    '''
    Retorna uma lista com os intervalos que cada indivíduo da população ocupa na roleta de seleção
    '''
    soma_das_aptidoes = sum(vetor_de_aptidao)
    #print('soma das aptidoes: ', soma_das_aptidoes)
    intervalos = []
    somas_parciais = 0 
    for aptidao in vetor_de_aptidao:
        graus = (aptidao * 360) / soma_das_aptidoes
        somas_parciais += graus
        #print(graus, somas_parciais)
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
    dicionario_de_geracoes[num_geracao]['dist'] = vetor_distancia_hamming
    
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

    for selecionado in individuos_selecionados:
        print('SELECIONADO: ', selecionado)

    print('Total de selecionados: ', len(individuos_selecionados))
    return individuos_selecionados

def reproduzir_individuos_selecionados(individuos_selecionados):
    '''
    Retorna uma lista contendo os indivíduos da nova população
    '''
    nova_populacao = []
    for i in range(0, len(individuos_selecionados), 2):

        print(' ')
        pares_de_acasalamento = individuos_selecionados[i:i+2]
        print(f'Par de acasalamento {i}')

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
        
        print(20 * '#')

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
                print('Aplicando mutacao')
                if gene == 0:
                    gene = 1
                else:
                    gene = 0 
            individuo_mutado.append(gene)
        populacao_mutada.append(individuo_mutado)
        individuo_mutado = []
    
    print('')
    print('POPULACAO_MUTADA')
    for i, individuo in enumerate(populacao_mutada):
        print(f'Individuo {i}: {individuo}')

    return populacao_mutada

TOTAL_DE_INDIVIDUOS = 8
TOTAL_DE_GENES = 12
PROBABILIDADE_CROSSSING_OVER = 0.2
PROBABILIDADE_MUTACAO = 0.02
BITSTRING_ALVO = CROMOSSOMO_ALVO = [1,1,1,1,0,1,1,0,1,1,1,1]
TOTAL_DE_GERACOES = 5

dicionario_de_geracoes = {}

for i in range(TOTAL_DE_GERACOES):
    print('')
    cprint(f'******************** Populacao {i} ********************', 'green', 'on_red')
    print('')

    if i == 0:
        print('População gerada aleatoriamente')
        populacao = gerar_populacao_inicial_aleatoria(TOTAL_DE_INDIVIDUOS, TOTAL_DE_GENES)
    else:
        print('População anterior mutada')
        populacao = populacao_mutada

    for i_ind, ind in enumerate(populacao):
        print(f'individuo {i_ind}: {ind}')
    print('')
    print('')

    numero_da_geracao = str(i)

    vetor_distancia_hamming = gerar_vetor_de_distancias_hamming(populacao)

    print(colored(f'Cromossomo alvo: {BITSTRING_ALVO}', 'red'))
    print(f'Distâncias de hamming: {vetor_distancia_hamming}')

    #Calculando as aptidões dos indivíduos da população
    vetor_de_aptidao = gerar_vetor_de_aptidao(vetor_distancia_hamming)
    print(colored(f'Vetor de aptidão: {vetor_de_aptidao}', 'green'))


    print('')
    intervalo_roleta = gerar_intervalo_da_roleta(vetor_de_aptidao)
    numeros_sorteados = gerar_vetores_numeros_roleta()
    print(colored(f'Numeros sorteados: {numeros_sorteados}', 'magenta'))
    print(' ')

    #Salvando e avaliando a população
    salvar_geracao_em_dicionario(numero_da_geracao)

    if dicionario_de_geracoes[numero_da_geracao]['mais_apto'] == TOTAL_DE_GENES:
        #Significa que encontrou o indivíduo mais apto
        break

    individuos_selecionados = selecionar_individuos_na_roleta(numeros_sorteados, dicionario_de_geracoes, numero_da_geracao)
    nova_populacao = reproduzir_individuos_selecionados(individuos_selecionados)
    populacao_mutada = aplicar_mutacao_na_populacao(nova_populacao)

