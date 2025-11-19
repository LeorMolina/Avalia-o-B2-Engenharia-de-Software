# controller.py
from datetime import date
from tkinter import messagebox

# Novo Controller para gerenciar o Login (Missão 8)
class LoginController:
    def __init__(self, model, login_view, root):
        self.model = model
        self.login_view = login_view
        self.root = root 
        self.login_view.set_controller(self)

    def fazer_login(self, usuario, senha):
        """Verifica credenciais e inicia a aplicação principal ou exibe aviso."""
        
        # Validações básicas (Missão 8)
        if not usuario or not senha:
            self.login_view.mostrar_aviso_simples("Usuário e senha são obrigatórios.")
            return

        # Chama o Model para validar
        credenciais_validas = self.model.validar_login(usuario, senha)

        if credenciais_validas:
            self.login_view.fechar_janela() # Fecha a janela de login
            self.login_view.main_app_callback() # Inicia a aplicação principal
        else:
            self.login_view.mostrar_aviso_simples("Usuário ou senha incorretos.")

class AcoesController:
    """
    Camada Controller: Conecta a View (Interface) com o Model (Dados).
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self) 
        self.listar()

    def adicionar(self, dados_acao):
        """
        Recebe dados da View, valida (Missão 7) e chama a inserção no Model.
        """
        descricao = dados_acao.get('descricao', '').strip()
        categoria = dados_acao.get('categoria', '').strip()
        impacto = dados_acao.get('impacto', '').strip()
        data_str = dados_acao.get('data', '').strip()

        # Validações Específicas (Missão 7)
        if not descricao:
            self.view.mostrar_aviso_simples("A descrição da ação não pode ficar vazia.")
            return

        if not categoria:
            self.view.mostrar_aviso_simples("A categoria da ação é obrigatória.")
            return
        
        if not impacto:
            self.view.mostrar_aviso_simples("O impacto da ação é obrigatório.")
            return
        
        if not data_str:
            self.view.mostrar_aviso_simples("A data da ação é obrigatória.")
            return

        # Validação de formato da data (existente)
        try:
            data_obj = date.fromisoformat(data_str)
        except ValueError:
            self.view.mostrar_alerta("Formato de Data Inválido", "Use o formato AAAA-MM-DD (ex: 2025-11-12).")
            return

        # Chama o Model para persistir os dados
        sucesso, mensagem = self.model.adicionar_acao(descricao, categoria, impacto, data_obj)

        if sucesso:
            self.view.mostrar_info("Sucesso!", mensagem)
            self.view.limpar_campos()
            self.listar() 
        else:
            self.view.mostrar_alerta("Erro na Inserção", mensagem)


    def listar(self):
        """
        Busca todos os dados no Model, envia para a View exibir e atualiza o contador.
        """
        acoes = self.model.listar_acoes()
        total = self.model.contar_total()
        
        if acoes is None:
            self.view.mostrar_alerta("Erro na Listagem", "Não foi possível buscar os dados. Verifique a conexão.")
        else:
            self.view.atualizar_lista(acoes)
            self.view.atualizar_contador(total)


    def listar_filtrado(self, categoria):
        """
        Busca ações no Model com base no filtro de categoria e atualiza a View (Missão 6).
        """
        if categoria == "Todas as Categorias":
            self.listar()
            return

        acoes = self.model.listar_acoes(categoria_filtro=categoria)
        total_filtrado = len(acoes) if acoes is not None else 0
        
        if acoes is None:
            self.view.mostrar_alerta("Erro na Listagem Filtrada", "Não foi possível buscar os dados. Verifique a conexão.")
        else:
            self.view.atualizar_lista(acoes)
            self.view.atualizar_contador(total_filtrado, is_filtered=True, categoria=categoria)


    def remover(self, id_acao):
        """
        Recebe o ID da View e chama o método de remoção no Model.
        """
        try:
            id_int = int(id_acao)
        except ValueError:
            self.view.mostrar_alerta("Erro de ID", "O ID deve ser um número inteiro.")
            return

        sucesso, mensagem = self.model.remover_acao(id_int)

        if sucesso:
            self.view.mostrar_info("Remoção Concluída", mensagem)
            self.listar()
        else:
            self.view.mostrar_alerta("Erro na Remoção", mensagem)