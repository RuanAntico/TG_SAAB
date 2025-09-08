import sqlite3
import bcrypt

from database import get_connection

class UserLogin:
    @staticmethod
    def Autenticar_Login(LOGIN_USER, SENHA):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM USUARIO WHERE LOGIN_USER = ?", (LOGIN_USER,))
            row = cursor.fetchone()

            if row is None:
                print("Usuário não encontrado")
                return False

            senha_hash = row[2]  # coluna SENHA
            if isinstance(senha_hash, str):
                senha_hash = senha_hash.encode("utf-8")

            senha_bytes = SENHA.encode("utf-8")

            return bcrypt.checkpw(senha_bytes, senha_hash)

            if bcrypt.checkpw(senha_bytes, senha_hash):
                return True
            else:
                return False

        except Exception as e:
            print(f"Erro ao fazer login: {e}")
            return False

        finally:
            conn.close()

        