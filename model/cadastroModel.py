import sqlite3
from database import get_connection

class CadastrarDados:
    
    @staticmethod
    def criar_usuario(LOGIN_USER, SENHA):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO USUARIO(LOGIN_USER, SENHA) VALUES (?, ?)", (LOGIN_USER, SENHA))
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