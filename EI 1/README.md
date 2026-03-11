# Biblioteca de Funções Matemáticas para Computação Gráfica

Trabalho acadêmico de Computação Gráfica — implementação de funções matemáticas essenciais para manipulação de gráficos computacionais.

## Estrutura do Projeto

```
EI 1/
├── graficos_math.py    # Biblioteca principal
├── exemplo_uso.py      # Exemplo de demonstração
├── teste_graficos_math.py  # Testes unitários
└── README.md           # Este arquivo
```

## Requisitos

- Python 3.6 ou superior
- Nenhuma dependência externa (apenas biblioteca padrão)

## Como Executar

### Exemplo de uso
```bash
python exemplo_uso.py
```

### Testes
```bash
python teste_graficos_math.py
```
Ou com pytest:
```bash
pip install pytest
python -m pytest teste_graficos_math.py -v
```

## Funcionalidades Implementadas

### 1. Ponto 2D e Ponto 3D

- **`Ponto2D(x, y)`**: Representa um ponto no plano bidimensional.
- **`Ponto3D(x, y, z)`**: Representa um ponto no espaço tridimensional.

Métodos disponíveis: `distancia_ate()`, `subtrair()`, `tupla()`.

### 2. Multiplicação de Matrizes

- **`multiplicar_matriz_2x2(a, b)`**: Multiplicação de matrizes 2×2  
  - Usada em transformações 2D (rotação, escala).

- **`multiplicar_matriz_3x3(a, b)`**: Multiplicação de matrizes 3×3  
  - Usada em transformações 3D sem translação.

- **`multiplicar_matriz_4x4(a, b)`**: Multiplicação de matrizes 4×4  
  - Usada em coordenadas homogêneas para rotação, translação e escala 3D.

### 3. Comprimento de Segmentos de Reta

- **`comprimento_segmento_2d(p1, p2)`**: Comprimento no plano (distância euclidiana).
- **`comprimento_segmento_3d(p1, p2)`**: Comprimento no espaço 3D.

Fórmula: \( d = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2 [+ (z_2-z_1)^2]} \)

### 4. Interseção entre Segmentos

- **`interseccao_segmentos_2d(a1, a2, b1, b2)`**: Retorna o ponto de interseção entre os segmentos (a1→a2) e (b1→b2), ou `None` se não houver interseção.

Algoritmo baseado em orientação (produto vetorial 2D) para detectar cruzamento e em parametrização para calcular o ponto exato.

## Pontos para a Apresentação

1. **Pontos**: Estrutura simples para coordenadas; distância com fórmula euclidiana.
2. **Matrizes**: Fórmula C[i][j] = Σ A[i][k] × B[k][j]; importância em transformações.
3. **Comprimento**: Uso direto da distância euclidiana entre extremos.
4. **Interseção**: Uso de orientação (esquerda/direita) e parametrização para o cálculo do ponto.

## Autor

Trabalho individual — Computação Gráfica.
