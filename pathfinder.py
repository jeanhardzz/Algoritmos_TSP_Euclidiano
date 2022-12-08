import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import time

from bnb import Bnb
from tat import Tat




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

        #print("Pontos:\n", pontos)
        
        #Criando arestas entre todos os vertices (v1-v2-distancia)
        arestas = []
        
        for i in range(len(pontos)):
            for j in range(i,len(pontos)):
                if i != j:
                    e = (i,j,self.Distancia(pontos[i],pontos[j]))
                    arestas.append(e) 
        
        #print("\nArestas:\n",arestas)

        for i, (x, y) in enumerate(pontos):
            self.g.add_node(i, pos=(x,y))

        for i in range(len(arestas)):
            self.g.add_edge(arestas[i][0],arestas[i][1], peso=arestas[i][2])
        
        #print(self.g)
                
        
    
        
        

    
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
        busca.bnb_my()
        fim = time.time()
        
        solucao_otima = self.EstimativaCustoOtimo()
        print("Estimativa da solucao otima: ",solucao_otima)
        print("Tempo: ",round(fim - inicio,4))
        #busca.bnb_tsp()
    
    def TwiceAroundTheTree(self):        
        busca = Tat(self.g)

        inicio = time.time()
        busca.tat()
        fim = time.time()

        solucao_otima = self.EstimativaCustoOtimo()
        print("Estimativa da solucao otima: ",solucao_otima)
        print("Tempo: ",round(fim - inicio,4))
        
    def Christofides(self):
        pass

    def EstimativaCustoOtimo(self):
        sol_parcial = []
        #print("Solução parcial", sol_parcial)
        total = 0
        nos = list(self.g.nodes) 
        for n in nos:
            if n not in sol_parcial:
                #print(n, " nao esta na parcial:")
                arestas = list(self.g.edges(n,data=True))
                menores = []
                for a in arestas:
                    menores.append(a[2]['peso'])
                menores.sort()
                #print(menores[0] ,"-", menores[1])
                total = total + menores[0] + menores[1]
            else:
                index = sol_parcial.index(n)
                if index == 0 or index == len(sol_parcial)-1:
                    #print(n, " esta na parcial - BORDA")
                    arestas = list(self.g.edges(n,data=True))
                    menores = []
                    for a in arestas:
                        menores.append(a[2]['peso'])
                    menores.sort()
                    #print(menores)
                    m1 = menores[0]
                    m2 = menores[1]
                    if len(sol_parcial)>1:
                        if index == 0:
                            v = self.g[n][sol_parcial[index+1]]
                            if v['peso'] != m1 and v['peso'] != m2:
                                if m1<m2:
                                    m2 = v['peso']
                                else:
                                    m1 = v['peso']
                        if index == len(sol_parcial)-1:
                            v = self.g[n][sol_parcial[index-1]]
                            if v['peso'] != m1 and v['peso'] != m2:
                                if m1<m2:
                                    m2 = v['peso']
                                else:
                                    m1 = v['peso']                        
                    total = total + m1 + m2
                    #print(m1,"-",m2)
                       
                else:
                    #print(n, " esta na parcial - DENTRO")
                    #print(sol_parcial[index+1])
                    v1 = self.g[n][sol_parcial[index+1]]   
                    m1 = v1['peso']

                    v2 = self.g[n][sol_parcial[index-1]]   
                    m2 = v2['peso']

                    total = total + m1 + m2
                    #print(m1,"-",m2) 
        
        total = np.ceil(total / 2)
        #print(total)
        return total