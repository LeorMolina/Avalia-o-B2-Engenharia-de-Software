# db_config.py
import mysql.connector
from mysql.connector import Error

def conectar():
    """
    Estabelece e retorna uma conexão com o banco de dados ecotrack_db.
    Inclui tratamento de exceção para falhas de conexão.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root",  # Mantenha o padrão da prova, mas em produção use variáveis de ambiente!
            database="ecotrack_db",
            # CORREÇÃO CRÍTICA: Tenta forçar o uso do plugin de autenticação mais antigo e compatível
            auth_plugin='mysql_native_password', 
            charset='latin1' 
        )
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

if __name__ == '__main__':
    # Teste de Conexão (Critério de Sucesso)
    conexao = conectar()
    if conexao and conexao.is_connected():
        print("Conexão bem-sucedida com o MySQL!")
        conexao.close()
    else:
        print("Falha na conexão.")