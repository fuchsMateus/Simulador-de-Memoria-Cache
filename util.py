#Modulo que contem funcoes uteis

import math

#Funcao que checa se um endereco fornecido pelo usuario e valido, contando os bits e verificando se e formado apenas por 1s e 0s
def enderecoValido(endereco, tamanhoEndereco):
    return len(endereco) == tamanhoEndereco and all(i in '01' for i in endereco)

#Checa se um numero e potencia de 2
def isPot2(n):
    return math.log2(n).is_integer()

#Funcao para calcular 'w', 'd', 's' e 'tag'
def calcularValores(palavraspBloco, nBlocos, nConjuntos):
    w = int(math.log2(palavraspBloco))
    s = int(math.log2(nBlocos))
    d = int(math.log2(nConjuntos))
    tag = s-d
    return w, d, s, tag  

#Funcao para ler o conteudo de um arquivo
def lerArquivo(caminho):
    conteudo = []
    with open(caminho, 'r') as arquivo:
        for linha in arquivo:
            conteudo.append(linha.strip())

    return conteudo  

#Funcao da converter uma string representando um binario para um decimal
def binParaDec(bin):
    dec = 0
    val =  1
    #Comeca a somar a partir do bit menos significativo
    for bit in bin[::-1]:
        if bit == '1': dec += val
        val *= 2
    return int(dec)