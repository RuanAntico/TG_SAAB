import sqlite3
from database import get_connection

class VerificarLog:
    @staticmethod
    def verificarLog(COD_USUARIO):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            print(f"Buscando usuário: {COD_USUARIO}")  # Debug
            
            # Verificar se a tabela existe
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='USUARIO'")
            tabela_existe = cursor.fetchone()
            
            if not tabela_existe:
                print("Tabela USUARIO não existe!")
                return None
            
            # Buscar usuário
            cursor.execute("SELECT * FROM USUARIO WHERE COD_USUARIO = ?", (COD_USUARIO,))
            usuario = cursor.fetchone()
            
            if usuario:
                print(f"Usuário encontrado: {usuario}")  # Debug
                # Converter para dicionário
                columns = [column[0] for column in cursor.description]
                usuario_dict = dict(zip(columns, usuario))
                return usuario_dict
            else:
                print("Usuário não encontrado no banco")  # Debug
                return None
                
        except Exception as e:
            print(f"Erro ao carregar usuario: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            if conn:
                conn.close()