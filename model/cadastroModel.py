import sqlite3
from database import get_connection

class CadastrarDados:
    @staticmethod
    def criar_pessoa(CPF, RG, NOME, TELEFONE, DT_NASC, EMAIL):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO PESSOA(CPF, RG, NOME, TELEFONE, DT_NASC, EMAIL) VALUES (?, ?, ?, ?, ?, ?)", (CPF, RG, NOME, TELEFONE, DT_NASC, EMAIL))
            conn.commit()
            return True
            
        except sqlite3.IntegrityError as e:
            print("Erro de integridade: {e}")
            return False
        except Exception as e:
            print("Erro ao criar pessoa: {e}")
            return False
        finally:
            conn.close()    