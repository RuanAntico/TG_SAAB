
from flask import Blueprint, render_template, session, request
import random
import os
from model.atividadesModel import gerar_pergunta_soma, gerar_pergunta_subtracao, gerar_opcoes

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'view'))
image_routes = Blueprint("atividades", __name__, template_folder = template_dir)

MAX_QUESTIONS = 10

@image_routes.route("/")
def index():

    current_num = session.get('question_number', 1)
    current_score = session.get('score', 0)

    last_answer = request.args.get('answered')
    if last_answer == 'correct':
        current_score += 1
    
 
    if current_num > MAX_QUESTIONS:
        mensagem_final = f"Fim de jogo! Você acertou {current_score} de {MAX_QUESTIONS}."
        
        # --- CORREÇÃO AQUI ---
        # Em vez de limpar TUDO, remove apenas as chaves do jogo.
        # Isso mantém o 'COD_USER' (login) intacto.
        session.pop('question_number', None)
        session.pop('score', None)
        # ---------------------
        
        # Envia para o template (que mostrará o bloco {% if mensagem %})
        return render_template("atividadesView.html", mensagem=mensagem_final)

    question_info = f"Questão {current_num} de {MAX_QUESTIONS}"
    score_info = f"Acertos: {current_score}"

    session['question_number'] = current_num + 1
    session['score'] = current_score

    geradores = [gerar_pergunta_soma, gerar_pergunta_subtracao]
    funcao_escolhida = random.choice(geradores)
    questao = funcao_escolhida()
    opcoes = gerar_opcoes(questao["resposta"])
    questao["opcoes"] = opcoes

    return render_template(
        "atividadesView.html",
        questao=questao,
        question_info=question_info,
        score_info=score_info
    )