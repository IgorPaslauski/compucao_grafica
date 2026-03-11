"""
Curvas de Bézier Dinâmicas - Pygame
Clique para adicionar pontos | Arraste para mover | Clique dir: remover
Tecla D: visualização De Casteljau | Tecla R: limpar

Referência: AZEVEDO, Eduardo. Computação gráfica: geração de imagens.
            Rio de Janeiro: Campos, 2003. (Seção 3.1.7)
"""

import pygame
import math

# Configurações da janela e parâmetros
LARGURA, ALTURA = 800, 600
RAIO_CLIQUE = 18
NUM_SEGMENTOS = 50


def ponto_bezier(pontos, t):
    """Calcula um ponto B(t) na Curva de Bézier usando polinômios de Bernstein."""
    if len(pontos) <= 1:
        return pontos[0] if pontos else (0, 0)
    x = y = 0.0
    grau = len(pontos) - 1
    for i in range(len(pontos)):
        peso = math.comb(grau, i) * (1 - t) ** (grau - i) * t ** i
        x += peso * pontos[i][0]
        y += peso * pontos[i][1]
    return (x, y)


def calcular_pontos_curva(pontos, num_segmentos):
    """Calcula os pontos intermediários da Curva de Bézier para desenho.
    Retorna lista de coordenadas (x, y) ao longo da curva."""
    return [ponto_bezier(pontos, i / num_segmentos) for i in range(num_segmentos + 1)]


def de_casteljau(pontos, t):
    """Algoritmo de De Casteljau - retorna (B(t), níveis) para visualização."""
    if len(pontos) < 2:
        return (pontos[0] if pontos else (0, 0)), []
    atual = list(pontos)
    niveis = [list(pontos)]
    for _ in range(len(pontos) - 1):
        atual = [((1 - t) * atual[i][0] + t * atual[i + 1][0],
                  (1 - t) * atual[i][1] + t * atual[i + 1][1])
                 for i in range(len(atual) - 1)]
        niveis.append(atual)
    return (atual[0], niveis)


def ponto_proximo(pontos, pos):
    """Retorna o índice do ponto de controle mais próximo da posição do mouse."""
    if not pontos:
        return -1
    i = min(range(len(pontos)), key=lambda j: math.dist(pos, pontos[j]))
    return i if math.dist(pos, pontos[i]) < RAIO_CLIQUE else -1

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Curvas de Bézier | Computação Gráfica")
    pontos, arras = [], -1
    modo_casteljau, t_param = False, 0.5
    clock = pygame.time.Clock()

    while True:
        # Atualiza parâmetro t na animação De Casteljau
        if modo_casteljau and len(pontos) >= 3:
            t_param = (t_param + 0.006) % 1.0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    i = ponto_proximo(pontos, e.pos)
                    arras = i if i >= 0 else arras
                    if i < 0:
                        pontos.append(e.pos)
                elif e.button == 3 and pontos:
                    pontos.pop()
                    arras = -1
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                arras = -1
            if e.type == pygame.MOUSEMOTION and 0 <= arras < len(pontos):
                pontos[arras] = e.pos
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    pontos.clear()
                    arras = -1
                elif e.key == pygame.K_d:
                    modo_casteljau = not modo_casteljau

        tela.fill((22, 26, 34))

        # Desenha polígono de controle (linhas entre pontos)
        if len(pontos) >= 2:
            for i in range(len(pontos) - 1):
                pygame.draw.aaline(tela, (70, 90, 115), (int(pontos[i][0]), int(pontos[i][1])),
                                  (int(pontos[i + 1][0]), int(pontos[i + 1][1])))
            # Modo De Casteljau ou desenho normal
            if modo_casteljau and len(pontos) >= 3:
                b, niveis = de_casteljau(pontos, t_param)
                for k, nv in enumerate(niveis[:-1]):
                    cor = (min(255, 90 + k * 45), min(255, 130 + k * 35), 215)
                    for j in range(len(nv) - 1):
                        a = (int(nv[j][0]), int(nv[j][1]))
                        a2 = (int(nv[j + 1][0]), int(nv[j + 1][1]))
                        pygame.draw.aaline(tela, cor, a, a2)
                pt_b = (int(b[0]), int(b[1]))
                pygame.draw.circle(tela, (255, 210, 80), pt_b, 10)
                pygame.draw.circle(tela, (255, 255, 255), pt_b, 10, 2)
                pc = [(int(p[0]), int(p[1])) for p in calcular_pontos_curva(pontos, NUM_SEGMENTOS)]
                corte = int(t_param * NUM_SEGMENTOS) + 1
                if corte > 1:
                    pygame.draw.aalines(tela, (255, 210, 80), False, pc[:corte])
                if corte < len(pc):
                    pygame.draw.aalines(tela, (70, 95, 85), False, pc[corte - 1:])
            else:
                # Dois pontos: linha reta | Três ou mais: Curva de Bézier
                if len(pontos) == 2:
                    pygame.draw.aaline(tela, (100, 200, 220), (int(pontos[0][0]), int(pontos[0][1])),
                                      (int(pontos[1][0]), int(pontos[1][1])))
                else:
                    pc = [(int(p[0]), int(p[1])) for p in calcular_pontos_curva(pontos, NUM_SEGMENTOS)]
                    pygame.draw.aalines(tela, (120, 220, 150), False, pc)

        # Desenha pontos de controle
        for i, p in enumerate(pontos):
            pt = (int(p[0]), int(p[1]))
            pygame.draw.circle(tela, (255, 100, 100) if i == arras else (255, 175, 90), pt, 6)
            pygame.draw.circle(tela, (255, 255, 255) if i == arras else (55, 70, 95), pt, 6, 1)

        f = pygame.font.Font(None, 20)
        info = f"Pontos: {len(pontos)} | R: limpar | D: De Casteljau"
        if modo_casteljau and len(pontos) >= 3:
            info += " (ativo)"
        tela.blit(f.render(info, True, (190, 200, 220)), (10, 10))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
