# main.py
import os
import sys

# Adiciona o diretório atual do script ao PYTHONPATH.
# Se main.py está em 'mini-maratona-berolab/', então 'mini-maratona-berolab/'
# será adicionado, permitindo que 'dino_runner' seja encontrado.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Importa a classe Game diretamente do módulo dino_runner.game (com 'g' minúsculo)
from dino_runner.game import Game

if __name__ == "__main__":
    game = Game()
    game.execute()
