"""
Word Defender - Lógica principal do jogo
Digite as letras das palavras que caem antes que toquem o solo.

Fluxo do jogo (a cada frame):
  1. processar_eventos() - teclas, fechar janela
  2. atualizar_jogo() - gera palavras, move tudo, verifica colisões
  3. desenhar_tudo() - renderiza a tela
"""

import os
import random

import pygame

from configuracoes import (
    LARGURA_TELA,
    ALTURA_TELA,
    POSICAO_X_CANHAO,
    POSICAO_Y_CANHAO,
    VIDAS_INICIAIS,
    PONTOS_POR_LETRA,
    PONTOS_POR_PALAVRA,
    INTERVALO_NASCIMENTO_PALAVRA,
    MAX_PALAVRAS_TELA,
    MIN_LETRAS_PALAVRA,
    MAX_LETRAS_PALAVRA,
    VELOCIDADE_BASE,
    ACELERACAO_POR_PONTO,
    MULTIPLICADOR_PUNICAO_ERRO,
    TENTATIVAS_POSICAO_LIVRE,
    MARGEM_TELA,
    FPS,
    Cores,
)
from loader_csv import carregar_csv, filtrar_tamanho
from entidades import Palavra, Projetil
from renderizador import Renderizador
from utilidades import letras_sao_iguais


class Jogo:
    """Controla o fluxo principal do Word Defender."""
    
    def __init__(self, caminho_csv=None):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Word Defender - Aula 02")
        self.relogio = pygame.time.Clock()
        
        caminho = caminho_csv or os.path.join(
            os.path.dirname(__file__), 'base_palavras_100_reais_ptbr_en.csv'
        )
        self.banco_palavras = carregar_csv(caminho)
        
        self.palavras_caindo = []
        self.projeteis = []
        self.pontos = 0
        self.vidas = VIDAS_INICIAIS
        self.jogo_encerrado = False
        self.temporizador_nascimento = 0
        self.contador_palavras = 0
        
        self.renderizador = Renderizador(self.tela)
    
    def _obter_palavras_disponiveis(self):
        """Retorna palavras filtradas por tamanho."""
        return filtrar_tamanho(self.banco_palavras, MIN_LETRAS_PALAVRA, MAX_LETRAS_PALAVRA, 'pt_br')
    
    def _encontrar_posicao_livre(self, largura):
        """Encontra uma posição horizontal que não sobreponha outras palavras."""
        intervalos_usados = [(p.x, p.x + p.largura) for p in self.palavras_caindo]
        for _ in range(TENTATIVAS_POSICAO_LIVRE):
            x = random.randint(MARGEM_TELA, LARGURA_TELA - largura - MARGEM_TELA)
            nao_sobrepoe = all(
                x + largura < x_inicio or x > x_fim
                for x_inicio, x_fim in intervalos_usados
            )
            if nao_sobrepoe:
                return x
        return (LARGURA_TELA - largura) // 2
    
    def _escolher_cores_palavra(self):
        """Alterna entre verde e amarelo para variedade visual."""
        cores = [(Cores.PALAVRA_VERDE, Cores.PALAVRA_VERDE_BORDA),
                 (Cores.PALAVRA_AMARELA, Cores.PALAVRA_AMARELA_BORDA)]
        self.contador_palavras += 1
        return cores[self.contador_palavras % 2]
    
    def gerar_nova_palavra(self):
        """Cria uma nova palavra caindo do topo da tela."""
        opcoes = self._obter_palavras_disponiveis()
        if not opcoes or len(self.palavras_caindo) >= MAX_PALAVRAS_TELA:
            return
        
        palavra_escolhida = random.choice(opcoes)
        texto = palavra_escolhida['pt_br']
        velocidade = VELOCIDADE_BASE + self.pontos * ACELERACAO_POR_PONTO
        largura = max(80, len(texto) * 16)
        x = self._encontrar_posicao_livre(largura)
        cor, cor_borda = self._escolher_cores_palavra()
        
        nova_palavra = Palavra(texto, x, 25, velocidade, cor, cor_borda)
        self.palavras_caindo.append(nova_palavra)
    
    def processar_letra_digitada(self, letra):
        """Processa a tecla digitada: acerta letra ou pune com aceleração."""
        if self.jogo_encerrado:
            return
        
        for indice, palavra in enumerate(self.palavras_caindo):
            if palavra.proxima_letra and letras_sao_iguais(letra, palavra.proxima_letra):
                self._acertar_letra(palavra, indice)
                return
        
        self._punir_erro()
    
    def _acertar_letra(self, palavra, indice):
        """Registra acerto, dispara projétil e remove palavra se completou."""
        palavra.remover_primeira_letra()
        self.pontos += PONTOS_POR_LETRA
        
        if palavra.esta_vazia():
            self.pontos += PONTOS_POR_PALAVRA
            self.palavras_caindo.pop(indice)
        
        alvo_x = palavra.x + 10
        alvo_y = palavra.y + palavra.altura / 2
        projetil = Projetil(POSICAO_X_CANHAO, POSICAO_Y_CANHAO, alvo_x, alvo_y)
        self.projeteis.append(projetil)
    
    def _punir_erro(self):
        """Acelera todas as palavras quando o jogador erra."""
        for palavra in self.palavras_caindo:
            palavra.velocidade *= MULTIPLICADOR_PUNICAO_ERRO
    
    def atualizar_jogo(self):
        """Atualiza o estado do jogo (palavras, projéteis, colisões)."""
        if self.jogo_encerrado:
            return
        # Gera novas palavras no intervalo correto
        self.temporizador_nascimento += 1
        if self.temporizador_nascimento >= INTERVALO_NASCIMENTO_PALAVRA:
            self.temporizador_nascimento = 0
            self.gerar_nova_palavra()
        # Move palavras e projéteis
        for palavra in self.palavras_caindo:
            palavra.mover()
        for projetil in self.projeteis[:]:
            if not projetil.mover():
                self.projeteis.remove(projetil)
        # Remove palavras no solo e subtrai vidas
        for palavra in self.palavras_caindo[:]:
            if palavra.tocou_solo():
                self.vidas -= 1
                self.palavras_caindo.remove(palavra)
                if self.vidas <= 0:
                    self.jogo_encerrado = True
    
    def processar_eventos(self):
        """Processa eventos. Retorna False para encerrar o jogo."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                return False
            if evento.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                if evento.key == pygame.K_r and (mods & pygame.KMOD_CTRL):
                    self.reiniciar_jogo()
                elif evento.unicode and not (mods & pygame.KMOD_CTRL):
                    self.processar_letra_digitada(evento.unicode)
        return True
    
    def reiniciar_jogo(self):
        """Reseta o jogo para o estado inicial."""
        self.palavras_caindo.clear()
        self.projeteis.clear()
        self.pontos = 0
        self.vidas = VIDAS_INICIAIS
        self.jogo_encerrado = False
        self.temporizador_nascimento = 0
    
    def executar(self):
        """Loop principal do jogo."""
        executando = True
        while executando:
            executando = self.processar_eventos()
            self.atualizar_jogo()
            self.renderizador.desenhar_tudo(self)
            pygame.display.flip()
            self.relogio.tick(FPS)
        
        pygame.quit()
