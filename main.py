import sys
import time
#Modulo das memorias
import memorias
#Modulo de utilidades
import util

#Menu principal do programa
print()
print('TRABALHO DE ARQUITETURA E ORGANIZAÇÃO DE COMPUTADORES'.center(68, '-'))
print('SIMULADOR DE MEMÓRIA CACHE COM MAPEAMENTO ASSOCIATIVO POR CONJUNTO'.center(68))
print('Alunos: Mateus Fuchs e Pedro Camillo Miranda'.center(68))
print('Versão usada: Python 3.12.3'.center(68))
print('--------------------------------------------------------------------\n')
time.sleep(0.8)

print('LER ARQUIVO DE ENTRADA'.center(68,'-'))

print("\nA primeira linha do arquivo deve conter o tamanho da MP em KBs (Max = 256).")
print("A segunda linha deve conter a quantidade de palavras por bloco na MP (2, 4 ou 8).")
print("A terceira linha deve conter o tamanho da cache em KBs (Max = 32).")
print("A quarta linha deve conter o número de linhas por conjunto da cache (Min = 2).")

#Declaracao e inicializacao de variaveis
while True:
    try:
        print("\nDigite ou cole o caminho absoluto do arquivo de entrada:\n(por exemplo: C:\\Users\\user\\Desktop\\entrada.txt)")
        caminho = input()
        tamanhoMP, palavrasPBloco, tamanhoCache, linhasPConjunto = map(int, util.lerArquivo(caminho)) #Ler arquivo de entradas

        #Verificando se as entradas estao dentro do limite
        if int(tamanhoMP) > 256 or not util.isPot2(tamanhoMP): 
            print("\nO tamanho da memória principal está fora dos limites ou não é potência de 2.")
            continue

        if int(palavrasPBloco) > 8 or int(palavrasPBloco) == 1 or not util.isPot2(palavrasPBloco): 
            print("\nA quantidade de palavras por bloco está fora dos limites ou não é potência de 2.")
            continue

        if int(tamanhoCache) > 32 or not util.isPot2(tamanhoCache): 
            print("\nO tamanho da memória cache está fora dos limites ou não é potência de 2.")
            continue

        if int(linhasPConjunto) <2 or not util.isPot2(linhasPConjunto): 
            print("\nA quantidade de linhas por conjunto está fora dos limites ou não é potência de 2.")
            continue

        break
    except(FileNotFoundError):
        print("\nArquivo não encontrado!\nVerifique se o caminho está correto e tente novamente.")
    except(ValueError) as e:
        print("\nAlgum valor do arquivo de entrada está incorreto!")
        print(f"Mensagem de erro: {str(e)}")

tamanho_palavra = 4 #Bytes
nPalavrasMP = (tamanhoMP * 1024)//tamanho_palavra #Quantidade de palavras na memoria principal
nPalavrasCache = (tamanhoCache * 1024)//tamanho_palavra #Quantidade de palavras na memoria cache
nBlocos = nPalavrasMP//palavrasPBloco #Quantidade de blocos na memoria principal
nLinhas = nPalavrasCache//palavrasPBloco #Quantidade de linhas na memoria cache
nConjuntos = nLinhas//linhasPConjunto #Quantidade de conjuntos na memoria cache
if nConjuntos == 0:
    print("\nA quantidade de linhas por conjunto excede o limite de quantidade de linhas/2.")
    sys.exit()

w, d, s, tag = util.calcularValores(palavrasPBloco, nBlocos, nConjuntos)
tamanhoEndereco = s+w

mp = memorias.MemoriaPrincipal(nPalavrasMP, palavrasPBloco, nBlocos) #Instancia da classe MemoriaPrincipal do arquivo "memorias"
cache = memorias.MemoriaCache(nLinhas, linhasPConjunto, nConjuntos) #Instancia da classe MemoriaCache do arquivo "memorias"

acessos = acertos = falhas = 0

#Funcao para mostrar informacoes uteis sobre as memorias
def mostrarInfo():
    print()
    print("INFORMAÇÕES SOBRE AS MEMÓRIAS".center(40, '-'))
    print(f'Tamanho da Palavra = {tamanho_palavra} Bytes ({tamanho_palavra*8} bits)')
    print(f'Tamanho do endereço da MP = {tamanhoEndereco} bits.')
    print(f'w={w} d={d} s={s} tag={tag}')
    print('----------------------------------------')
    print("MEMÓRIA PRINCIPAL".center(40))
    print(f"Tamanho: {tamanhoMP}KB\nPalavras: {nPalavrasMP}\nPalavras por Bloco: {palavrasPBloco}\nBlocos: {nBlocos}".center(40))
    print('----------------------------------------')
    print("MEMÓRIA CACHE".center(40))
    print(f"Tamanho: {tamanhoCache}KB\nLinhas: {nLinhas}\nLinhas por Conjunto: {linhasPConjunto}\nConjuntos: {nConjuntos}".center(40))
    print('----------------------------------------')

time.sleep(0.3)
mostrarInfo()

#Funcao para buscar endereco na cache, e se nao achar, busca na MP.
#Depois disso, aloca o bloco enderecado na cache, e se a cache estiver cheia, aplica o algoritmo LFU.
def buscarEndereco(endereco, omitir=False):
    global acessos, falhas, acertos #Para fazer operacoes de escrita em atributos globais
    iBloco = util.binParaDec(endereco[0:s])
    iPalavra = util.binParaDec(endereco[s:])
    
    result = cache.retornaPalavra(iBloco, endereco, iPalavra, tag)
    time.sleep(0.1)
    if(result):
        iConjunto, iLinha, palavra = result
        print("\nACERTO")
        print(f"\nO endereço '{endereco}' foi encontrado na cache!")
        time.sleep(0.1)
        print(f"A palavra encontrada foi '{palavra}', na linha {iLinha} do conjunto {iConjunto}.")
        acertos+=1
        acessos+=1
        if(not omitir):
            time.sleep(0.4)
            cache.mostrar(iConjunto, iLinha)
        else: print('\n-------------------------------------------------------------------------------------------------')

    else:
        print("\nFALHA")
        print(f"\nO endereço '{endereco}' não foi encontrado na cache.")
        time.sleep(0.1)
        print("Buscando bloco na memória principal...")
        falhas+=1
        acessos+=1
        bloco = mp.blocos[iBloco]
        palavra = bloco[iPalavra]
        time.sleep(0.1)
        print(f"\nO endereço '{endereco}' foi encontrado na memória principal.")
        time.sleep(0.1)
        print(f"A palavra encontrada foi '{palavra}'.")
        time.sleep(0.1)
        print('\nAlocando bloco na cache...')
        iConjunto, iLinha = cache.alocarBloco(bloco, iBloco, endereco, tag)
        time.sleep(0.1)
        print(f'Bloco alocado na cache, na linha {iLinha} do conjunto {iConjunto}.')
        if(not omitir):
            time.sleep(0.4)
            cache.mostrar(iConjunto, iLinha)
        else: print('\n-------------------------------------------------------------------------------------------------')

while True:
    print('\nDigite o código da opção desejada.')
    print('\t1: Ler arquivo de endereços da memória principal a serem acessados.')
    print('\t2: Escolher um endereço da memória principal para ser acessado.')
    print('\t3: Visualizar informações sobre as memórias.')
    print('\t4: Encerrar o Programa e visualizar dados.')
    escolha = int(input())
    if(escolha == 4): 
        time.sleep(0.1)
        print(f"\nNo total, houveram {acessos} acessos, sendo {acertos} acertos e {falhas} falhas.")
        time.sleep(0.1)
        print(f"Taxa de acertos = {(acertos/acessos*100):.2f}%")
        time.sleep(0.1)
        print(f"Taxa de falhas = {(falhas/acessos*100):.2f}%")
        time.sleep(0.1)
        print(f"Número de substituições = {cache.substituicoes}")            
        time.sleep(0.3)
        print("\nAbaixo está a configuração final da cache, mostrando os conjuntos que tem pelo menos uma linha não vazia:\n")
        time.sleep(1)
        for i in range(cache.nConjuntos):
            conjunto = cache.conjuntos[i]
            conjuntoPreenchido = any(linha['tag']!=None for linha in conjunto)
            if not conjuntoPreenchido: continue
            print(f"Conjunto {i}:")
            for j in range(cache.linhasPConjunto):
                print('-------------------------------------------------------------------------------------------------')
                print(f"               {j}: tag={conjunto[j]['tag']} bloco={conjunto[j]['bloco']}")
            print('-------------------------------------------------------------------------------------------------')

        sys.exit()

    if(escolha == 3):
        mostrarInfo()

    if(escolha == 2):
        endereco = input("\nDigite um endereço válido da MP para ser acessado (Em binário, com " + str(tamanhoEndereco)+" bits): ")
        if util.enderecoValido(endereco, tamanhoEndereco): buscarEndereco(endereco)
        else:
            print("Endereço no formato inválido!")

    if(escolha == 1):
        while True:    
            try:
                print(f"\nDigite ou cole o caminho absoluto do arquivo de endereços ({tamanhoEndereco} bits cada):")
                caminho = input()
                enderecos = util.lerArquivo(caminho)
                break
            except(FileNotFoundError):
                print("\nArquivo não encontrado!\nVerifique se o caminho está correto e tente novamente.")
            

        enderecosValidos = True
        for endereco in enderecos:
            if not util.enderecoValido(endereco, tamanhoEndereco):
                enderecosValidos = False
                print(f"Endereço '{endereco}' está em um formato inválido!")
                break
        if not enderecosValidos: continue

        print('\nComo deseja que a cache seja mostrada?')
        print('Digite o código da opção desejada.')
        print('\t1: Mostrar a cache para cada acesso de endereço (pode ficar muito extenso)')
        print('\t2: Mostrar apenas ao encerrar o programa.')
        escolha = int(input())

        if escolha==1:
            for endereco in enderecos:
                buscarEndereco(endereco)

        if escolha==2:
            for endereco in enderecos:
                buscarEndereco(endereco, omitir=True)
    

