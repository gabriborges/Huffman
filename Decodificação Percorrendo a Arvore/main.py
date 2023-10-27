# Gabriel Borges Carvalho - CC8
import pandas as pd
from classes import Leave, Node, imprimir_arvore

# uma serie do pandas criada com metodos aplicados Ordenação e Soma de Itens na serie


def Inicializar_Serie(entrada):
    entrada_unicos = list(set(entrada))
    entrada_inicial = {}

    for caractere in entrada_unicos:
        entrada_inicial[caractere] = entrada.count(caractere)

    tabela = pd.Series(entrada_inicial)
    tabela_sorted = tabela.sort_values(ascending=True)
    soma = tabela_sorted.sum()

    return tabela_sorted, (tabela_sorted/soma)*100


def Criar_Folhas(data, lista=[]):
    for indice, valor in data.items():
        folha = Leave(valor, indice)
        lista.append(folha)
    return lista

# busca o indice em que o novo No sera inserido na lista ordenada


def buscar_indice_INSERTION_SORT(lista, freq_no):
    for i in range(len(lista)):
        if lista[i].freq >= freq_no:
            return i
    return len(lista)


def Criar_Nos(lista):
    lista_folhas = lista
    while len(lista_folhas) > 1:
        esquerda = lista_folhas.pop(0)
        direita = lista_folhas.pop(0)

        novo_no_freq = esquerda.freq + direita.freq
        novo_no = Node(novo_no_freq, esquerda, direita)

        indice_insercao = buscar_indice_INSERTION_SORT(
            lista_folhas, novo_no_freq)
        lista_folhas.insert(indice_insercao, novo_no)
    return lista_folhas


def Atribuir_Codigo_Binario(node, codigo_atual="", tabela_codigos={}):
    if isinstance(node, Leave):
        tabela_codigos[node.caractere] = codigo_atual
    else:
        if node.left:
            Atribuir_Codigo_Binario(
                node.left, codigo_atual + "0", tabela_codigos)
        if node.right:
            Atribuir_Codigo_Binario(
                node.right, codigo_atual + "1", tabela_codigos)


def Codificar_String(texto, tabela_codigos):
    string_codificada = ""
    for caractere in texto:
        if caractere in tabela_codigos:
            codigo = tabela_codigos[caractere]
            string_codificada += codigo
    return string_codificada

def Verificar_Codigo(node, binario, codigo_atual=""):

    if isinstance(node, Leave):
        return node.caractere, codigo_atual
    elif binario is None:
        return -1, -1
    elif binario[0] == '0':
        if len(binario) == 1:
            return Verificar_Codigo(node.left, None, codigo_atual + "0")
        else:
            return Verificar_Codigo(node.left, binario[1:], codigo_atual + "0")
    elif binario[0] == '1':
        if len(binario) == 1:
            return Verificar_Codigo(node.right, None, codigo_atual + "1")
        else:
            return Verificar_Codigo(node.right, binario[1:], codigo_atual + "1")

def Decodificar_String(binario, node, decodificado):
    codigo_atual = ""
    if len(binario) == 0:
        return ""
    else:
        for bit in binario:
            codigo_atual += bit
            caractere, codigo = Verificar_Codigo(node, codigo_atual)
            if codigo == codigo_atual:
                return caractere + Decodificar_String(binario[len(codigo_atual):], node, decodificado + caractere)
            
    return decodificado


if __name__ == "__main__":

    texto = 'IFMA CAMPUS CAXIAS'
    # texto = input("Texto: ")

    # 'data' retorna uma serie do pandas com cada caractere e sua frequencia em inteiro, ordenado menor para o maior
    data, data_percent = Inicializar_Serie(texto)

    # cria uma lista de folhas a partir de um dicionario, o dicionario inicial já esta ordenado
    lista_folhas = Criar_Folhas(data)

    # organiza as folhas e nos que as ligam e atualiza na propria lista
    lista_nos = Criar_Nos(lista_folhas)

    raiz = lista_nos[0]

    # cria um dicionario com cada caractere como Chave e o seu codigo como Valor
    tabela_codigos = {}
    Atribuir_Codigo_Binario(raiz, "", tabela_codigos)

    # string codificada em binario
    string_codificada = Codificar_String(texto, tabela_codigos)

    # string decodificada
    string_decodificada = Decodificar_String(string_codificada, raiz, "")

    print("Tabela de Códigos: ")
    for caractere, codigo in tabela_codigos.items():
        print(f"{caractere}, {codigo}")
    print(f'\nCodificado: {string_codificada}')
    print(f'Decodificado: {string_decodificada}')

    # considerando cada caractere com 8 bits
    bytes_original = len(texto)
    bytes_huffman = len(string_codificada)/8
    reducao = "{:.2f}".format(((bytes_huffman*100/bytes_original)-100)*-1)

    print(
        f'\nQuantidade de Bytes antes e depois: {bytes_original} bytes -> {bytes_huffman} bytes ({reducao}% menor) \n')
