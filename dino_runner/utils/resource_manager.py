import sys # Importa o módulo sys, que fornece acesso a variáveis e funções que interagem fortemente com o interpretador.
import os # Importa o módulo os, que fornece uma maneira de usar funcionalidades dependentes do sistema operacional, como manipulação de caminhos.

def resource_path(relative_path):
    """
    Obtém o caminho absoluto para o recurso, funciona para desenvolvimento e para o PyInstaller.
    A `relative_path` deve ser relativa ao diretório raiz do pacote `dino_runner`.
    Ex: "dino_runner/assets/Font/joystix monospace.otf"
    """
    # Normaliza as barras no caminho para usar sempre barras frontais e remove barras duplas.
    relative_path = relative_path.replace('\\', '/').replace('//', '/')
    # Remove repetições de 'dino_runner/' no início do caminho, se houver.
    while relative_path.startswith('dino_runner/dino_runner/'):
        relative_path = relative_path.replace('dino_runner/dino_runner/', 'dino_runner/', 1)
    # Remove barras duplas extras no início do caminho, se houver.
    while relative_path.startswith('dino_runner//'):
        relative_path = relative_path.replace('dino_runner//', 'dino_runner/', 1)
    # Verifica novamente e corrige se 'dino_runner/dino_runner' ainda aparecer no início.
    if relative_path.startswith('dino_runner/dino_runner'):
        relative_path = relative_path.replace('dino_runner/dino_runner', 'dino_runner', 1)
    # Verifica novamente e corrige se 'dino_runner//' ainda aparecer no início.
    elif relative_path.startswith('dino_runner//'):
        relative_path = relative_path.replace('dino_runner//', 'dino_runner/', 1)
    try:
        # Quando o PyInstaller empacota o aplicativo, ele cria uma pasta temporária.
        # O caminho para essa pasta é armazenado em sys._MEIPASS.
        # Os recursos são colocados dentro de uma subpasta "dino_runner" dentro de sys._MEIPASS.
        base_path = os.path.join(sys._MEIPASS, "dino_runner")
    except Exception:
        # Se não estiver rodando como um executável empacotado pelo PyInstaller (ou seja, em desenvolvimento),
        # o caminho base é a raiz do projeto.
        # __file__ é o caminho deste arquivo (resource_manager.py).
        # os.path.dirname(__file__) obtém o diretório deste arquivo ('dino_runner/utils').
        # os.path.join(..., "..", "..") sobe dois níveis para a raiz do projeto.
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    # Combina o caminho base com o caminho relativo do recurso para formar o caminho completo.
    full_path = os.path.join(base_path, relative_path)
    # Normaliza o caminho completo para o formato padrão do sistema operacional (ex: converte '/' para '\' no Windows).
    full_path = os.path.normpath(full_path)
    return full_path # Retorna o caminho absoluto e normalizado para o recurso.
