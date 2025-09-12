import sqlite3
import bcrypt

from database import get_connection

class CadastrarDados:

    @staticmethod
    def criar_usuario(LOGIN_USER, SENHA, TIPO_USER):
        # Gera o hash da senha
        hash_senha = bcrypt.hashpw(SENHA.encode("utf-8"), bcrypt.gensalt(8))

        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO USUARIO(LOGIN_USER, SENHA, TIPO_USER) VALUES (?, ?, ?)",
                (LOGIN_USER, hash_senha, TIPO_USER)
            )
            conn.commit()
            return True

        except sqlite3.IntegrityError as e:
            print("Erro ao cadastrar usuário:", e)
            return False
        except Exception as e:
            print(f"Erro ao criar pessoa: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def criar_pessoa(CPF, RG, NOME, TELEFONE, DT_NASC, EMAIL):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO PESSOA(CPF, RG, NOME, TELEFONE, DT_NASC, EMAIL) VALUES (?, ?, ?, ?, ?, ?)", (CPF, RG, NOME, TELEFONE, DT_NASC, EMAIL))
            conn.commit()
            return True

        except sqlite3.IntegrityError as e:
            print(f"Erro de integridade: {e}")
            conn.rollback()
            return False
        except Exception as e:
            print(f"Erro ao criar pessoa: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
