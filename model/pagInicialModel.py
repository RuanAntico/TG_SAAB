import sqlite3
from database import get_connection

class VerificarLog:
    @staticmethod
    def verificarLog(COD_USUARIO):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql = """
                SELECT U.*, P.NOME 
                FROM USUARIO U
                LEFT JOIN PESSOA P ON U.COD_USUARIO = P.COD_USUARIO
                WHERE U.COD_USUARIO = ?
            """
            cursor.execute(sql, (COD_USUARIO,))
            usuario = cursor.fetchone()
            
            if usuario: 
                columns = [column[0] for column in cursor.description]
                usuario_dict = dict(zip(columns, usuario))
                return usuario_dict
            else:
                return None
                
        except Exception as e:
            print(f"Erro ao carregar usuario: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            if conn:
                conn.close()