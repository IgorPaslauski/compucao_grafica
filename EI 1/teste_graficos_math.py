import math
from graficos_math import (
    Ponto2D, Ponto3D,
    multiplicar_matriz_2x2, multiplicar_matriz_3x3, multiplicar_matriz_4x4,
    comprimento_segmento_2d, comprimento_segmento_3d,
    interseccao_segmentos_2d
)

def test_ponto2d_distancia():
    p = Ponto2D(0, 0)
    q = Ponto2D(3, 4)
    assert p.distancia(q) == 5.0


def test_ponto3d_distancia():
    p = Ponto3D(0, 0, 0)
    q = Ponto3D(1, 0, 0)
    assert p.distancia(q) == 1.0
    p2 = Ponto3D(1, 2, 2)
    assert math.isclose(p.distancia(p2), 3.0)


def test_matriz_2x2():
    a = [[1, 0], [0, 1]]
    b = [[2, 3], [4, 5]]
    r = multiplicar_matriz_2x2(a, b)
    assert r == [[2, 3], [4, 5]]


def test_matriz_3x3():
    a = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    b = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    r = multiplicar_matriz_3x3(a, b)
    assert r == b


def test_matriz_4x4():
    a = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    b = [[1, 0, 0, 5], [0, 1, 0, 3], [0, 0, 1, 2], [0, 0, 0, 1]]
    r = multiplicar_matriz_4x4(a, b)
    assert r == b


def test_comprimento_segmento_2d():
    assert comprimento_segmento_2d((0, 0), (3, 4)) == 5.0
    assert comprimento_segmento_2d(Ponto2D(0, 0), Ponto2D(1, 0)) == 1.0


def test_comprimento_segmento_3d():
    assert comprimento_segmento_3d((0, 0, 0), (1, 0, 0)) == 1.0
    assert math.isclose(comprimento_segmento_3d((0, 0, 0), (1, 2, 2)), 3.0)


def test_interseccao_cruzamento():
    inter = interseccao_segmentos_2d(
        (0, 0), (4, 4),
        (0, 4), (4, 0)
    )
    assert inter is not None
    assert abs(inter.x - 2) < 1e-6 and abs(inter.y - 2) < 1e-6


def test_interseccao_paralelos():
    inter = interseccao_segmentos_2d(
        (0, 0), (2, 2),
        (1, 0), (3, 2)
    )
    assert inter is None


def test_interseccao_vertice_comum():
    inter = interseccao_segmentos_2d(
        (0, 0), (2, 2),
        (2, 2), (4, 0)
    )
    assert inter is not None
    assert inter.x == 2 and inter.y == 2


if __name__ == "__main__":
    test_ponto2d_distancia()
    test_ponto3d_distancia()
    test_matriz_2x2()
    test_matriz_3x3()
    test_matriz_4x4()
    test_comprimento_segmento_2d()
    test_comprimento_segmento_3d()
    test_interseccao_cruzamento()
    test_interseccao_paralelos()
    test_interseccao_vertice_comum()
    print("Todos os testes passaram!")
