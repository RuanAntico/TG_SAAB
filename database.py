import sqlite3
from flask import Blueprint, render_template, Response
import os
import bcrypt

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'view'))
database_bp = Blueprint("contador", __name__, template_folder=template_dir)

def get_connection():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    return conn

def criar_tab():
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS USUARIO (
        COD_USUARIO INTEGER PRIMARY KEY AUTOINCREMENT,
        LOGIN_USER TEXT UNIQUE,
        SENHA TEXT,
        TIPO_USER TEXT
    );

    CREATE TABLE IF NOT EXISTS PESSOA (
        COD_PESSOA INTEGER PRIMARY KEY AUTOINCREMENT,
        CPF INTEGER UNIQUE,
        RG INTEGER UNIQUE,
        NOME TEXT,
        TELEFONE INTEGER,
        DT_NASC DATE,
        EMAIL TEXT,
        COD_USUARIO INTEGER,
        FOREIGN KEY (COD_USUARIO) REFERENCES USUARIO(COD_USUARIO) 
    );

    CREATE TABLE IF NOT EXISTS PROFESSORA (
        COD_PROFESSORA INTEGER PRIMARY KEY AUTOINCREMENT,
        COD_PESSOA INTEGER,
        FOREIGN KEY (COD_PESSOA) REFERENCES PESSOA(COD_PESSOA) 
    );

    CREATE TABLE IF NOT EXISTS TURMA (
        COD_TURMA INTEGER PRIMARY KEY AUTOINCREMENT,
        TURMA TEXT NOT NULL,
        COD_PROFESSORA INTEGER,
        FOREIGN KEY (COD_PROFESSORA) REFERENCES PROFESSORA(COD_PROFESSORA)
    );

    CREATE TABLE IF NOT EXISTS ALUNO (
        COD_ALUNO INTEGER PRIMARY KEY AUTOINCREMENT,
        COD_TURMA INTEGER,
        FOREIGN KEY (COD_TURMA) REFERENCES TURMA(COD_TURMA)
    );

    CREATE TABLE IF NOT EXISTS PAIS (
        COD_PAI INTEGER PRIMARY KEY AUTOINCREMENT,
        COD_PESSOA INTEGER,
        COD_ALUNO INTEGER,
        FOREIGN KEY (COD_PESSOA) REFERENCES PESSOA(COD_PESSOA),
        FOREIGN KEY (COD_ALUNO) REFERENCES ALUNO(COD_ALUNO)
    );
    """)
    
    cursor.execute("SELECT 1 FROM USUARIO WHERE LOGIN_USER = ?", ("adm",))
    if cursor.fetchone() is None:
        senha_hash = bcrypt.hashpw("adm".encode("utf-8"), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO USUARIO (LOGIN_USER, SENHA) VALUES (?, ?)",
            ("adm", senha_hash)
        )

    conn.commit()
    conn.close()
