# main.py
import tkinter as tk
from model import AcoesModel
from view import AcoesView
from controller import AcoesController

def main():
    # 1. Inicializa o Tkinter  # [cite: 119]
    root = tk.Tk()
    
    # 2. Instancia o Model (Dados)  # [cite: 121]
    model = AcoesModel()
    
    # 3. Instancia a View (Interface)  # [cite: 122]
    view = AcoesView(root)
    
    # 4. Instancia o Controller (Elo Vital), passando Model e View  # [cite: 123]
    controller = AcoesController(model, view)
    
    # 5. Inicia o loop principal do Tkinter  # [cite: 124]
    root.mainloop()

if __name__ == '__main__':
    main()
