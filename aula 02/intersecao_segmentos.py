"""
Aula 02 - Interseção de Segmentos de Reta em 2D
Programa interativo: defina 4 pontos com o mouse (P1, P2, P3, P4)
para dois segmentos e visualize a interseção.
"""

import pygame
import math

# Configurações
LARGURA, ALTURA = 800, 600
COR_FUNDO = (240, 242, 245)
COR_SEG1, COR_SEG2 = (41, 128, 185), (231, 76, 60)
COR_PONTO, COR_INTERSECAO = (44, 62, 80), (39, 174, 96)


def distancia(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def produto_vetorial(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]


def verificar_interseccao(p1, p2, p3, p4):
    """
    Verifica se os segmentos P1-P2 e P3-P4 se intersectam.
    Paramétrico: P1 + t*(P2-P1) = P3 + s*(P4-P3)
    t, s em [0,1] => interseção dentro dos segmentos.
    """
    d1 = (p2[0] - p1[0], p2[1] - p1[1])  # vetor P2-P1
    d2 = (p4[0] - p3[0], p4[1] - p3[1])  # vetor P4-P3
    d3 = (p1[0] - p3[0], p1[1] - p3[1])  # vetor P1-P3
    
    cross = produto_vetorial(d1, d2)
    
    if abs(cross) < 1e-10:
        if abs(produto_vetorial(d3, d2)) < 1e-10:
            return ('colineares', None)
        return ('paralelos', None)
    
    # t = -(d3×d2)/(d1×d2)  e  s = -(d3×d1)/(d1×d2)
    t = -produto_vetorial(d3, d2) / cross
    s = -produto_vetorial(d3, d1) / cross
    
    if 0 <= t <= 1 and 0 <= s <= 1:
        ponto = (p1[0] + t * d1[0], p1[1] + t * d1[1])
        return ('interseccao', ponto)
    return ('fora_intervalo', None)


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Aula 02 - Interseção de Segmentos")
    relogio = pygame.time.Clock()
    fonte = pygame.font.Font(None, 24)
    
    pontos = []
    rodando = True
    
    while rodando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                rodando = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                pontos = []
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and len(pontos) < 4:
                pontos.append(e.pos)
        
        # Cálculos
        compr1 = distancia(pontos[0], pontos[1]) if len(pontos) >= 2 else None
        compr2 = distancia(pontos[2], pontos[3]) if len(pontos) >= 4 else None
        situacao, ponto_int = (None, None)
        if len(pontos) >= 4:
            situacao, ponto_int = verificar_interseccao(*pontos[:4])
        
        # Desenho
        tela.fill(COR_FUNDO)
        
        # Grid simples
        for i in range(0, LARGURA, 40):
            pygame.draw.line(tela, (200, 200, 205), (i, 0), (i, ALTURA), 1)
        for j in range(0, ALTURA, 40):
            pygame.draw.line(tela, (200, 200, 205), (0, j), (LARGURA, j), 1)
        
        # Segmentos
        if len(pontos) >= 2:
            pygame.draw.line(tela, COR_SEG1, pontos[0], pontos[1], 3)
        if len(pontos) >= 4:
            pygame.draw.line(tela, COR_SEG2, pontos[2], pontos[3], 3)
        
        # Pontos
        for p in pontos:
            pygame.draw.circle(tela, COR_PONTO, (int(p[0]), int(p[1])), 6)
        
        # Interseção
        if ponto_int:
            pygame.draw.circle(tela, COR_INTERSECAO,
                (int(ponto_int[0]), int(ponto_int[1])), 10)
        
        # Info
        y = 10
        if compr1: tela.blit(fonte.render(f"Seg 1: {compr1:.1f} px", True, (0,0,0)), (10, y)); y += 22
        if compr2: tela.blit(fonte.render(f"Seg 2: {compr2:.1f} px", True, (0,0,0)), (10, y)); y += 22
        if situacao:
            msg = {'interseccao':'Interseção', 'paralelos':'Paralelos', 
                   'colineares':'Colineares', 'fora_intervalo':'Cruzam fora'}[situacao]
            tela.blit(fonte.render(msg, True, (0,0,0)), (10, y))
        tela.blit(fonte.render("4 cliques | R: Reset | ESC: Sair", True, (100,100,100)), (10, ALTURA-25))
        
        pygame.display.flip()
        relogio.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()
