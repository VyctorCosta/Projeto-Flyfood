import time
#Função pegar matriz e colocar as letras e coordenadas em uma lista
def CriarListaPontos(tam_linha, tam_coluna, lista=[]):
    for linha in range(tam_linha, 0, -1):
        linha_atual = input().upper().split()
        for indice_coluna, valor in enumerate(linha_atual):
            if valor != '0':
                lista.append({'letra': valor,'coordenadas': (indice_coluna+1, linha)})
    return lista

#Função calcular a Distancia entre 2 pontos
def Distancia2Pontos(PontoA, PontoB):
    xA, xB, yA, yB = PontoA['coordenadas'][0], PontoB['coordenadas'][0], PontoA['coordenadas'][1], PontoB['coordenadas'][1]
    distancia =  abs(xA - xB) + abs(yA - yB)
    return distancia

#Função calcular distancia entre n pontos A,B,C...
def DistanciaNPontos(string_ponto, lista_pontos):
    for ponto in lista_pontos:
        if ponto['letra'] == string_ponto[-1:]:
            Ponto_An = ponto
        elif ponto['letra'] == string_ponto[-2:-1]:
            Ponto_An_1 = ponto
    
    if len(string_ponto) > 2:
        string_ponto = string_ponto[:-1]
        return DistanciaNPontos(string_ponto, lista_pontos) + Distancia2Pontos(Ponto_An_1, Ponto_An)
    else:
        return Distancia2Pontos(Ponto_An, Ponto_An_1)

#Função para Permutar uma string 

def Permutar(string):
    if len(string) == 1:
        yield from string
    lista_permutações = []
    for letra in string:
        string_aux = string.replace(letra, '')
        lista_permutações.extend([letra+string for string in Permutar(string_aux)])
    yield from lista_permutações


tam_linha, tam_coluna = [int(tamanho) for tamanho in input().split()]
lista_pontos = CriarListaPontos(tam_linha, tam_coluna)
string_pontos = ''
for item in lista_pontos: #Pegando as letras que serão permutadas
    letra = item['letra']
    if letra != 'R':
        string_pontos += letra
a = time.clock_gettime(1)

lista_pontos_permutados = Permutar(string_pontos)

#Pegando a distancia de cada ponto na lista permutada e escolhendo o ponto que tenha a menor distancia
for ponto in lista_pontos_permutados:
    menor_ponto = 'R' + ponto + 'R'
    menor_distancia = DistanciaNPontos(menor_ponto, lista_pontos)
    break
for ponto in lista_pontos_permutados:
    ponto = 'R' + ponto + 'R'
    distancia_ponto = DistanciaNPontos(ponto, lista_pontos)
    if distancia_ponto < menor_distancia:
        menor_ponto = ponto
        menor_distancia = distancia_ponto
b = time.clock_gettime(1)
tempo = abs(a-b)
print(menor_ponto[1:-1])
print('tempo gasto: %.2f' %(tempo))
