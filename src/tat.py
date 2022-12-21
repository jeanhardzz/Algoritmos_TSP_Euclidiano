import networkx as nx
import matplotlib.pyplot as plt

class Tat:
    g = None    
    visitados = []
    def __init__(self,g) -> None:
        self.g = g
    
    def tat(self):                        
                
        mst = nx.minimum_spanning_tree(self.g, weight='peso', algorithm='prim')
        inicial = list(self.g.nodes())[0]
        nos = nx.get_node_attributes(self.g,'pos')

        self.BuscaPreOrder(mst,inicial)
        self.visitados.append(inicial)


        solucao = []
        custo = 0
        for i in range(len(self.visitados)):
            if i+1 < len(self.visitados):
                v = self.g[self.visitados[i]][self.visitados[i+1]]
                custo = custo + v['peso']           

            solucao.append(nos[self.visitados[i]])
        
        print("Solucao: ",solucao)                                
        print("Custo da solucao: ",custo)

        

    def BuscaPreOrder(self,mst, no):
                
        self.visitados.append(no)        
        
        for filho in mst[no]:
            if filho in self.visitados:
                continue
            else:                
                self.BuscaPreOrder(mst, filho)
        

 