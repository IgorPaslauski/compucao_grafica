"""
Aula 02 - Carregador de palavras do CSV
Formato esperado: pt-br, len-pt-br, en, len-en
- len-pt-br e len-en validam que o tamanho armazenado confere com o texto
"""

import csv
import os


def carregar_csv(caminho):
    """Carrega palavras do CSV. Retorna lista de dict com pt_br, en, len_pt_br, len_en."""
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    
    palavras = []
    with open(caminho, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        cols = [c.strip().lower() for c in reader.fieldnames or []]
        if 'pt-br' not in cols or 'en' not in cols:
            raise ValueError("CSV deve ter colunas pt-br e en")
        
        for linha in reader:
            pt = linha.get('pt-br', '').strip()
            en = linha.get('en', '').strip()
            if not pt or not en:
                continue
            try:
                len_pt = int(linha.get('len-pt-br', len(pt)))
                len_en = int(linha.get('len-en', len(en)))
            except ValueError:
                continue
            if len(pt) != len_pt or len(en) != len_en:
                continue
            palavras.append({'pt_br': pt, 'en': en, 'len_pt_br': len_pt, 'len_en': len_en})
    
    if not palavras:
        raise ValueError("Nenhuma palavra válida no CSV")
    
    palavras.sort(key=lambda p: (p['len_pt_br'], p['pt_br']))
    return palavras


def filtrar_tamanho(palavras, min_len, max_len, idioma='pt_br'):
    """Filtra palavras por tamanho."""
    col = 'len_pt_br' if idioma == 'pt_br' else 'len_en'
    return [p for p in palavras if min_len <= p[col] <= max_len]
