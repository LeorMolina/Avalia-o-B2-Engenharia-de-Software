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

    def listar_acoes(self, categoria_filtro=None):
        """Retorna todos os registros de ações sustentáveis, opcionalmente filtrados por categoria."""
        conexao = conectar()
        if conexao is None:
            return []

        sql = "SELECT id, descricao, categoria, impacto, data FROM acoes_sustentaveis"
        dados = []

        if categoria_filtro:
            sql += " WHERE categoria = %s"
            dados.append(categoria_filtro)
            
        sql += " ORDER BY data DESC"

        cursor = conexao.cursor()

        try:
            cursor.execute(sql, dados)
            resultados = cursor.fetchall()
            return resultados
        except Error as e:
            print(f"Erro ao listar ações: {e}")
            return []
        finally:
            cursor.close()
            conexao.close()

    def contar_total(self):
        """Retorna a contagem total de registros na tabela."""
        conexao = conectar()
        if conexao is None:
            return 0

        sql = "SELECT COUNT(*) FROM acoes_sustentaveis"
        cursor = conexao.cursor()

        try:
            cursor.execute(sql)
            total = cursor.fetchone()[0]
            return total
        except Error as e:
            print(f"Erro ao contar ações: {e}")
            return 0
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

    def validar_login(self, usuario, senha):
        """Verifica as credenciais de login na tabela usuarios."""
        conexao = conectar()
        if conexao is None:
            return None 

        sql = "SELECT usuario FROM usuarios WHERE usuario = %s AND senha = %s"
        dados = (usuario, senha)
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, dados)
            resultado = cursor.fetchone() 
            return resultado
        except Error as e:
            print(f"Erro ao validar login: {e}")
            return None
        finally:
            cursor.close()
            conexao.close()