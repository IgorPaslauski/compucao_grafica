from graficos_math import (
    Ponto2D, Ponto3D,
    multiplicar_matriz_2x2, multiplicar_matriz_3x3, multiplicar_matriz_4x4,
    comprimento_segmento_2d, comprimento_segmento_3d,
    interseccao_segmentos_2d,
    imprimir_matriz
)


def main():
    print("=" * 60)
    print("BIBLIOTECA DE FUNÇÕES MATEMÁTICAS - COMPUTAÇÃO GRÁFICA")
    print("=" * 60)

    print("\n1. PONTOS 2D E 3D")
    print("-" * 40)
    p2d = Ponto2D(3, 4)
    q2d = Ponto2D(0, 0)
    print(f"Ponto 2D: {p2d}")
    print(f"Distancia ate origem: {p2d.distancia(q2d):.2f}")
    
    p3d = Ponto3D(1, 2, 2)
    q3d = Ponto3D(0, 0, 0)
    print(f"\nPonto 3D: {p3d}")
    print(f"Distancia ate origem: {p3d.distancia(q3d):.2f}")
    
    print("\n2. MULTIPLICAÇÃO DE MATRIZES")
    print("-" * 40)
    
    rot90 = [
        [0, -1],
        [1,  0]
    ]
    identidade2 = [
        [1, 0],
        [0, 1]
    ]
    m2 = multiplicar_matriz_2x2(rot90, identidade2)
    print("Matriz 2x2 - Rotação 90° × Identidade:")
    imprimir_matriz(m2, "Resultado")
    
    a3 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    b3 = [
        [9, 8, 7],
        [6, 5, 4],
        [3, 2, 1]
    ]
    m3 = multiplicar_matriz_3x3(a3, b3)
    print("Matriz 3x3:")
    imprimir_matriz(m3, "A × B")
    
    trans = [
        [1, 0, 0, 5],
        [0, 1, 0, 3],
        [0, 0, 1, 2],
        [0, 0, 0, 1]
    ]
    identidade4 = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    m4 = multiplicar_matriz_4x4(trans, identidade4)
    print("Matriz 4x4 - Translação (5,3,2) × Identidade:")
    imprimir_matriz(m4, "Resultado")
    
    print("\n3. COMPRIMENTO DE SEGMENTOS")
    print("-" * 40)
    seg2d = comprimento_segmento_2d(Ponto2D(0, 0), Ponto2D(3, 4))
    print(f"Segmento 2D de (0,0) a (3,4): {seg2d:.2f}")
    
    seg3d = comprimento_segmento_3d((0, 0, 0), (1, 2, 2))
    print(f"Segmento 3D de (0,0,0) a (1,2,2): {seg3d:.2f}")
    
    print("\n4. INTERSEÇÃO ENTRE SEGMENTOS")
    print("-" * 40)
    
    s1_a = Ponto2D(0, 0)
    s1_b = Ponto2D(4, 4)
    s2_a = Ponto2D(0, 4)
    s2_b = Ponto2D(4, 0)
    inter = interseccao_segmentos_2d(s1_a, s1_b, s2_a, s2_b)
    print(f"Segmento 1: {s1_a} -> {s1_b}")
    print(f"Segmento 2: {s2_a} -> {s2_b}")
    print(f"Interseção: {inter}")
    
    s3_a = Ponto2D(0, 0)
    s3_b = Ponto2D(2, 2)
    s4_a = Ponto2D(1, 0)
    s4_b = Ponto2D(3, 2)
    inter2 = interseccao_segmentos_2d(s3_a, s3_b, s4_a, s4_b)
    print(f"\nSegmento 3: {s3_a} -> {s3_b}")
    print(f"Segmento 4: {s4_a} -> {s4_b}")
    print(f"Interseção: {inter2}")
    
    print("\n" + "=" * 60)
    print("Fim da demonstração.")
    print("=" * 60)


if __name__ == "__main__":
    main()
