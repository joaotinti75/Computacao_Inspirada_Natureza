def perceptron():
    epoca = 1
    while epoca <= 10:
        print('')
        print(20*'=')
        print(f'Epoca {epoca}')
        print(20*'=')
        print('')

        for b, x1, x2, d in zip(BIAS, X1S, X2S, TRUE_OUTPUTS):
            u = calculate_u(b, x1, x2, weights)
            y = activation_function(u)
            if y != d:
                error = calculate_error(d, y)
                update_weights(weights, learning_rate, error, b, x1, x2)

        epoca += 1

def calculate_u(b, x1, x2, weights):
    return b * weights[0] + x1 * weights[1] + x2 * weights[2] 

def activation_function(u): #Step function
    if u > 0:
        return 1
    else:
        return 0

def update_weights(weights, learning_rate, error, b, x1, x2):
    #Atualizando os pesos
    weights[0] = weights[0] + learning_rate * error * b
    weights[1] = weights[1] + learning_rate * error * x1
    weights[2] = weights[2] + learning_rate * error * x2
    print('Novos pesos: ', weights)

def calculate_error(d, y):
    return d - y #saida desejada - saida calculada

X1S = [0,0,1,1]
X2S = [0,1,0,1]
BIAS = [1,1,1,1]
TRUE_OUTPUTS = [0,0,0,1]

weights = [0,0,0]
learning_rate = alfa = 0.5

perceptron()