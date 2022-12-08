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
        print(nos)

        #nx.draw(mst,with_labels=True, font_weight='bold')
        #plt.show()

        self.BuscaPreOrder(mst,inicial)
        self.visitados.append(inicial)

        print(self.visitados)

        solucao = []
        custo = 0
        for i in range(len(self.visitados)):
            if i+1 < len(self.visitados):
                v = self.g[self.visitados[i]][self.visitados[i+1]]
                custo = custo + v['peso']           

            solucao.append(nos[self.visitados[i]])
        
        print("Solucao: ",solucao)                
        #Custo de memoria usado para fins comparativos será a quantidade de vertices armazenados.
        #O algoritmo de Prim armazena cada vertice uma unica vez, entao seu custo para fins
        # comparativos de memoria é a quantidade de vertices total.
        print("\nMemoria: ", len(nos))
        print("Custo da solucao: ",custo)

        """
        print("Solucao: ",sucesso)
        print("\nCusto da solucao: ",best)
        print("Estimativa da solucao otima: ",solucao_otima)
        print("Quantidade maxima de nos armazenados no heap: ", tamanho_borda)
        print("Quantidade de nos expandidos:",nos_explorados)
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
        

 