# Grid MST - Trabalho Prático 1 (Unidade 3)

Este repositório contém a resolução do problema **Grid MST** da plataforma Kattis, como parte do Trabalho Prático 1 da disciplina de Resolução de Problemas com Grafos.

## Integrantes do Grupo
- **[João Victor Lira Saraiva Leão]**
- **[Cauan Gomes dos Santos Barbosa]**
- **[Isadora Ferreira Neves Rios]**

*Professor Orientador:* Prof. Me Ricardo Carubbi

---

## Detalhes do Problema
- **Nome do Problema**: [Grid MST](https://open.kattis.com/problems/gridmst)
- **ID do Problema**: `gridmst`
- **Linguagem Utilizada**: Python (versão 3.8+)
- **Estruturas Implementadas**: Union-Find / DSU (Disjoint Set Union) personalizada, BFS Multi-Origem (Multi-Source BFS) e Algoritmo de Kruskal.

---

## Modelagem e Abordagem

O problema consiste em encontrar a Árvore Geradora Mínima (MST) de um conjunto de até $100.000$ pontos em uma grade 2D de tamanho máximo de $1000 \times 1000$, sob a métrica de distância de Manhattan:
$$\text{dist}(P_1, P_2) = |x_1 - x_2| + |y_1 - y_2|$$

### O Desafio
Um grafo completo contendo todas as arestas possíveis entre os $N$ pontos possui $\mathcal{O}(N^2)$ arestas. Com $N = 100.000$, teríamos $10^{10}$ arestas, tornando algoritmos tradicionais de MST (como Prim ou Kruskal puros sobre o grafo completo) totalmente inviáveis devido ao estouro de tempo e memória.

### A Estratégia de Resolução

1. **Remoção de Duplicatas (Deduplicação)**:
   Se houver pontos com coordenadas idênticas, a distância entre eles é $0$. Eles podem ser unidos imediatamente com custo 0. Portanto, filtramos as duplicatas para trabalhar apenas com os $K$ pontos únicos, mantendo a corretude matemática da MST.

2. **Busca em Largura Multi-Origem (Multi-Source BFS)**:
   Como a grade é pequena ($1001 \times 1001$ células) e as distâncias são dadas em Manhattan, podemos projetar um diagrama de Voronoi discreto na grade.
   - Inicializamos uma fila com as coordenadas de todos os pontos únicos (as origens).
   - Executamos uma BFS simultânea a partir de todas as origens.
   - Para cada célula $(x, y)$ da grade, determinamos o ponto de origem mais próximo (`owner`) e a distância até ele (`dist`).
   - Isso é feito de forma supereficiente em tempo linear em relação à área da grade: $\mathcal{O}(\text{Tamanho da Grade}) = \mathcal{O}(10^6)$ operações.

3. **Extração de Arestas Candidatas**:
   Com o diagrama de Voronoi calculado, as únicas arestas que podem pertencer à MST são aquelas que conectam origens cujas regiões de Voronoi são vizinhas na grade.
   - Percorremos todas as células da grade e comparamos o dono de cada célula com os donos de seus vizinhos adjacentes (direita e de baixo).
   - Se os donos forem diferentes (digamos, origens $u$ e $v$), criamos uma aresta candidata entre $u$ e $v$ com peso dado por:
     $$\text{peso} = \text{dist}[u] + \text{dist}[v] + 1$$
   - Isso reduz o conjunto de arestas de $10^{10}$ para no máximo $2 \times 10^6$ arestas candidatas!

4. **Algoritmo de Kruskal**:
   - Ordenamos as arestas candidatas extraídas pelo peso.
   - Usamos o **Union-Find / DSU** otimizado para unir as componentes.
   - A construção termina imediatamente quando tivermos adicionado exatamente $K - 1$ arestas à árvore geradora.

---

## Análise de Complexidade

- **Tempo**: $\mathcal{O}(V_{\text{grid}} + E_{\text{cand}} \log E_{\text{cand}})$ onde:
  - $V_{\text{grid}}$ é a área da grade ($1001 \times 1001 \approx 10^6$ células). A BFS multi-origem e a extração de arestas percorrem a grade um número constante de vezes.
  - $E_{\text{cand}}$ é o número de arestas candidatas (no máximo $2 \times 10^6$). O termo dominante é a ordenação das arestas, que leva cerca de **1.5 segundos** em Python padrão.
  - O DSU com compressão de caminhos e união por rank garante que as operações de `find` e `union` no Kruskal rodem em tempo praticamente constante $\mathcal{O}(\alpha(N))$.
- **Espaço**: $\mathcal{O}(V_{\text{grid}})$ para armazenar a grade de distâncias e proprietários, o que consome aproximadamente ~24 MB de memória, muito abaixo do limite de 1024 MB do Kattis.

## Estrutura do Repositório

```text
T1/
├── README.md
├── src/
│   ├── main.py
│   └── uf.py
├── evidencias/
│   └── accepted.png
├── apresentacao/
│   └── apresentacao.pdf
└── dados/
    ├── 1.in
    ├── 1.ans
    ├── 2.in
    ├── 2.ans
    ├── caso_medio.txt
    └── caso_limite.txt
```

---

## Casos de Teste Disponíveis

Para facilitar a validação local da corretude e da performance da solução, o diretório `T1/dados/` contém os arquivos oficiais fornecidos pela plataforma Kattis e alguns casos adicionais:

1. **`1.in` / `1.ans`**: O primeiro caso de teste oficial do enunciado ($N = 4$ pontos, saída esperada: `3`).
2. **`2.in` / `2.ans`**: O segundo caso de teste oficial do enunciado ($N = 5$ pontos com duplicatas, saída esperada: `14`).
3. **`caso_limite.txt`**: Um caso mínimo limite ($N = 2$) com a maior distância de Manhattan possível na grade de $[0, 1000] \times [0, 1000]$ (saída esperada: `2000`).
4. **`caso_medio.txt`**: Um caso médio ($N = 20$ pontos) contendo múltiplos pontos sobrepostos e distâncias variadas para estressar a deduplicação de vértices (saída esperada: `3997`).

---

## Como Executar a Solução

Para executar o programa com qualquer caso de teste da pasta de dados:

1. Navegue até o diretório `T1/src/`:
   ```bash
   cd T1/src
   ```

2. Execute o código redirecionando os dados do arquivo para a entrada padrão:

   * **No Linux / macOS / Git Bash (Bash padrão):**
     ```bash
     python main.py < ../dados/1.in
     python main.py < ../dados/2.in
     python main.py < ../dados/caso_limite.txt
     python main.py < ../dados/caso_medio.txt
     ```

   * **No Windows (PowerShell):**
     ```powershell
     Get-Content ../dados/1.in | python main.py
     Get-Content ../dados/2.in | python main.py
     Get-Content ../dados/caso_limite.txt | python main.py
     Get-Content ../dados/caso_medio.txt | python main.py
     ```

---

## Visualizador Interativo (Interface Gráfica Opcional)

Para tornar a apresentação do trabalho mais amigável e demonstrar de forma clara o funcionamento prático do algoritmo para o professor e alunos ouvintes, desenvolvemos um **Visualizador Interativo** localizado em `T1/src/visualizador.html`.

Esta interface gráfica é **totalmente opcional** e portátil, não interferindo na execução do script terminal (`main.py`) que calcula a MST para a plataforma Kattis.

### Principais Recursos:
- **Portabilidade Total**: Desenvolvido puramente em HTML5 Canvas, CSS moderno (com design dark mode e glassmorphism) e JavaScript. Roda em qualquer navegador (Chrome, Edge, Firefox, Safari) sem necessidade de servidores locais ou de instalar pacotes Python extras (como Pygame ou Tkinter).
- **Animação da BFS**: Veja o grid se preencher gradativamente a partir das origens com cores neon distintas, evidenciando a criação das células de Voronoi e o cálculo de distâncias.
- **Animação do Kruskal e DSU**: Acompanhe o processamento de cada aresta candidata em tempo real. Arestas aceitas brilham em azul ciano, enquanto arestas rejeitadas por criarem ciclos piscam em vermelho.
- **Totalmente Interativo**: Clique diretamente no Canvas para adicionar pontos manuais, limpe a tela, regule a velocidade da simulação usando o Slider ou carregue conjuntos aleatórios.
- **Suporte a Drag-and-Drop**: Arraste qualquer arquivo `.in` ou `.txt` oficial de entrada da plataforma para dentro da interface para vê-lo carregar e resolver o problema visualmente na hora!

### Como Executar o Visualizador:
Basta navegar até a pasta `T1/src/` e dar **dois cliques** no arquivo `visualizador.html` usando o Explorer/Finder do seu sistema operacional, ou executar no terminal a partir da raiz do repositório:

* **No Windows (PowerShell):**
  ```powershell
  Start-Process T1/src/visualizador.html
  ```
* **No Linux / macOS (Terminal):**
  ```bash
  open T1/src/visualizador.html
  ```

---

## Evidência de Accepted
*(A imagem que comprova a submissão com status **Accepted** na plataforma Kattis estará localizada na pasta `T1/evidencias/accepted.png`)*

![Accepted](evidencias/accepted.png)
