# model.py
from db_config import conectar
from mysql.connector import Error

class AcoesModel:
    """
    Camada Model: Gerencia a persistência das ações sustentáveis no banco de dados.
    """

    def adicionar_acao(self, descricao, categoria, impacto, data):
        """Insere um novo registro de ação no banco de dados."""
        conexao = conectar()
        if conexao is None:
            return False, "Erro de conexão com o banco de dados."

        sql = "INSERT INTO acoes_sustentaveis (descricao, categoria, impacto, data) VALUES (%s, %s, %s, %s)"
        dados = (descricao, categoria, impacto, data)
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, dados)
            conexao.commit()
            return True, "Ação sustentável registrada com sucesso!"
        except Error as e:
            # Tratamento de exceção e log de erro no console 
            print(f"Erro ao adicionar ação: {e}")
            return False, f"Erro SQL: {e}"
        finally:
            cursor.close()
            conexao.close()

    def listar_acoes(self):
        """Retorna todos os registros de ações sustentáveis."""
        conexao = conectar()
        if conexao is None:
            return []

        sql = "SELECT id, descricao, categoria, impacto, data FROM acoes_sustentaveis"
        cursor = conexao.cursor()

        try:
            cursor.execute(sql)
            # Retorna todos os resultados como uma lista de tuplas
            resultados = cursor.fetchall()
            return resultados
        except Error as e:
            print(f"Erro ao listar ações: {e}")
            return []
        finally:
            cursor.close()
            conexao.close()

    def remover_acao(self, id_acao):
        """Deleta uma ação específica pelo ID."""
        conexao = conectar()
        if conexao is None:
            return False, "Erro de conexão com o banco de dados."

        sql = "DELETE FROM acoes_sustentaveis WHERE id = %s"
        dados = (id_acao,)
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, dados)
            conexao.commit()
            # Verifica se alguma linha foi afetada para confirmar a remoção
            if cursor.rowcount > 0:
                return True, f"Ação ID {id_acao} removida com sucesso."
            else:
                return False, f"ID {id_acao} não encontrado."
        except Error as e:
            print(f"Erro ao remover ação: {e}")
            return False, f"Erro SQL: {e}"
        finally:
            cursor.close()
            conexao.close()

if __name__ == '__main__':
    # Teste do Model (Critério de Sucesso) [cite: 70]
    model = AcoesModel()
    
    # 1. Inserir (adicionar_acao)
    print("\nTeste de Inserção:")
    sucesso, msg = model.adicionar_acao("Economia de 50W em monitor", "Energia", "Média", "2025-11-12")
    print(f"Status: {sucesso}, Mensagem: {msg}")

    # 2. Listar (listar_acoes)
    print("\nTeste de Listagem:")
    acoes = model.listar_acoes()
    if acoes:
        print("Ações cadastradas (última inserida):")
        for acao in acoes:
            print(acao)
    else:
        print("Nenhuma ação encontrada.")
    
    # 3. Remover (remover_acao) - Remove a ação que acabamos de adicionar (se tiver dado certo)
    if sucesso and acoes:
        id_para_remover = acoes[-1][0] # Pega o ID da última ação
        print(f"\nTeste de Remoção (ID {id_para_remover}):")
        sucesso_rem, msg_rem = model.remover_acao(id_para_remover)
        print(f"Status: {sucesso_rem}, Mensagem: {msg_rem}")

        # Listar novamente para confirmar
        print("\nListagem após remoção:")
        acoes_restantes = model.listar_acoes()
        for acao in acoes_restantes:
            print(acao)
        if len(acoes_restantes) < len(acoes):
             print("Remoção confirmada.")
        else:
             print("Remoção falhou.")