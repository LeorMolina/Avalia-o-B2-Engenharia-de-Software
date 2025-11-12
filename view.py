# view.py
import tkinter as tk
from tkinter import messagebox, ttk

class AcoesView:
    """
    Camada View: Interface gráfica do EcoTrack utilizando Tkinter.
    """
    def __init__(self, master):
        self.master = master
        master.title("EcoTrack - Sistema Sustentável")
        
        # O controller será setado após a instanciação (Missão 4)
        self.controller = None 
        
        self.configurar_layout(master)

    def set_controller(self, controller):
        """Define o Controller para que a View possa chamar seus métodos."""
        self.controller = controller

    def configurar_layout(self, master):
        # 1. Frame de Cadastro (Entrada de Dados)
        cadastro_frame = tk.LabelFrame(master, text="Cadastro de Ação", padx=10, pady=10)
        cadastro_frame.pack(padx=10, pady=10, fill="x")

        # Campos de entrada [cite: 82]
        self.fields = {} # Dicionário para armazenar as variáveis e Entry widgets
        
        # Descrição
        tk.Label(cadastro_frame, text="Descrição:").grid(row=0, column=0, sticky="w", pady=2)
        self.fields['descricao'] = tk.Entry(cadastro_frame, width=50)
        self.fields['descricao'].grid(row=0, column=1, padx=5, pady=2)
        
        # Categoria (ComboBox/Dropdown)
        tk.Label(cadastro_frame, text="Categoria:").grid(row=1, column=0, sticky="w", pady=2)
        self.categoria_var = tk.StringVar(master)
        self.categoria_var.set("Energia") # Valor inicial
        categorias = ["Energia", "Reciclagem", "Transporte Verde", "Outro"]
        self.fields['categoria'] = ttk.Combobox(cadastro_frame, textvariable=self.categoria_var, values=categorias, state="readonly", width=47)
        self.fields['categoria'].grid(row=1, column=1, padx=5, pady=2)
        
        # Impacto
        tk.Label(cadastro_frame, text="Impacto:").grid(row=2, column=0, sticky="w", pady=2)
        self.impacto_var = tk.StringVar(master)
        self.impacto_var.set("Baixo") 
        impactos = ["Baixo", "Médio", "Alto"]
        self.fields['impacto'] = ttk.Combobox(cadastro_frame, textvariable=self.impacto_var, values=impactos, state="readonly", width=47)
        self.fields['impacto'].grid(row=2, column=1, padx=5, pady=2)

        # Data
        tk.Label(cadastro_frame, text="Data (AAAA-MM-DD):").grid(row=3, column=0, sticky="w", pady=2)
        self.fields['data'] = tk.Entry(cadastro_frame, width=50)
        self.fields['data'].grid(row=3, column=1, padx=5, pady=2)
        
        # Botões [cite: 83]
        btn_adicionar = tk.Button(cadastro_frame, text="Adicionar Ação", command=self.adicionar_handler)
        btn_adicionar.grid(row=4, column=0, columnspan=2, pady=10)

        # 2. Frame de Visualização (Treeview)
        visualizacao_frame = tk.LabelFrame(master, text="Ações Registradas", padx=10, pady=10)
        visualizacao_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Configuração do Treeview 
        columns = ("ID", "Descrição", "Categoria", "Impacto", "Data")
        self.tree = ttk.Treeview(visualizacao_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.W)
            self.tree.column(col, width=100, minwidth=50, stretch=tk.YES)
            
        # Ajuste de largura da coluna ID
        self.tree.column("ID", width=50, anchor=tk.CENTER)

        # Scrollbar vertical
        v_scrollbar = ttk.Scrollbar(visualizacao_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        # Empacotamento
        v_scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Botões de Ação na Lista [cite: 83]
        action_frame = tk.Frame(master)
        action_frame.pack(pady=5, fill="x")

        btn_listar = tk.Button(action_frame, text="Listar Ações", command=self.listar_handler)
        btn_listar.pack(side="left", padx=5)

        btn_remover = tk.Button(action_frame, text="Remover Selecionada", command=self.remover_handler)
        btn_remover.pack(side="right", padx=5)


    def adicionar_handler(self):
        """Coleta dados e chama o método adicionar do Controller."""
        if self.controller:
            # Validação simples de campos vazios
            data = {k: v.get() if isinstance(v, tk.Entry) else v.get() for k, v in self.fields.items()}
            
            # Incluir dados dos Comboboxes (StringVar)
            data['categoria'] = self.categoria_var.get()
            data['impacto'] = self.impacto_var.get()
            
            # Passa a responsabilidade para o Controller
            self.controller.adicionar(data)
        else:
            self.mostrar_alerta("Erro interno: Controller não definido.")

    def listar_handler(self):
        """Chama o método listar do Controller."""
        if self.controller:
            self.controller.listar()
        else:
            self.mostrar_alerta("Erro interno: Controller não definido.")

    def remover_handler(self):
        """Coleta o ID da linha selecionada e chama o método remover do Controller."""
        selecionado = self.tree.focus()
        if not selecionado:
            self.mostrar_aviso("Selecione uma ação", "Por favor, clique em uma linha na tabela para remover.")
            return

        # Pega o ID da primeira coluna (ID) da linha selecionada
        id_acao = self.tree.item(selecionado, "values")[0]
        
        if messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover a Ação ID {id_acao}?"):
            if self.controller:
                self.controller.remover(id_acao)
            else:
                self.mostrar_alerta("Erro interno: Controller não definido.")

    def atualizar_lista(self, dados):
        """Limpa e insere os dados fornecidos (lista de tuplas) no Treeview."""
        # Limpa o Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Insere os novos dados
        for row in dados:
            # Garante que a data seja formatada como string antes de inserir
            row_list = list(row)
            if row_list and isinstance(row_list[-1], (type(''), type(None))):
                 # Se for string ou None, já está ok
                pass
            else:
                 # Se for um objeto date, converte para string
                 row_list[-1] = str(row_list[-1])
            self.tree.insert("", tk.END, values=row_list)

    # Métodos de Feedback ao Usuário (messagebox) 
    def mostrar_info(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)

    def mostrar_alerta(self, titulo, mensagem):
        messagebox.showerror(titulo, mensagem) # Usando showerror para erros mais críticos

    def mostrar_aviso(self, titulo, mensagem):
        messagebox.showwarning(titulo, mensagem)
        
    def limpar_campos(self):
        """Limpa todos os campos de entrada após a inserção."""
        for name, widget in self.fields.items():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
        # Reseta os Comboboxes
        self.categoria_var.set("Energia")
        self.impacto_var.set("Baixo")

if __name__ == '__main__':
    # Teste da View (Critério de Sucesso) [cite: 88]
    root = tk.Tk()
    app = AcoesView(root)
    app.mostrar_info("Teste de View", "Interface aberta com sucesso!")
    root.mainloop()