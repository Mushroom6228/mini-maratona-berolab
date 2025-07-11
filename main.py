<<<<<<< HEAD
import os # Importa o módulo 'os' para interagir com o sistema operacional, como manipulação de caminhos.
import sys # Importa o módulo 'sys', que fornece acesso a variáveis e funções que interagem fortemente com o interpretador.
=======
# main.py
import os
import sys

# Adiciona o diretório atual do script ao PYTHONPATH.
# Se main.py está em 'mini-maratona-berolab/', então 'mini-maratona-berolab/'
# será adicionado, permitindo que 'dino_runner' seja encontrado.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Importa a classe Game diretamente do módulo dino_runner.game (com 'g' minúsculo)
from dino_runner.game import Game
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82

# Adiciona o diretório atual do script ao PYTHONPATH.
# Isso é crucial para que o Python consiga encontrar o pacote 'dino_runner'
# quando o script 'main.py' é executado.
# os.path.abspath(os.path.dirname(__file__)) retorna o caminho absoluto do diretório onde 'main.py' está.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Importa a classe 'Game' diretamente do módulo 'dino_runner.game'.
# Como o diretório do projeto foi adicionado ao PYTHONPATH, Python pode encontrar 'dino_runner'.
from dino_runner.game import Game

# Verifica se o script está sendo executado diretamente (não importado como um módulo).
if __name__ == "__main__":
    game = Game() # Cria uma instância da classe 'Game', inicializando o jogo.
    game.execute() # Inicia o loop principal do jogo.
