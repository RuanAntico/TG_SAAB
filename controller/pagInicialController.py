from flask import Blueprint, render_template, request, redirect, url_for, session
from model.pagInicialModel import VerificarLog
import os

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'view'))
pagInicial_bp = Blueprint("pagInicial", __name__, template_folder=template_dir)

@pagInicial_bp.route("/")
def pagina():

    if 'COD_USER' in session:
        user_id_logado = session['COD_USER']
        usuario_logado = VerificarLog.verificarLog(user_id_logado)
        
        if usuario_logado:
            return render_template('pagInicialView.html', usuario=usuario_logado)
        else:
            session.clear()
    

    return render_template("loginView.html")

@pagInicial_bp.route("/login/auth", methods=["GET", "POST"])
def pagina1():
    try:
        if request.method == "POST":
            COD_USER = request.form.get("COD_USER", "").strip()
            
            if not COD_USER:
                return render_template("loginView.html", erro="Código de usuário é obrigatório")
            
    
            usuario = VerificarLog.verificarLog(COD_USER)
            print(f"Usuário válido? {usuario is not None}")
            
            if usuario:

                session['COD_USER'] = COD_USER
                session['user_info'] = usuario
                print(f"Login bem-sucedido para usuário: {COD_USER}")
                return redirect(url_for('pagInicial.pagina'))
            else:
                return render_template("loginView.html", erro="Usuário não encontrado")
        
        return redirect(url_for('pagInicial.pagina'))
        
    except Exception as e:
        print(f"Erro interno: {str(e)}")  
        import traceback
        traceback.print_exc()
        return render_template("loginView.html", erro="Erro interno do sistema")

@pagInicial_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('pagInicial.pagina'))