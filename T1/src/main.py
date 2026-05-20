# -*- coding: utf-8 -*-
import sys
from collections import deque
from uf import UF

def main():
    # Leitura rápida de toda a entrada padrão
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    # N é o número de pontos
    N = int(input_data[0])
    
    # Lendo as coordenadas dos pontos
    points = []
    idx = 1
    for _ in range(N):
        x = int(input_data[idx])
        y = int(input_data[idx+1])
        points.append((x, y))
        idx += 2
        
    # Deduplicação dos pontos. Pontos repetidos têm distância 0.
    # Usamos dict.fromkeys para manter a ordem de inserção original de forma rápida (C-speed)
    unique_points = list(dict.fromkeys(points))
    num_unique = len(unique_points)
    
    # Se houver 1 ou nenhum ponto único, a MST tem peso 0
    if num_unique <= 1:
        print(0)
        return
        
    # Definição dos limites da grade (conforme restrição: 0 <= x, y <= 1000)
    GRID_SIZE = 1000
    stride = GRID_SIZE + 1
    
    # owner armazena o índice do ponto único mais próximo da célula da grade
    owner = [-1] * (stride * stride)
    # dist armazena a distância mínima até o owner correspondente
    dist = [-1] * (stride * stride)
    
    queue = deque()
    
    # Inicializa a fila da BFS com todos os pontos originais (as origens simultâneas)
    for p_idx, (x, y) in enumerate(unique_points):
        cell_idx = x * stride + y
        owner[cell_idx] = p_idx
        dist[cell_idx] = 0
        queue.append((x, y))
        
    # Executa a BFS Multi-Origem para gerar o diagrama de Voronoi discreto na grade
    while queue:
        x, y = queue.popleft()
        u_idx = x * stride + y
        u_owner = owner[u_idx]
        u_dist = dist[u_idx]
        
        next_dist = u_dist + 1
        
        # Vizinho de cima
        if x > 0:
            n_idx = u_idx - stride
            if owner[n_idx] == -1:
                owner[n_idx] = u_owner
                dist[n_idx] = next_dist
                queue.append((x - 1, y))
                
        # Vizinho de baixo
        if x < GRID_SIZE:
            n_idx = u_idx + stride
            if owner[n_idx] == -1:
                owner[n_idx] = u_owner
                dist[n_idx] = next_dist
                queue.append((x + 1, y))
                
        # Vizinho da esquerda
        if y > 0:
            n_idx = u_idx - 1
            if owner[n_idx] == -1:
                owner[n_idx] = u_owner
                dist[n_idx] = next_dist
                queue.append((x, y - 1))
                
        # Vizinho da direita
        if y < GRID_SIZE:
            n_idx = u_idx + 1
            if owner[n_idx] == -1:
                owner[n_idx] = u_owner
                dist[n_idx] = next_dist
                queue.append((x, y + 1))
                
    # Extração das arestas candidatas conectando regiões vizinhas de donos diferentes
    edges = []
    for x in range(stride):
        row_offset = x * stride
        for y in range(stride):
            u_idx = row_offset + y
            u_owner = owner[u_idx]
            
            # Aresta com o vizinho da direita (se houver dono diferente)
            if y < GRID_SIZE:
                r_idx = u_idx + 1
                r_owner = owner[r_idx]
                if u_owner != r_owner:
                    w = dist[u_idx] + dist[r_idx] + 1
                    edges.append((w, u_owner, r_owner))
                    
            # Aresta com o vizinho de baixo (se houver dono diferente)
            if x < GRID_SIZE:
                b_idx = u_idx + stride
                b_owner = owner[b_idx]
                if u_owner != b_owner:
                    w = dist[u_idx] + dist[b_idx] + 1
                    edges.append((w, u_owner, b_owner))
                    
    # Ordenar arestas pelo peso em ordem crescente (Timsort em C é extremamente rápido)
    edges.sort()
    
    # Algoritmo de Kruskal com a classe UF oficial da base algs4-py
    uf = UF(num_unique)
    mst_weight = 0
    edges_used = 0
    needed_edges = num_unique - 1
    
    for w, u, v in edges:
        if not uf.connected(u, v):
            uf.union(u, v)
            mst_weight += w
            edges_used += 1
            # Para assim que a MST estiver completa (conecta todos os únicos)
            if edges_used == needed_edges:
                break
                
    print(mst_weight)

if __name__ == '__main__':
    main()
