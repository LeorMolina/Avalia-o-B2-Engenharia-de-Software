# main.py
import tkinter as tk
from model import AcoesModel
from view import AcoesView, LoginView 
from controller import AcoesController, LoginController 

def iniciar_app_principal(root, model):
    """Inicializa e exibe a tela principal do EcoTrack (AcoesView)."""
    # 3. Instancia a View (Interface Principal)
    view_principal = AcoesView(root)
    
    # 4. Instancia o Controller (Elo Vital), passando Model e View
    AcoesController(model, view_principal)
    
    # Redimensiona a janela após o login para caber a View Principal
    root.geometry("") 
    root.title("EcoTrack - Sistema Sustentável")


def main():
    # 1. Inicializa o Tkinter
    root = tk.Tk()
    
    # 2. Instancia o Model (Dados)
    model = AcoesModel()
    
    # Prepara a função de callback para iniciar a aplicação principal
    callback_iniciar = lambda: iniciar_app_principal(root, model)
    
    # 3. Instancia a View de Login
    login_view = LoginView(root, callback_iniciar)
    
    # 4. Instancia o Controller de Login
    LoginController(model, login_view, root)
    
    # 5. Inicia o loop principal do Tkinter
    root.mainloop()

if __name__ == '__main__':
    main()