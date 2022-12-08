import sys
from pathfinder import Pathfinder

def main():
    lst = sys.argv[1:]
    
    tsp = Pathfinder()
    
    # Algoritmo / instancia / métrica
    # Algoritmos: bnb - tat - chr
    # Instancia: 4 - 5 - 6 - 7 - 8 - 9 - 10
    # Metrica: euc - man

    tsp.Leitura(lst[0],lst[1],lst[2]) 
    tsp.CriarGrafo()   
    tsp.Busca()
    #tsp.ShowGrafo()

if __name__ == "__main__":
    main()