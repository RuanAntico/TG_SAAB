import pyodbc  # Importe a biblioteca pyodbc em vez de sqlite3
from flask import Blueprint, render_template, Response
import os
import bcrypt

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'view'))
database_bp = Blueprint("contador", __name__, template_folder=template_dir)

def get_connection():
    # Substitua com os detalhes do seu servidor, banco de dados, usuário e senha
    # É necessário ter o driver ODBC para SQL Server instalado na máquina
    conn_str = (
        r'Driver={ODBC Driver 17 for SQL Server};'
        r'Server=DESKTOP-Q1GPVLA;'
        r'Database=SAAB_Database;'
        r'Uid=saab_user;'
        r'Pwd=Saab@123;'
    )
    conn = pyodbc.connect(conn_str)
    return conn

def criar_tab():
    conn = get_connection()
    cursor = conn.cursor()
    
    # OBS: executescript não existe no pyodbc, então cada comando é executado separadamente.
    # A sintaxe SQL foi ajustada para o SQL Server.

    # Tabela USUARIO
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[USUARIO]') AND type in (N'U'))
    CREATE TABLE USUARIO (
        COD_USUARIO INT PRIMARY KEY IDENTITY(1,1),
        LOGIN_USER NVARCHAR(100) UNIQUE,
        SENHA NVARCHAR(255),
        TIPO_USER NVARCHAR(50)
    );
    """)

    # Tabela PESSOA
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[PESSOA]') AND type in (N'U'))
    CREATE TABLE PESSOA (
        COD_PESSOA INT PRIMARY KEY IDENTITY(1,1),
        CPF BIGINT UNIQUE,
        RG BIGINT UNIQUE,
        NOME NVARCHAR(255),
        TELEFONE BIGINT,
        DT_NASC DATE,
        EMAIL NVARCHAR(255),
        COD_USUARIO INT,
        FOREIGN KEY (COD_USUARIO) REFERENCES USUARIO(COD_USUARIO) 
    );
    """)

    # Tabela PROFESSORA
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[PROFESSORA]') AND type in (N'U'))
    CREATE TABLE PROFESSORA (
        COD_PROFESSORA INT PRIMARY KEY IDENTITY(1,1),
        COD_PESSOA INT,
        FOREIGN KEY (COD_PESSOA) REFERENCES PESSOA(COD_PESSOA) 
    );
    """)

    # Tabela TURMA
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[TURMA]') AND type in (N'U'))
    CREATE TABLE TURMA (
        COD_TURMA INT PRIMARY KEY IDENTITY(1,1),
        TURMA NVARCHAR(100) NOT NULL,
        COD_PROFESSORA INT,
        FOREIGN KEY (COD_PROFESSORA) REFERENCES PROFESSORA(COD_PROFESSORA)
    );
    """)

    # Tabela ALUNO
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ALUNO]') AND type in (N'U'))
    CREATE TABLE ALUNO (
        COD_ALUNO INT PRIMARY KEY IDENTITY(1,1),
        COD_TURMA INT,
        COD_PESSOA INT,
        FOREIGN KEY (COD_TURMA) REFERENCES TURMA(COD_TURMA),
        FOREIGN KEY (COD_PESSOA) REFERENCES PESSOA(COD_PESSOA)
    );
    """)
    
    # Tabela PAIS
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[PAIS]') AND type in (N'U'))
    CREATE TABLE PAIS (
        COD_PAI INT PRIMARY KEY IDENTITY(1,1),
        COD_PESSOA INT,
        COD_ALUNO INT,
        FOREIGN KEY (COD_PESSOA) REFERENCES PESSOA(COD_PESSOA),
        FOREIGN KEY (COD_ALUNO) REFERENCES ALUNO(COD_ALUNO)
    );
    """)

    # Lógica para inserir o usuário 'adm' se não existir
    cursor.execute("SELECT 1 FROM USUARIO WHERE LOGIN_USER = ?", ("adm",))
    if cursor.fetchone() is None:
        # LINHA ORIGINAL (gera bytes)
        # senha_hash = bcrypt.hashpw("adm".encode("utf-8"), bcrypt.gensalt())

        # CÓDIGO CORRIGIDO (gera bytes e depois decodifica para string)
        senha_hash_bytes = bcrypt.hashpw("adm".encode("utf-8"), bcrypt.gensalt())
        senha_hash_string = senha_hash_bytes.decode("utf-8") # <-- A MÁGICA ESTÁ AQUI

        cursor.execute(
            "INSERT INTO USUARIO (LOGIN_USER, SENHA) VALUES (?, ?)",
            # Use a versão em string para inserir no banco
            ("adm", senha_hash_string)
        )

    conn.commit()
    conn.close()