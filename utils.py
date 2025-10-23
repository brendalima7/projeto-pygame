import sys
import os

def resource_path(relative_path):
    """ Obtém o caminho absoluto do recurso, verificando se o código está sendo executado pelo PyInstaller. """
    
    # Verifica se o código está sendo executado pelo PyInstaller
    if hasattr(sys, '_MEIPASS'):
        # Se sim, usa o caminho temporário criado pelo PyInstaller
        base_path = sys._MEIPASS
    else:
        # Se não, usa o caminho atual (modo de desenvolvimento)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)