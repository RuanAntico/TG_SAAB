from flask import Blueprint, render_template, request
from model.loginModel import UserLogin
import os

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'view'))
login_bp = Blueprint("login", __name__, template_folder = template_dir)

@login_bp.route("/")
def login():
    return render_template("loginView.html")    

@login_bp.route("/auth", methods=["GET", "POST"])
def login_post():
    try:
        LOGIN_USER = request.form.get("LOGIN_USER", "").strip()
        SENHA = request.form.get("SENHA", "").strip()
        if LOGIN_USER and SENHA:
            usuario_valido = UserLogin.Autenticar_Login(LOGIN_USER, SENHA)
            print(f"Usuário válido? {usuario_valido}")
        
        if usuario_valido:
            return render_template("pagInicialView.html")
        else:
            return render_template("loginView.html", erro="Preencha todos os campos")
      
    except Exception as e:
         print(f"Erro interno: {str(e)}")  
         return render_template("loginView.html", erro="Erro interno do sistema")
     
@login_bp.route("/pagInicialView.html")
def pagInicialView():
    return render_template("pagInicialView.html")
