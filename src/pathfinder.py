import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import tracemalloc

from bnb import Bnb
from tat import Tat
from chr import Chr




class Pathfinder:
    alg = None
    instancia = None
    metrica = None
    g = nx.Graph() #grafo    

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
        
        #Criando arestas entre todos os vertices (v1-v2-distancia)
        arestas = []
        
        for i in range(len(pontos)):
            for j in range(i,len(pontos)):
                if i != j:
                    e = (i,j,self.Distancia(pontos[i],pontos[j]))
                    arestas.append(e)                 

        for i, (x, y) in enumerate(pontos):
            self.g.add_node(i, pos=(x,y))

        for i in range(len(arestas)):
            self.g.add_edge(arestas[i][0],arestas[i][1], peso=arestas[i][2])
                  
        
    
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
        pos=nx.get_node_attributes(self.g,'pos')               
        nx.draw(self.g,pos,with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(self.g,'peso')
        nx.draw_networkx_edge_labels(self.g,pos,edge_labels=labels)
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

        inicio = time.time()
        tracemalloc.start()
        busca.bnb()
        memoria = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        fim = time.time()

        print("Memoria: ",memoria[1])
        print("Tempo: ",round(fim - inicio,4))
        
        
    
    def TwiceAroundTheTree(self):        
        busca = Tat(self.g)

        inicio = time.time()
        tracemalloc.start()
        busca.tat()
        memoria = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        fim = time.time()
                
        
        print("Memoria: ",memoria[1])
        print("Tempo: ",round(fim - inicio,4))
        
        
    def Christofides(self):
        busca = Chr(self.g)

        inicio = time.time()
        tracemalloc.start()
        busca.Chr()
        memoria = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        fim = time.time()
         
        print("Memoria: ",memoria[1])
        print("Tempo: ",round(fim - inicio,4))
       