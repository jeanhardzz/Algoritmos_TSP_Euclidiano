import numpy as np
import heapq
import networkx as nx

class Bnb:
    g = None
    agente = None

    def __init__(self,g) -> None:
        self.g = g

    
    
    def bound(self,sol_parcial):        
        total = 0
        nos = list(self.g.nodes) 
        for n in nos:
            if n not in sol_parcial:                
                arestas = list(self.g.edges(n,data=True))
                menores = []
                for a in arestas:
                    menores.append(a[2]['peso'])
                menores.sort()                
                total = total + menores[0] + menores[1]
            else:
                index = sol_parcial.index(n)
                if index == 0 or index == len(sol_parcial)-1:                    
                    arestas = list(self.g.edges(n,data=True))
                    menores = []
                    for a in arestas:
                        menores.append(a[2]['peso'])
                    menores.sort()                    
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
                       
                else:                    
                    v1 = self.g[n][sol_parcial[index+1]]   
                    m1 = v1['peso']

                    v2 = self.g[n][sol_parcial[index-1]]   
                    m2 = v2['peso']

                    total = total + m1 + m2                    
        
        total = np.ceil(total / 2)        
        return total
                

    def bnb(self):
        borda = []
        sucesso = []
        heapq.heapify(borda)

        nos = list(self.g.nodes)
        n = len(nos)
        
        nos_explorados = 0
        tamanho_borda = 0
        

        sucesso.append(nos[0])
        
        root = (self.bound(sucesso),1,0,sucesso)

        heapq.heappush(borda,root)

        best = float("inf")

        while len(borda) > 0:
            
            if len(borda) > tamanho_borda:
                tamanho_borda = len(borda)
                
            no = heapq.heappop(borda)
            nos_explorados = nos_explorados + 1            

            estimativa = no[0]
            level = no[1]
            custo = no[2]
            sol = no[3].copy()
            
            if level == n:                
                v = self.g[sol[-1:][0]][sol[0]]
                peso = v['peso']
                possivel_best = custo + peso
                if possivel_best < best:
                    best = possivel_best
                    sucesso = sol.copy()
                    sucesso.append(sol[0])

            else:
                if estimativa < best:                                              
                    for k in nos:
                        if k not in no[3]:                            
                            if len(sol) == 0:
                                peso = 0
                            else:                                
                                v = self.g[sol[-1:][0]][k]
                                peso = v['peso']
                                                        
                            sol_aux = sol.copy()
                            sol_aux.append(k)                            
                            if self.bound(sol_aux) <= best:
                                aux = (self.bound(sol_aux), no[1]+1, custo+peso, sol_aux)                                
                                heapq.heappush(borda,aux)                            
                                                        
        nos = nx.get_node_attributes(self.g,'pos') 
        solucao = []
        for n in sucesso:
            solucao.append(nos[n])

        print("Solucao: ",solucao)                   
        print("Custo da solucao: ",best)     
                








