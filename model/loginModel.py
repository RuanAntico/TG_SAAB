import pyodbc
import bcrypt


from database import get_connection

class UserLogin:
    @staticmethod
    def Autenticar_Login(LOGIN_USER, SENHA):
        conn = None  # Inicializa a variável de conexão
        try:
            conn = get_connection()
            # Se a conexão falhar, get_connection() pode retornar None
            if conn is None:
                raise ConnectionError("Não foi possível conectar ao banco de dados.")

            cursor = conn.cursor()

            cursor.execute("SELECT SENHA FROM USUARIO WHERE LOGIN_USER = ?", (LOGIN_USER,))
            row = cursor.fetchone()

            if row is None:
                print("Usuário não encontrado")
                return False

            senha_hash = row[0]
            if isinstance(senha_hash, str):
                senha_hash = senha_hash.encode("utf-8")

            senha_bytes = SENHA.encode("utf-8")

            return bcrypt.checkpw(senha_bytes, senha_hash)

        except Exception as e:
            print(f"Erro ao fazer login: {e}")
            return False

        finally:
            # Garante que a conexão seja fechada apenas se ela foi estabelecida com sucesso
            if conn:
                conn.close()

        