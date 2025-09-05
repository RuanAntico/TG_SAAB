import sqlite3
from database import get_connection

class UserLogin:
    @staticmethod    
    def ler_login(LOGIN_USER, SENHA):
        try:
            conn = get_connection()
            cursor = conn.cursor()
    
            cursor.execute("SELECT * FROM USUARIO WHERE LOGIN_USER = ? and SENHA = ?", (LOGIN_USER, SENHA))
            usuario = cursor.fetchone()
            conn.close()
            
            if usuario:
                return True
            else:
                return False
        except Exception as e:
            print("Erro ao fazer login: {e}")
            return False
            