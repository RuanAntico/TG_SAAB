import pyodbc
import bcrypt
from database import get_connection

class UserLogin:
    @staticmethod
    def Autenticar_Login(LOGIN_USER, SENHA):
        conn = None 
        try:
            conn = get_connection()
            if conn is None:
                raise ConnectionError("Não foi possível conectar ao banco de dados.")

            cursor = conn.cursor()

            cursor.execute("SELECT * FROM USUARIO WHERE LOGIN_USER = ?", (LOGIN_USER,))
            row = cursor.fetchone()

            if row is None:
                return None 
            columns = [column[0] for column in cursor.description]
            usuario_dict = dict(zip(columns, row))

            senha_hash = usuario_dict.get('SENHA') 
        
            if not senha_hash:
                 print("ERRO: Coluna 'SENHA' não encontrada no usuário.")
                 return None

            if isinstance(senha_hash, str):
                senha_hash = senha_hash.encode("utf-8")

            senha_bytes = SENHA.encode("utf-8")

            if bcrypt.checkpw(senha_bytes, senha_hash):
              
                return usuario_dict
            else:
          
                print("Senha incorreta")
                return None

        except Exception as e:
            print(f"Erro ao fazer login: {e}")
            return None

        finally:
            if conn:
                conn.close()