"""
Aula 02 - Word Defender
Execute: python main.py
Ou: python main.py caminho/words.csv
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import Jogo

if __name__ == "__main__":
    caminho_csv = sys.argv[1] if len(sys.argv) > 1 else None
    Jogo(caminho_csv).executar()
