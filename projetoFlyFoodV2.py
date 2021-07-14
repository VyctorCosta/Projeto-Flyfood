import tsplib95, time
from matplotlib import pyplot as plt
from module import *

problem = tsplib95.load('/home/vyctor/UFRPE/Projeto/testes/berlin52.tsp')
coords = problem.node_coords
distance_type = problem.edge_weight_type

# --------- PARAMETROS DO ALGORITMO -----------
seed = 1626206618.6914158           # <---- Semente randomica do experimento OBS: Deixe None caso não queira especificar nenhuma semente    
cross_type = 'torneio'      # <---- Parametro para o tipo de cruzamento. | 'Torneio' ou 'Roleta' 
number_individuals = 100    # <---- Numero de Individuos existentes na população
generations = 400           # <---- Numero de gerações
elitism = False             # <---- Parametro para ter elitismo no algoritmo, True ou False
num_elitism = None          # <---- Numero de individuos salvos para a proxima geração, APENAS se o elitismo for Verdadeiro. Caso queira deixar padrão coloque None. num_elitism padrão = 1
# ---------------------------------------------
a = time.clock_gettime(1)    
seed = setRandomSeed(seed)     
alg = GA(number_individuals, coords)
alg.setFitness()

for i in range(1, generations+1):
    alg.crossing_population(cross_type)
    alg.selectBestIndividuals(elitism, num_elitism)
    alg.setFitness()

    
b = time.clock_gettime(1)
print('')
best_individual = alg.returnBestIndividual()
print(f'Distancia: {best_individual.returnDistance()}')
print(f'Tempo gasto: {abs(a-b):.2f}' )
print(f'Semente randomica: {seed}')