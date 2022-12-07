import numpy as np
import heapq

class Bnb:
    g = None
    agente = None

    def __init__(self,g) -> None:
        self.g = g

    
    
    def bound(self,sol_parcial):
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
        
        """
        for (u, v, wt) in self.g.edges.data('peso'):
            print(u,"-",v," = ",wt)
        """
                    
                    
                
       

        #print(nx.all_neighbors(g,1))

    def bnb_my(self):
        borda = []
        sucesso = []
        heapq.heapify(borda)

        nos = list(self.g.nodes)
        n = len(nos)
        
        nos_explorados = 0

        sucesso.append(nos[0])
        root = (self.bound(sucesso),1,0,sucesso)

        heapq.heappush(borda,root)

        best = float("inf")

        while len(borda) > 0:
            
            no = heapq.heappop(borda)
            print("olhando no: ",no)

            estimativa = no[0]
            level = no[1]
            custo = no[2]
            sol = no[3].copy()
            
            if level == n:
                #print("solução viavel",no)
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
                            #print("vertice ",k)
                            if len(sol) == 0:
                                peso = 0
                            else:                                
                                v = self.g[sol[-1:][0]][k]
                                peso = v['peso']
                                                        
                            sol_aux = sol.copy()
                            sol_aux.append(k)
                            #print(self.bound(sol_aux))
                            if self.bound(sol_aux) < best:
                                aux = (self.bound(sol_aux), no[1]+1, custo+peso, sol_aux)
                                #print("add: ",aux)
                                heapq.heappush(borda,aux)
                                nos_explorados = nos_explorados + 1
                                #print("borda: ",borda)                            
                            
        print(best)
        print(sucesso)
        print(nos_explorados)
                









    def bnb_tsp(self):
        cont = 0
        sol = []
        fila = []
        heapq.heapify(fila)

        nos = list(self.g.nodes)
        n = len(nos) 
        #print(nos)

        root = (self.bound(sol),0,0,sol) #(bound,level,custo,parcial)
        
        heapq.heappush(fila,root)
        best = float("inf")
        sucesso = []
        
        #print(fila)
        while len(fila)>0:
            print("loop")
            no = heapq.heappop(fila)
            sol = no[3]
            #print("entrei while")
            #print(no)
            if no[1] > n:
                #print("if 1")
                if best > no[2]:
                    #print("sucesso")
                    best = no[2]
                    sucesso = no[3]
            elif no[0] < best:
                #print("elif 1")
                if no[1] < n:
                    #print("\t if 1")
                    for k in nos:
                        #print("\t for")
                        if k not in no[3]:
                            #print("\t if 2")
                            sol2 = sol.copy()
                            sol2.append(k)
                            if self.bound(sol2) < best:
                                #print("\t if 3")
                                if len(sol) == 0:
                                    peso = 0
                                else:
                                    #print("sol maior q 1 ",sol[-1:][0])
                                    a = self.g[sol[-1:][0]][k]
                                    peso = a['peso']
                                aux = (self.bound(sol2), no[1]+1, no[2]+peso, sol2)
                                #print(aux)
                                heapq.heappush(fila,aux)
                                cont = cont + 1
                else:
                    #print("else 1")
                    if len(sol) != 0:
                        sol3 = sol.copy()
                        sol3.append(sol[0])
                        #print(sol3)
                        if self.bound(sol3) < best:
                            #print("else if 2")
                            if len(sol) == 0:
                                peso = 0
                            else:
                                a = self.g[sol[-1:][0]][sol[0]]
                                peso = a['peso']
                            #print("segundo bound")
                            aux = (self.bound(sol3), no[1]+1, no[2] + peso, sol3)
                            #print(aux)
                            heapq.heappush(fila,aux)
                            cont = cont + 1
        
        print(best)
        print(sucesso)
        print(cont)
        """
        print(self.bound(sol))

        sol.append(nos[0])
        sol.append(nos[1])
        sol.append(nos[2])
        
        print(self.bound(sol))
        """