# controller.py
from datetime import date
from tkinter import messagebox

class AcoesController:
    """
    Camada Controller: Conecta a View (Interface) com o Model (Dados).
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        # Garante que a View saiba quem é o Controller para enviar comandos
        self.view.set_controller(self) 
        
        # Ao iniciar, lista as ações para popular a tela
        self.listar()

    def adicionar(self, dados_acao):
        """
        Recebe dados da View, valida (simplesmente) e chama a inserção no Model.
        """
        descricao = dados_acao.get('descricao', '').strip()
        categoria = dados_acao.get('categoria', '').strip()
        impacto = dados_acao.get('impacto', '').strip()
        data_str = dados_acao.get('data', '').strip()

        # Validação de dados (ex: campos obrigatórios)
        if not all([descricao, categoria, impacto, data_str]):
            self.view.mostrar_aviso("Dados Incompletos", "Todos os campos de cadastro devem ser preenchidos.")
            return

        # Validação de formato da data (poderia ser mais robusta, mas vamos com o básico)
        try:
            # Tenta converter a string para um objeto date (AAAA-MM-DD)
            data_obj = date.fromisoformat(data_str)
        except ValueError:
            self.view.mostrar_alerta("Formato de Data Inválido", "Use o formato AAAA-MM-DD (ex: 2025-11-12).")
            return

        # Chama o Model para persistir os dados [cite: 97]
        sucesso, mensagem = self.model.adicionar_acao(descricao, categoria, impacto, data_obj)

        if sucesso:
            self.view.mostrar_info("Sucesso!", mensagem)
            self.view.limpar_campos()
            # Atualiza a lista na tela após a inserção
            self.listar() 
        else:
            self.view.mostrar_alerta("Erro na Inserção", mensagem)


    def listar(self):
        """
        Busca todos os dados no Model e envia para a View exibir.
        """
        # Busca dados no Model [cite: 98]
        acoes = self.model.listar_acoes()

        if acoes is None:
            self.view.mostrar_alerta("Erro na Listagem", "Não foi possível buscar os dados. Verifique a conexão.")
        else:
            # Envia os dados para a View atualizar a tabela [cite: 98]
            self.view.atualizar_lista(acoes)


    def remover(self, id_acao):
        """
        Recebe o ID da View e chama o método de remoção no Model.
        """
        # Chama o Model para deletar o registro [cite: 99]
        try:
            id_int = int(id_acao)
        except ValueError:
            self.view.mostrar_alerta("Erro de ID", "O ID deve ser um número inteiro.")
            return

        sucesso, mensagem = self.model.remover_acao(id_int)

        if sucesso:
            self.view.mostrar_info("Remoção Concluída", mensagem)
            # Atualiza a lista na tela após a remoção
            self.listar()
        else:
            self.view.mostrar_alerta("Erro na Remoção", mensagem)