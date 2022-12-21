import networkx as nx
import matplotlib.pyplot as plt

class Chr:
    g = None    
    visitados = []

    def __init__(self,g) -> None:
        self.g = g
    
    def Chr(self):                        

        #Encontrando a arvore geradora minima   
        mst = nx.minimum_spanning_tree(self.g, weight='peso', algorithm='prim')


        #Pegando os vertices de grau impar da mst
        vertices_grau_impar = []
        
        for vertice in mst.nodes():              
            grau = mst.degree(vertice)            
                
            if grau % 2 == 1:
                vertices_grau_impar.append(vertice)        
                        
        
        #Construindo o grafo induzido a partir dos vertices de grau impar
        g_induzido = nx.induced_subgraph(self.g, vertices_grau_impar)        
        

        #Encontrando o menor matching perfeito do grafo induzido com relação ao peso
        matching_perfeito = nx.algorithms.matching.min_weight_matching(g_induzido,weight='peso')        


        #Adicionando as arestas do matching no multigrafo
        mult = nx.MultiGraph()
        for u,v in mst.edges:
            mult.add_edge(u,v)
        
        for u,v in matching_perfeito:
            mult.add_edge(u,v)
            

        #Encontrando o caminho euleriano
        ec = nx.eulerian_path(mult)        
        custo = 0
        solucao = []
        nos = nx.get_node_attributes(self.g,'pos') 
        for u,v in ec:            
            v = self.g[u][v]
            custo = custo + v['peso']
            solucao.append(nos[u])
        
        solucao.append(nos[0])

        print("Solucao: ",solucao)                               
        print("Custo da solucao: ",custo)
        
    
        