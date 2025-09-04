from database import get_connection

conn = get_connection()
cursor = conn.cursor()

class userLogin:
    @staticmethod
    def ler_login(LOGIN_USER, SENHA):
        try:
            cursor.execute("SELECT * FROM USUARIO WHERE LOGIN_USER = ? and SENHA = ?", (LOGIN_USER, SENHA))
            usuario = cursor.fetchone()
            if usuario:
                return True
            else:
                return False
        except sqlite3.IntegrityError:
            print("Erro ao fazer login!")
            