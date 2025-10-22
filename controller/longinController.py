from flask import Blueprint, render_template, request, redirect, url_for, session
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
            
            usuario_dict = UserLogin.Autenticar_Login(LOGIN_USER, SENHA)
           
            if usuario_dict:
                

                try:

                    user_id_numerico = usuario_dict['COD_USUARIO']

                    session['COD_USER'] = user_id_numerico

                    url_destino = url_for('pagInicial.pagina')
                    return redirect(url_destino)

                except (KeyError, TypeError):
                    return render_template("loginView.html", erro="Erro de configuração do Model")
            else:
                return render_template("loginView.html", erro="Login ou senha inválidos")
        
        else:
            return render_template("loginView.html", erro="Preencha todos os campos")
    
    except Exception as e:
       print(f"!!! ERRO FATAL no try/except !!!: {str(e)}")
       import traceback
       traceback.print_exc()
       print("="*50 + "\n")
       return render_template("loginView.html", erro="Erro interno do sistema")