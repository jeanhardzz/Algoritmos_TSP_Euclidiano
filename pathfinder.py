import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from bnb import Bnb


class Pathfinder:
    alg = None
    instancia = None
    metrica = None
    g = nx.Graph() #grafo
    pos = None #auxiliar para desenhar o grafico

    def __init__(self) -> None:
        pass
    
    def Leitura(self,alg,instancia,metrica):        
        self.alg = alg
        self.instancia = int(instancia)
        self.metrica = metrica

    def CriarGrafo(self):

        #Criando vertices usando pontos aleatorios do plano

        pontos = []

        for i in range(2**self.instancia):
            p = (random.randint(0,1000),random.randint(0,1000))
            pontos.append(p)

        #print("Pontos:\n", pontos)
        
        #Criando arestas entre todos os vertices (v1-v2-distancia)
        arestas = []
        
        for i in range(len(pontos)):
            for j in range(i,len(pontos)):
                if i != j:
                    e = (i,j,self.Distancia(pontos[i],pontos[j]))
                    arestas.append(e) 
        
        #print("\nArestas:\n",arestas)

        for i in range(len(arestas)):
            self.g.add_edge(pontos[arestas[i][0]],pontos[arestas[i][1]], peso=arestas[i][2])

        self.pos = {point: point for point in pontos}      
        print(self.g)
        
        

    
    def Distancia(self,p1,p2):
        p = np.array(p1)
        q = np.array(p2) 
        d = 0

        if self.metrica == "euc":                   
            d = np.linalg.norm(p-q)            

        if self.metrica == "man":
            d = np.linalg.norm(p-q, ord=1)

        return round(d,4)
    
    def ShowGrafo(self):
        # you want your own layout
        # pos = nx.spring_layout(G)
        

        # add axis
        fig, ax = plt.subplots()
        nx.draw(self.g, pos=self.pos, node_color='k', ax=ax)
        nx.draw(self.g, pos=self.pos, node_size=1500, ax=ax)  # draw nodes and edges
        nx.draw_networkx_labels(self.g, pos=self.pos)  # draw node labels/names
        # draw edge weights
        labels = nx.get_edge_attributes(self.g, 'peso')
        nx.draw_networkx_edge_labels(self.g, self.pos, edge_labels=labels, ax=ax)
        plt.axis("on")
        ax.set_xlim(0, 1001)
        ax.set_ylim(0,1001)
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        plt.show()
    
    def Busca(self):
        if self.alg == "bnb":
            self.BranchAndBound()
        if self.alg == "tat":
            self.TwiceAroundTheTree()
        if self.alg == "chr":
            self.Christofides()

    def BranchAndBound(self):
        busca = Bnb(self.g)
        busca.bnb_my()
    
    def TwiceAroundTheTree(self):
        pass

    def Christofides(self):
        pass