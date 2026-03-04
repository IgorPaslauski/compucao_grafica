"""
Word Defender - Renderizador
Responsável por desenhar todos os elementos na tela.
"""

import pygame

from configuracoes import (
    LARGURA_TELA,
    ALTURA_TELA,
    ALTURA_PLATAFORMA,
    POSICAO_Y_PLATAFORMA,
    POSICAO_X_CANHAO,
    POSICAO_Y_CANHAO,
    VIDAS_INICIAIS,
    Cores,
)
from utilidades import desenhar_gradiente_vertical, desenhar_retangulo_arredondado


class Renderizador:
    """Desenha todos os elementos visuais do jogo."""
    
    def __init__(self, tela):
        self.tela = tela
        self._carregar_fontes()
    
    def _carregar_fontes(self):
        """Carrega as fontes usadas no jogo."""
        try:
            self.fonte_hud = pygame.font.SysFont('segoeui', 20)
            self.fonte_palavra = pygame.font.SysFont('segoeui', 24)
            self.fonte_titulo = pygame.font.SysFont('segoeui', 48)
        except Exception:
            self.fonte_hud = pygame.font.Font(None, 22)
            self.fonte_palavra = pygame.font.Font(None, 26)
            self.fonte_titulo = pygame.font.Font(None, 44)
    
    def desenhar_fundo(self):
        """Fundo com gradiente e grade."""
        retangulo_tela = (0, 0, LARGURA_TELA, ALTURA_TELA)
        desenhar_gradiente_vertical(self.tela, retangulo_tela, Cores.FUNDO_TOPO, Cores.FUNDO_BASE)
        for i in range(0, LARGURA_TELA, 60):
            pygame.draw.line(self.tela, Cores.GRADE, (i, 0), (i, ALTURA_TELA), 1)
        for j in range(0, ALTURA_TELA, 60):
            pygame.draw.line(self.tela, Cores.GRADE, (0, j), (LARGURA_TELA, j), 1)
    
    def desenhar_plataforma(self):
        """Plataforma onde o canhão está apoiado."""
        pygame.draw.rect(
            self.tela, Cores.PLATAFORMA,
            (0, POSICAO_Y_PLATAFORMA, LARGURA_TELA, ALTURA_PLATAFORMA)
        )
        pygame.draw.line(
            self.tela, Cores.PLATAFORMA_BORDA,
            (0, POSICAO_Y_PLATAFORMA), (LARGURA_TELA, POSICAO_Y_PLATAFORMA), 4
        )
    
    def desenhar_canhao(self):
        """Canhão fixo na plataforma."""
        cx, cy = int(POSICAO_X_CANHAO), int(POSICAO_Y_CANHAO)
        # Base
        pygame.draw.rect(self.tela, Cores.CANHAO_BOCA, (cx - 32, cy + 5, 64, 20), border_radius=4)
        # Corpo
        pygame.draw.circle(self.tela, Cores.CANHAO, (cx, cy - 2), 20)
        pygame.draw.circle(self.tela, (80, 95, 120), (cx, cy - 2), 20, 2)
        # Tubo
        pygame.draw.rect(self.tela, Cores.CANHAO_BOCA, (cx - 5, cy - 42, 10, 42), border_radius=2)
    
    def desenhar_palavras(self, palavras):
        """Desenha todas as palavras na tela."""
        for palavra in palavras:
            retangulo = (int(palavra.x), int(palavra.y), int(palavra.largura), int(palavra.altura))
            desenhar_retangulo_arredondado(
                self.tela, retangulo, palavra.cor,
                raio=10, cor_borda=palavra.cor_borda, espessura_borda=2
            )
            texto = self.fonte_palavra.render(palavra.texto, True, Cores.TEXTO_PALAVRA)
            pos_x = palavra.x + (palavra.largura - texto.get_width()) / 2
            pos_y = palavra.y + (palavra.altura - texto.get_height()) / 2
            self.tela.blit(texto, (pos_x, pos_y))
    
    def desenhar_projeteis(self, projeteis):
        """Desenha todos os projéteis em voo."""
        for projetil in projeteis:
            px, py = int(projetil.x), int(projetil.y)
            pygame.draw.circle(self.tela, Cores.PROJETIL_BRILHO, (px, py), 10)
            pygame.draw.circle(self.tela, Cores.PROJETIL, (px, py), 6)
    
    def desenhar_hud(self, pontos, vidas):
        """Painel de informações (pontos e vidas)."""
        largura_painel, altura_painel = 200, 85
        painel = pygame.Surface((largura_painel, altura_painel))
        painel.set_alpha(220)
        painel.fill(Cores.PAINEL_FUNDO)
        pygame.draw.rect(painel, Cores.PAINEL_BORDA, (0, 0, largura_painel, altura_painel), 2, border_radius=10)
        self.tela.blit(painel, (12, 12))
        
        cor_label = Cores.HUD_LABEL
        self.tela.blit(self.fonte_hud.render("PONTOS", True, cor_label), (22, 18))
        self.tela.blit(self.fonte_hud.render(str(pontos), True, Cores.HUD), (22, 38))
        self.tela.blit(self.fonte_hud.render("VIDAS", True, cor_label), (22, 58))
        texto_vidas = "♥" * vidas + "♡" * (VIDAS_INICIAIS - vidas)
        self.tela.blit(self.fonte_hud.render(texto_vidas, True, Cores.HUD_VIDA), (22, 68))
        
        self.tela.blit(
            self.fonte_hud.render("Digite as letras!", True, cor_label),
            (LARGURA_TELA - 160, 12)
        )
    
    def desenhar_tela_game_over(self, pontos):
        """Tela de game over com pontuação final."""
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
        overlay.set_alpha(200)
        overlay.fill(Cores.FUNDO_TOPO)
        self.tela.blit(overlay, (0, 0))
        
        largura, altura = 380, 170
        x = (LARGURA_TELA - largura) // 2
        y = (ALTURA_TELA - altura) // 2
        pygame.draw.rect(self.tela, Cores.PAINEL_BORDA, (x, y, largura, altura), border_radius=18)
        pygame.draw.rect(self.tela, Cores.PROJETIL, (x, y, largura, altura), 3, border_radius=18)
        
        titulo = self.fonte_titulo.render("GAME OVER", True, Cores.PROJETIL)
        texto_pontos = self.fonte_hud.render(f"Pontuação: {pontos}", True, Cores.HUD)
        texto_reiniciar = self.fonte_hud.render(
            "[ Ctrl+R ] Reiniciar  |  [ ESC ] Sair", True, Cores.HUD_LABEL
        )
        
        self.tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, y + 30))
        self.tela.blit(texto_pontos, (LARGURA_TELA // 2 - texto_pontos.get_width() // 2, y + 85))
        self.tela.blit(texto_reiniciar, (LARGURA_TELA // 2 - texto_reiniciar.get_width() // 2, y + 115))
    
    def desenhar_tudo(self, jogo):
        """Desenha toda a cena a partir do estado do jogo."""
        self.desenhar_fundo()
        self.desenhar_plataforma()
        self.desenhar_canhao()
        self.desenhar_palavras(jogo.palavras_caindo)
        self.desenhar_projeteis(jogo.projeteis)
        self.desenhar_hud(jogo.pontos, jogo.vidas)
        if jogo.jogo_encerrado:
            self.desenhar_tela_game_over(jogo.pontos)
