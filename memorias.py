#Modulo que contem as classes das memorias

import time
import random

class MemoriaPrincipal:
    def __init__(self, nPalavras, palavrasPBloco, nBlocos):
        self.nPalavras = nPalavras
        self.palavrasPBloco = palavrasPBloco
        self.nBlocos = nBlocos
        self.inicializar()

    blocos = []

    def inicializar(self):
        for i in range(self.nBlocos):
            bloco = []
            for j in range(self.palavrasPBloco):
                #Sendo a palavra um inteiro de 32 bits (de −2,147,483,648 até 2,147,483,647)
                bloco.append(random.randint(-2147483648, 2147483647))
            self.blocos.append(bloco)

class MemoriaCache:
    def __init__(self, nLinhas, linhasPConjunto, nConjuntos):
        self.nLinhas = nLinhas
        self.linhasPConjunto = linhasPConjunto
        self.nConjuntos = nConjuntos
        self.inicializar()

    conjuntos = []
    substituicoes = 0

    def inicializar(self):
        for i in range(self.nConjuntos):
            conjunto = []
            for j in range(self.linhasPConjunto):
                #representacao de uma linha, ja incluindo um contador para as referencias (LFU)
                linha = {'referencias' : 0,'tag' : None, 'bloco': None}
                conjunto.append(linha)
            self.conjuntos.append(conjunto)

    #Funcao para alocar um bloco na cache
    def alocarBloco(self, bloco, iBloco, endereco, tag):
        iConjunto = iBloco % self.nConjuntos
        linhasOcupadas = True
        iLinha = 0
        for linha in self.conjuntos[iConjunto]:
            if linha['tag']!=None: 
                iLinha+=1
                continue
            else:
                linhasOcupadas = False
                linha['referencias']+=1
                linha['tag'] = endereco[0:tag]
                linha['bloco'] = bloco
                return [iConjunto, iLinha]
        #Caso todas as linhas estejam ocupadas, aplicar a substituicao
        if linhasOcupadas: 
            time.sleep(0.1)
            print("A cache está cheia!")
            time.sleep(0.1)
            print("\nAplicando algoritmo de substituição...")
            return self.substituirLinha(bloco, iConjunto, endereco, tag)

    #Funcao para substituir linhas na cache
    def substituirLinha(self, bloco, iConjunto, endereco, tag):
        conjunto = self.conjuntos[iConjunto]
        iLinhaEscolhida = 0
        minReferencia = float('inf')
        for i in range(self.linhasPConjunto):
            if conjunto[i]['referencias'] < minReferencia:
                iLinhaEscolhida = i
                minReferencia = conjunto[i]['referencias']

        linhaEscolhida = conjunto[iLinhaEscolhida]
        linhaEscolhida['referencias'] = 1
        linhaEscolhida['tag'] = endereco[0:tag]
        linhaEscolhida['bloco'] = bloco
        time.sleep(0.1)
        print(f"Linha {iLinhaEscolhida} do conjunto {iConjunto} foi substituida.")
        time.sleep(0.1)
        print("Substituição Completa!\n")
        self.substituicoes+=1
        return [iConjunto, iLinhaEscolhida]
        
    #Funcao que retorna uma palavra se ela estiver presente na cache
    def retornaPalavra(self, iBloco, endereco, iPalavra, tag):
        iConjunto = iBloco % self.nConjuntos
        conjunto = self.conjuntos[iConjunto]
        for i in range(self.linhasPConjunto):
            if conjunto[i]['tag'] == endereco[0:tag]:
                conjunto[i]['referencias'] +=1
                return [iConjunto, i, conjunto[i]['bloco'][iPalavra]]
        return False
    
    #Funcao para exibir na tela as linhas e conjuntos proximos de uma linha acessada
    def mostrar(self, iConjunto, iLinha):
        conjunto = self.conjuntos[iConjunto]
        if(iConjunto>0):
            conjuntoAnt = self.conjuntos[iConjunto-1]
            print(f'\nConjunto {iConjunto-1} (Anterior):')
            for i in range(len(conjuntoAnt)):
                print('-------------------------------------------------------------------------------------------------')
                print(f"               {i}: tag={conjuntoAnt[i]['tag']} bloco={conjuntoAnt[i]['bloco']}")
            print('-------------------------------------------------------------------------------------------------')

        print(f'\nConjunto {iConjunto} (Atual):')
        for i in range(len(conjunto)):
            print('-------------------------------------------------------------------------------------------------')
            if i==iLinha: print(f"LINHA ATUAL -> {i}: tag={conjunto[i]['tag']} bloco={conjunto[i]['bloco']}")
            else: print(f"               {i}: tag={conjunto[i]['tag']} bloco={conjunto[i]['bloco']}")
        print('-------------------------------------------------------------------------------------------------')

        if(iConjunto < len(self.conjuntos)-1):
            conjuntoSuc = self.conjuntos[iConjunto+1]
            print(f'\nConjunto {iConjunto+1} (Seguinte):')
            for i in range(len(conjuntoSuc)):
                print('-------------------------------------------------------------------------------------------------')
                print(f"               {i}: tag={conjuntoSuc[i]['tag']} bloco={conjuntoSuc[i]['bloco']}")
            print('-------------------------------------------------------------------------------------------------')

        print('\n')