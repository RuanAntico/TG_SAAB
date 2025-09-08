
from flask import Flask
from controller.longinController import login_bp
from controller.contadorDedosController import contarDedos_bp
from database import criar_tab

criar_tab()

app = Flask(__name__)

# Middleware para evitar cache (vale para todas as rotas)
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Registrar o Blueprint
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(contarDedos_bp, url_prefix='/contador')

@app.route("/")
def root():
    from flask import redirect
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
