# -*- coding: utf-8 -*-

# José Fernando Garcia Junior email: jf.junior18@hotmail.com
from sys import exit
import networkx as nx
import numpy as np
from numpy import Inf
from heapq import heapify
from heapq import heappop as pop
from heapq import heappush as push

def main():
    nome = raw_input('Digite o caminho e o nome da matriz: ')
    grafo = gera_grafo(nome)
    op = int(raw_input('Digite:\n1 - Para extrair a MDT\n2 - Para extrair a MDT com grupos\n'))
    if op == 2:
        numero_raizes = int(raw_input('Qual o número de sementes? '))
        nome = nome[0:(len(nome)-4)]+'_NumSem'+str(numero_raizes)+'.png'        
    else:
        numero_raizes = 1
        nome = nome[0:(len(nome)-3)] + 'png'
    if numero_raizes == 0:
        print 'Valor não é valido'        
        exit()
    raizes = []    
    for i in range(numero_raizes):
        raizes.append(int(raw_input('numero (nome) da semente? ')))        
    arvore = dijkstra(grafo,raizes)
    arvore = nx.to_agraph(arvore)
    arvore.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')
    arvore.draw(nome)
    print 'Grafo gerado em: ', nome    
    

def dijkstra(g,raizes):
    '''
    Parametro: g, representando um grafo
    Retorno: arvore, arvore de caminhos minimos
    Função: Retorna a SPT (Shortest Path Tree) ou arvore de caminhos minimos
    do grafo recebido como parametro
    '''
    lista_prioridades = [(Inf,i) for i in range(int(nx.number_of_nodes(g)))]
    # lista_prioridades transformar em heap
    heapify(lista_prioridades) 
    # inserir nó 0 (assumindo que o nó 0 é a raiz) com prioridade 0
    for i in raizes:    
        push(lista_prioridades, (0, i))
    #representação: posterior é o indice e anterior é o valor armazenado
    anteriores = [None for i in range(int(nx.number_of_nodes(g)))]
    # cria um dicionário que indica se um vertice v está no heap (se está no heap, ainda não foi processado)
    inheap = { v: True for v in g.nodes() }
    # cria um dicionário de pesos
    pesos = { v: float('inf') for v in g.nodes() }
    for i in raizes:    
        pesos[i] = 0;
 
    while lista_prioridades:
        no = pop(lista_prioridades)
        # testa se no ainda não foi removido do heap anteriormente (como não podemos atualizar os pesos, um nó pode repetir)
        if (inheap[no[1]]):
            inheap[no[1]] = False # foi retirado do heap pela primeira vez
        else:
            continue # já foi retirado do heap antes (repetido)

        #Seleciona cada vizinho
        for i in nx.neighbors(g,no[1]):
            #verifica se vizinho esta na lista de prioridades            
            if (inheap[i]): 
                #verifica se um no é anterior do outro   
                peso = g.get_edge_data(no[1],i)['weight'] + no[0]
                if peso < pesos[i]:
                    push(lista_prioridades, (peso, i))
                    anteriores[i] = no[1]
                    pesos[i] = peso
                
    arestas = [(i,anteriores[i]) for i in range(len(anteriores))]
    nos = []    
    for i in raizes:
        if (i,None) in arestas:
            nos.append(i)
			#Remove arestas que ligam um grafo a None
            arestas.remove((i,None))
    #arestas.pop(0) #Descarta o primeiro pois é a aresta da raiz, que não se liga com ninguém (0,None)
    g.clear()
    g.add_edges_from(arestas)
	#Coloca os nós que ficaram sozinhos
    g.add_nodes_from(nos)
    return g
    
def gera_grafo(nome_arquivo):
    '''
    Parametro: nome_arquivo, tem nome do arquivo que possui a matriz de adjacencia
    Retorno: retorna o grafo correspondente à matriz de adjacencia
    Função: obter um grafo apartir da matriz de adjacencia
    '''
    #cria um grafo vazio
    g = nx.Graph() 
    #ler matriz de adjacencia
    matriz_adj = np.loadtxt(nome_arquivo)
    #Obter coordenadas em que o peso é diferente de zero
    linha, coluna = np.where(matriz_adj > 0)
    #Combina a linha com a coluna, formando as arestas.
    aresta = zip(linha,coluna)
    #coloca peso nas arestas
    aresta_peso = [(u,v,{'weight':matriz_adj[u][v]})for u,v in aresta]
    #Preenche o grafo com as arestas e vertices    
    g.add_edges_from(aresta_peso)
    #retorna o grafo com os pesos
    return g

if __name__=="__main__":
    main()
