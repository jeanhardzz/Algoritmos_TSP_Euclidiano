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

        #nx.draw(mst,with_labels=True, font_weight='bold')
        #plt.show()

        #Pegando os vertices de grau impar da mst
        vertices_grau_impar = []
        
        for vertice in mst.nodes():              
            grau = mst.degree(vertice)
            #print("v ",vertice, " grau: ",grau)      
                
            if grau % 2 == 1:
                vertices_grau_impar.append(vertice)

        # Imprime a lista de vértices de grau ímpar
        #print(vertices_grau_impar)
                        
        
        #Construindo o grafo induzido a partir dos vertices de grau impar
        g_induzido = nx.induced_subgraph(self.g, vertices_grau_impar)        
        

        #Encontrando o menor matching perfeito do grafo induzido com relação ao peso
        matching_perfeito = nx.algorithms.matching.min_weight_matching(g_induzido,weight='peso')
        #print(matching_perfeito)

        #Adicionando as arestas do matching na arvore
        for u,v in matching_perfeito:
            mst.add_edge(u,v)
        
        #nx.draw(mst,with_labels=True, font_weight='bold')
        #plt.show()

        #Fazendo a busca do caminho da nova arvore
        inicial = list(self.g.nodes())[0]
        nos = nx.get_node_attributes(self.g,'pos')      
        self.BuscaPreOrder(mst,inicial)
        self.visitados.append(inicial)

        #print(self.visitados)
        solucao = []
        custo = 0
        for i in range(len(self.visitados)):
            if i+1 < len(self.visitados):
                v = self.g[self.visitados[i]][self.visitados[i+1]]
                custo = custo + v['peso']           

            solucao.append(nos[self.visitados[i]])
        
        print("Solucao: ",solucao)                
        #Não sei o custo de memoria
        #print("\nMemoria: ", len(nos))
        print("\nCusto da solucao: ",custo)
        
        """
        pos=nx.get_node_attributes(g_induzido,'pos')               
        nx.draw(g_induzido,pos,with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g_induzido,'peso')
        nx.draw_networkx_edge_labels(g_induzido,pos,edge_labels=labels)
        plt.show()
        """
    
    def BuscaPreOrder(self,mst, no):
        
        # Adiciona o vértice atual à lista de vértices visitados
        self.visitados.append(no)

        # Para cada filho do vértice atual
        for filho in mst[no]:

            # Se o filho já foi visitado, ignore
            if filho in self.visitados:
                continue
            else:
                # Senão, recursivamente percorra a árvore a partir do filho
                self.BuscaPreOrder(mst, filho)
        

        