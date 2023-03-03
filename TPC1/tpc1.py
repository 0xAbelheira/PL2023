from validator import *
from pessoa import * 
from dados import * 
import matplotlib.pyplot as plt
import numpy as np

def carregar_dados(path):
    file = open(path)
    f = file.readlines()
    f.pop(0) #tirar a primeira linha do comentario

    lista = list()
    extremos = {
        "idade":{
            "max" : float('-inf'),
            "min" : float('inf')
        },
        "colesterol": {
            "max" : float('-inf'),
            "min" : float('inf')
        }
    }

    for line in f:
        line = line.replace("\n","")
        lines = line.split(",")

        if len(lines) == 6:
            if validar_inteiro(lines[0])            \
                and validar_sexo(lines[1])          \
                and validar_inteiro(lines[2])       \
                and validar_inteiro(lines[3])       \
                and validar_inteiro(lines[4])       \
                and validar_bit(lines[5]):
                idade = int(lines[0])
                sexo = lines[1]
                tensao = int(lines[2])
                colesterol = int(lines[3])
                batimento = int(lines[4])
                doenca = bool(int(lines[5]))

                lista.append(Pessoa(idade, sexo, tensao, colesterol, batimento, doenca))

                if idade > extremos["idade"]["max"]:
                    extremos["idade"]["max"] = idade
                elif idade < extremos["idade"]["min"]:
                    extremos["idade"]["min"] = idade

                if colesterol > extremos["colesterol"]["max"]:
                    extremos["colesterol"]["max"] = colesterol
                elif colesterol < extremos["colesterol"]["min"]:
                    extremos["colesterol"]["min"] = colesterol
                    
    file.close()

    return Dados(lista, extremos)

def distribuicao_sexo(dados): # testa quantos elementos de cada sexo têm a doença e quantos não têm
    res = {
        "M" : {
            False : 0,
            True : 0
        },
        "F" : {
            False : 0,
            True : 0
        }
    }

    for pessoa in dados.lista:
        res[pessoa.sexo][pessoa.doenca] += 1

    return res

def distribuicao_faixaEtaria(dados): # idade máxima é 77 e mínima 28
    max = dados.extremos["idade"]["max"]

    res = dict()
    for i in range(0, (max//5) + 1): # x * 5 -> mínimo || (x * 5) + 4 -> máximo
        res[(i*5, i*5 + 4)] = {
            False : 0,
            True : 0
        }

    for pessoa in dados.lista:
        intervalo = pessoa.idade//5
        res[(intervalo*5, intervalo*5 + 4)][pessoa.doenca] += 1
        

    return res

def distribuicao_colesterol(dados):
    min = dados.extremos["colesterol"]["min"]
    max = dados.extremos["colesterol"]["max"]

    res = dict()
    for i in range(min // 10, (max // 10) + 1):
        res[(i*10, i*10 + 9)] = {
            False : 0,
            True : 0
        }
    
    for pessoa in dados.lista:
        intervalo = pessoa.colesterol // 10
        res[(intervalo * 10, intervalo * 10 + 9)][pessoa.doenca] += 1

    return res

def tabela_distribuicao(distribuicao):
    # Define a tabela como uma lista de listas
    tabela = [["", "Com doença", "Sem doença"]]
    
    for key in distribuicao.keys():
        tabela += [[str(key), str(distribuicao[key][True]), str(distribuicao[key][False])]]

    # Define o número de colunas e linhas da tabela
    num_colunas = len(tabela[0])
    num_linhas = len(tabela)

    # Define a largura das colunas
    larguras = [max(len(tabela[i][j]) for i in range(num_linhas)) for j in range(num_colunas)]

    # Imprime a tabela
    for i in range(num_linhas):
        for j in range(num_colunas):
            print("{:{}}".format(tabela[i][j], larguras[j]), end="  ")
        print()

def distribuicaoGrafico(distribuicao, f):
    x_eixo = np.arange(len(distribuicao.keys()))
    x_coords = [str(elem) for elem in distribuicao.keys()]
    y_cd = [elem[True] for elem in distribuicao.values()]
    y_sd = [elem[False] for elem in distribuicao.values()]

    plt.figure(figsize=[13, 9])

    plt.barh(x_eixo - 0.2, y_cd, color = "orchid", label="Com doença", tick_label=x_coords, height=0.4)
    plt.barh(x_eixo + 0.2, y_sd, color = "skyblue", label="Sem doença", tick_label=x_coords, height=0.4)

    plt.yticks(x_eixo, distribuicao.keys())
    plt.xlabel("Frequência Absoluta")
    
    match f:
        case 0: 
            plt.title("Distribuição por Sexo")
        case 1:
            plt.title("Distribuição por Escalão Etário")
        case 2:
            plt.title("Distribuição por Níveis de Colesterol")

    plt.legend()
    plt.show()

csv_path = input("Path do ficheiro CSV:\n")
dados = carregar_dados(csv_path)
print("Dados Carregados")

option = 0
while option != 4:
    print('\n')
    print('Escolha uma opção')
    print('-----------------------------------------')
    print('1 - Distribuição por Sexo')
    print('2 - Distribuição por Escalões Etários')
    print('3 - Distribuição por Níveis de Colesterol')
    print('4 - Sair')
    print('-----------------------------------------')
    option = int(input())

    match option:
        case 1:
            print("------------------------------------------")
            print("1 - Tabela")
            print("2 - Gráfico")
            print("------------------------------------------")
            format = int(input())

            match format:
                case 1:
                    tabela_distribuicao(distribuicao_sexo(dados))
                case 2:
                    distribuicaoGrafico(distribuicao_sexo(dados),0)
                case _:
                    print("Opção inválida!")
        case 2:
            print("------------------------------------------")
            print("1 - Tabela")
            print("2 - Gráfico")
            print("------------------------------------------")
            format = int(input())

            match format:
                case 1:
                    tabela_distribuicao(distribuicao_faixaEtaria(dados))
                case 2:
                    distribuicaoGrafico(distribuicao_faixaEtaria(dados),1)
                case _:
                    print("Opção inválida!")
        case 3:
            print("------------------------------------------")
            print("1 - Tabela")
            print("2 - Gráfico")
            print("------------------------------------------")
            format = int(input())

            match format:
                case 1:
                    tabela_distribuicao(distribuicao_colesterol(dados))
                case 2:
                    distribuicaoGrafico(distribuicao_colesterol(dados),2)
                case _:
                    print("Opção inválida!")
        case 4:
            print("A sair...")
        case _:
            print("Opção inválida!")



