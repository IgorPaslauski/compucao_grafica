"""
Aula 02 - Transformações Geométricas 2D - Polígono Interativo
Clique para adicionar vértices. ENTER para fechar (mín. 3 pontos).
Exibe o centro geométrico (centroide) do polígono.
"""

import pygame

# Configurações
LARGURA, ALTURA = 800, 600
COR_FUNDO = (248, 249, 250)
COR_POLIGONO = (52, 73, 94)
COR_VERTICE = (44, 62, 80)
COR_CENTRO = (231, 76, 60)
COR_PREVIEW = (189, 195, 199)


def centro_geometrico(pontos):
    """Centroide: média das coordenadas dos vértices."""
    if len(pontos) < 2:
        return None
    n = len(pontos)
    return (sum(p[0] for p in pontos)/n, sum(p[1] for p in pontos)/n)


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Aula 02 - Polígono - Centro Geométrico")
    relogio = pygame.time.Clock()
    fonte = pygame.font.Font(None, 24)
    
    pontos = []
    finalizado = False
    rodando = True
    
    while rodando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                rodando = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    pontos, finalizado = [], False
                elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if not finalizado and len(pontos) >= 3:
                        finalizado = True
                    elif finalizado:
                        pontos, finalizado = [], False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and not finalizado:
                pontos.append(e.pos)
        
        centro = centro_geometrico(pontos) if finalizado and pontos else None
        mouse = pygame.mouse.get_pos()
        
        # Desenho
        tela.fill(COR_FUNDO)
        
        for x in range(0, LARGURA, 40):
            pygame.draw.line(tela, (220, 223, 227), (x, 0), (x, ALTURA), 1)
        for y in range(0, ALTURA, 40):
            pygame.draw.line(tela, (220, 223, 227), (0, y), (LARGURA, y), 1)
        
        # Polígono
        if len(pontos) >= 2:
            if not finalizado:
                for i in range(len(pontos)-1):
                    pygame.draw.line(tela, COR_PREVIEW, pontos[i], pontos[i+1], 2)
                if len(pontos) >= 1:
                    pygame.draw.line(tela, COR_PREVIEW, pontos[-1], mouse, 2)
            elif len(pontos) >= 3:
                pygame.draw.polygon(tela, (200, 210, 215), pontos)
                pygame.draw.polygon(tela, COR_POLIGONO, pontos, 3)
        
        for p in pontos:
            pygame.draw.circle(tela, COR_VERTICE, (int(p[0]), int(p[1])), 6)
        
        if centro:
            pygame.draw.circle(tela, COR_CENTRO, (int(centro[0]), int(centro[1])), 12)
            pygame.draw.circle(tela, (255,255,255), (int(centro[0]), int(centro[1])), 12, 2)
        
        # Info
        tela.blit(fonte.render(f"Vértices: {len(pontos)}", True, (0,0,0)), (10, 10))
        if centro and finalizado:
            tela.blit(fonte.render(f"Centro: ({centro[0]:.1f}, {centro[1]:.1f})", True, (0,0,0)), (10, 32))
        if not finalizado and len(pontos) >= 3:
            tela.blit(fonte.render("ENTER: fechar polígono", True, (39, 174, 96)), (10, ALTURA-50))
        tela.blit(fonte.render("Clique: vértice | ENTER: fechar | R: reset | ESC: sair", True, (100,100,100)), (10, ALTURA-25))
        
        pygame.display.flip()
        relogio.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()
