from flask import Blueprint, render_template, request
from model.cadastroModel import CadastrarDados
import os
import traceback

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'view'))
cadPessoa_bp = Blueprint("cadastro", __name__, template_folder = template_dir)

@cadPessoa_bp.route("/")
def cadastro_user():
    return render_template("cadastroPessoaView.html")

@cadPessoa_bp.route("/cadUser", methods=["POST"])
def cadastrar():
    CPF = request.form["CPF"]
    RG = request.form["RG"]
    NOME = request.form["NOME"]
    TELEFONE = request.form["TELEFONE"]
    DT_NASC = request.form["DT_NASC"]
    EMAIL = request.form["EMAIL"]
    
    LOGIN_USER = request.form["LOGIN_USER"]
    SENHA = request.form["SENHA"]
    TIPO_USER = request.form["TIPO_USER"]
    
    CadastrarDados.criar_pessoa(CPF, RG, NOME, TELEFONE, DT_NASC, EMAIL, TIPO_USER)
    CadastrarDados.criar_usuario(LOGIN_USER, SENHA)
    
    return "Usuário cadastrado com sucesso!"
    