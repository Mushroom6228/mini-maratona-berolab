# dino_runner/utils/resource_manager.py
import sys
import os

def resource_path(relative_path):
    """
    Obtém o caminho absoluto para o recurso, funciona para desenvolvimento e para o PyInstaller.
    A `relative_path` deve ser relativa ao diretório raiz do pacote `dino_runner`.
    Ex: "dino_runner/assets/Font/joystix monospace.otf"
    """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        # Quando empacotamos "dino_runner", ele vai para sys._MEIPASS/dino_runner
        # Então, o caminho base para os assets é sys._MEIPASS/dino_runner
        base_path = os.path.join(sys._MEIPASS, "dino_runner")
        print(f"DEBUG (resource_path): Executável detectado. Base path: {base_path}") # Debug
    except Exception:
        # No ambiente de desenvolvimento, o caminho base é o diretório onde `main.py` está.
        # O script `resource_manager.py` está em dino_runner/utils/, então precisamos subir 2 níveis
        # para chegar à raiz do projeto (onde "dino_runner" e "main.py" estão).
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        print(f"DEBUG (resource_path): Ambiente de desenvolvimento. Base path: {base_path}") # Debug

    full_path = os.path.join(base_path, relative_path)
    print(f"DEBUG (resource_path): Resolvendo caminho: {full_path}") # Debug
    return full_path
