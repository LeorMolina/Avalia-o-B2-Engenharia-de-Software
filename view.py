# view.py
import tkinter as tk
from tkinter import messagebox, ttk

# --------------------
# CLASSE DE LOGIN (Missão 8)
# --------------------
class LoginView:
    """Interface de Login simples."""
    def __init__(self, master, main_app_callback):
        self.master = master
        master.title("EcoTrack - Portal Verde")
        self.main_app_callback = main_app_callback 
        
        master.geometry("400x200") 
        master.resizable(False, False)

        self.login_frame = tk.Frame(master, padx=20, pady=20)
        self.login_frame.pack(expand=True)

        # Campos
        tk.Label(self.login_frame, text="Usuário:").grid(row=0, column=0, sticky="w", pady=5)
        self.usuario_entry = tk.Entry(self.login_frame, width=30)
        self.usuario_entry.grid(row=0, column=1, padx=5, pady=5)
        self.usuario_entry.focus_set() 
        
        tk.Label(self.login_frame, text="Senha:").grid(row=1, column=0, sticky="w", pady=5)
        self.senha_entry = tk.Entry(self.login_frame, width=30, show="*") 
        self.senha_entry.grid(row=1, column=1, padx=5, pady=5)

        # Botão
        btn_login = tk.Button(self.login_frame, text="Entrar", command=self.login_handler, width=20)
        btn_login.grid(row=2, column=0, columnspan=2, pady=15)
        self.master.bind('<Return>', lambda event: self.login_handler()) 
        
        self.controller = None 

    def set_controller(self, controller):
        self.controller = controller

    def login_handler(self):
        """Coleta dados e chama a verificação no Controller."""
        usuario = self.usuario_entry.get().strip()
        senha = self.senha_entry.get().strip()
        
        if self.controller:
            self.controller.fazer_login(usuario, senha)

    def mostrar_aviso_simples(self, mensagem):
        """Método de aviso simples (Missão 7 e 8)."""
        messagebox.showwarning("Aviso", mensagem)

    def fechar_janela(self):
        """Fecha a janela de login e desliga o atalho Enter."""
        self.master.unbind('<Return>')
        self.login_frame.destroy()


# --------------------
# CLASSE PRINCIPAL (EcoTrack)
# --------------------
class AcoesView:
    """
    Camada View: Interface gráfica do EcoTrack utilizando Tkinter.
    """
    def __init__(self, master):
        self.master = master
        
        self.controller = None 
        self.categorias = ["Energia", "Reciclagem", "Transporte Verde", "Outro"]
        
        self.configurar_layout(master)

    def set_controller(self, controller):
        """Define o Controller para que a View possa chamar seus métodos."""
        self.controller = controller

    def configurar_layout(self, master):
        # 1. Frame de Cadastro (Entrada de Dados)
        cadastro_frame = tk.LabelFrame(master, text="Cadastro de Ação", padx=10, pady=10)
        cadastro_frame.pack(padx=10, pady=10, fill="x")

        # Campos de entrada
        self.fields = {} 
        
        # Descrição
        tk.Label(cadastro_frame, text="Descrição:").grid(row=0, column=0, sticky="w", pady=2)
        self.fields['descricao'] = tk.Entry(cadastro_frame, width=50)
        self.fields['descricao'].grid(row=0, column=1, padx=5, pady=2)
        
        # Categoria (ComboBox/Dropdown)
        tk.Label(cadastro_frame, text="Categoria:").grid(row=1, column=0, sticky="w", pady=2)
        self.categoria_var = tk.StringVar(master)
        self.categoria_var.set(self.categorias[0]) 
        self.fields['categoria'] = ttk.Combobox(cadastro_frame, textvariable=self.categoria_var, values=self.categorias, state="readonly", width=47)
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
        
        # Botões
        btn_adicionar = tk.Button(cadastro_frame, text="Adicionar Ação", command=self.adicionar_handler)
        btn_adicionar.grid(row=4, column=0, columnspan=2, pady=10)

        # 2. Frame de Relatório e Filtro (Missão 6)
        filtro_frame = tk.LabelFrame(master, text="Relatório e Filtro", padx=10, pady=10)
        filtro_frame.pack(padx=10, pady=5, fill="x")

        # Contador de Ações (Missão 6)
        self.contador_var = tk.StringVar()
        self.contador_var.set("Total de Ações: 0")
        tk.Label(filtro_frame, textvariable=self.contador_var, font=('Arial', 10, 'bold')).pack(side="left", padx=5)
        
        # Combo Box de Filtro por Categoria (Missão 6)
        tk.Label(filtro_frame, text="Filtrar por Categoria:").pack(side="left", padx=(20, 5))
        
        self.filtro_var = tk.StringVar(master)
        opcoes_filtro = ["Todas as Categorias"] + self.categorias 
        self.filtro_var.set(opcoes_filtro[0])
        
        self.filtro_combo = ttk.Combobox(filtro_frame, textvariable=self.filtro_var, values=opcoes_filtro, state="readonly", width=25)
        self.filtro_combo.pack(side="left", padx=5)

        # Botão Filtrar (Missão 6)
        btn_filtrar = tk.Button(filtro_frame, text="Filtrar", command=self.filtrar_handler)
        btn_filtrar.pack(side="left", padx=5)


        # 3. Frame de Visualização (Treeview)
        visualizacao_frame = tk.LabelFrame(master, text="Ações Registradas", padx=10, pady=10)
        visualizacao_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Configuração do Treeview 
        columns = ("ID", "Descrição", "Categoria", "Impacto", "Data")
        self.tree = ttk.Treeview(visualizacao_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.W)
            self.tree.column(col, width=100, minwidth=50, stretch=tk.YES)
            
        self.tree.column("ID", width=50, anchor=tk.CENTER)

        # Scrollbar vertical
        v_scrollbar = ttk.Scrollbar(visualizacao_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        v_scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Botões de Ação na Lista 
        action_frame = tk.Frame(master)
        action_frame.pack(pady=5, fill="x")

        btn_listar = tk.Button(action_frame, text="Recarregar Tudo", command=self.listar_handler)
        btn_listar.pack(side="left", padx=5)

        btn_remover = tk.Button(action_frame, text="Remover Selecionada", command=self.remover_handler)
        btn_remover.pack(side="right", padx=5)


    def adicionar_handler(self):
        """Coleta dados e chama o método adicionar do Controller."""
        if self.controller:
            data = {k: v.get() if isinstance(v, tk.Entry) else v.get() for k, v in self.fields.items()}
            
            data['categoria'] = self.categoria_var.get()
            data['impacto'] = self.impacto_var.get()
            
            self.controller.adicionar(data)
        else:
            self.mostrar_alerta("Erro interno: Controller não definido.")

    def listar_handler(self):
        """Chama o método listar do Controller (sem filtro)."""
        self.filtro_var.set("Todas as Categorias") 
        if self.controller:
            self.controller.listar()
        else:
            self.mostrar_alerta("Erro interno: Controller não definido.")

    def filtrar_handler(self):
        """Coleta o valor do filtro e chama o método listar_filtrado do Controller."""
        categoria_selecionada = self.filtro_var.get()
        if self.controller:
            self.controller.listar_filtrado(categoria_selecionada)
        else:
            self.mostrar_alerta("Erro interno: Controller não definido.")

    def remover_handler(self):
        """Coleta o ID da linha selecionada e chama o método remover do Controller."""
        selecionado = self.tree.focus()
        if not selecionado:
            self.mostrar_aviso("Selecione uma ação", "Por favor, clique em uma linha na tabela para remover.")
            return

        id_acao = self.tree.item(selecionado, "values")[0]
        
        if messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover a Ação ID {id_acao}?"):
            if self.controller:
                self.controller.remover(id_acao)
            else:
                self.mostrar_alerta("Erro interno: Controller não definido.")

    def atualizar_lista(self, dados):
        """Limpa e insere os dados fornecidos (lista de tuplas) no Treeview."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for row in dados:
            row_list = list(row)
            if not isinstance(row_list[-1], (type(''), type(None))):
                 row_list[-1] = str(row_list[-1])
            self.tree.insert("", tk.END, values=row_list)

    def atualizar_contador(self, total, is_filtered=False, categoria=None):
        """Atualiza o Label com o total de ações cadastradas ou filtradas."""
        if is_filtered:
            msg = f"Ações de '{categoria}': {total}"
        else:
            msg = f"Total de Ações Cadastradas: {total}"
        self.contador_var.set(msg)

    # Métodos de Feedback ao Usuário (messagebox) 
    def mostrar_info(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)

    def mostrar_alerta(self, titulo, mensagem):
        messagebox.showerror(titulo, mensagem) 

    def mostrar_aviso(self, titulo, mensagem):
        messagebox.showwarning(titulo, mensagem)

    def mostrar_aviso_simples(self, mensagem):
        """Método de aviso simples (Missão 7 e 8)."""
        messagebox.showwarning("Aviso", mensagem)
        
    def limpar_campos(self):
        """Limpa todos os campos de entrada após a inserção."""
        for name, widget in self.fields.items():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
        self.categoria_var.set(self.categorias[0])
        self.impacto_var.set("Baixo")