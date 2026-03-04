"""
Word Defender - Entidades do jogo
Classes que representam os elementos visuais e interativos.
"""

import math

from configuracoes import POSICAO_Y_PLATAFORMA


class Palavra:
    """Uma palavra que cai pela tela. O jogador deve digitar as letras para destruí-la."""
    
    LARGURA_MINIMA = 80
    LARGURA_POR_LETRA = 16
    ALTURA = 44
    
    def __init__(self, texto, x, y, velocidade, cor, cor_borda):
        self.texto = texto
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.cor = cor
        self.cor_borda = cor_borda
        self._atualizar_dimensoes()
    
    def _atualizar_dimensoes(self):
        """Recalcula largura baseada no texto atual."""
        minimo = 60 if self.texto else self.LARGURA_MINIMA
        self.largura = max(minimo, len(self.texto) * self.LARGURA_POR_LETRA)
        self.altura = self.ALTURA
    
    @property
    def proxima_letra(self):
        """Retorna a primeira letra que deve ser digitada."""
        return self.texto[0] if self.texto else None
    
    def remover_primeira_letra(self):
        """Remove a primeira letra (quando o jogador acerta)."""
        if self.texto:
            self.texto = self.texto[1:]
            self._atualizar_dimensoes()
    
    def mover(self):
        """Move a palavra para baixo."""
        self.y += self.velocidade
    
    def tocou_solo(self):
        """Verifica se a palavra chegou à plataforma."""
        return self.y + self.altura >= POSICAO_Y_PLATAFORMA
    
    def esta_vazia(self):
        """Indica se todas as letras foram acertadas."""
        return not self.texto


class Projetil:
    """Um projétil que voa do canhão em direção à palavra."""
    
    VELOCIDADE = 28
    RAIO_ALCANCE = 18
    
    def __init__(self, origem_x, origem_y, alvo_x, alvo_y):
        self.x = origem_x
        self.y = origem_y
        self.alvo_x = alvo_x
        self.alvo_y = alvo_y
        self._calcular_direcao()
        self.ativo = True
    
    def _calcular_direcao(self):
        """Calcula a direção normalizada do movimento."""
        dx = self.alvo_x - self.x
        dy = self.alvo_y - self.y
        distancia = math.hypot(dx, dy) or 1
        fator = self.VELOCIDADE / distancia
        self.velocidade_x = dx * fator
        self.velocidade_y = dy * fator
    
    def mover(self):
        """Move o projétil e verifica se chegou ao alvo."""
        self.x += self.velocidade_x
        self.y += self.velocidade_y
        distancia_ao_alvo = math.hypot(self.alvo_x - self.x, self.alvo_y - self.y)
        if distancia_ao_alvo < self.RAIO_ALCANCE:
            self.ativo = False
        return self.ativo
