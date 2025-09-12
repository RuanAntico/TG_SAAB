from flask import Blueprint, render_template, Response
from model.contadorDedosModel import count_fingers
import cv2
import os
import mediapipe as mp
import random

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'view'))
contarDedos_bp = Blueprint("contador", __name__, template_folder = template_dir)

# Variáveis globais para o jogo
pergunta_atual = None
resposta_correta = None
digito_unidade = None
acertou = False

def gerarMultiplicacao():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    
    resultado = num1 * num2
    # Pegar apenas o último dígito (unidade)
    digito_unidade = resultado % 10
    
    return num1, num2, resultado, digito_unidade

@contarDedos_bp.route('/')
def cont_dedo():
    global pergunta_atual, resposta_correta, digito_unidade, acertou
    
    # Gerar nova pergunta ao carregar a página
    num1, num2, resultado, unidade = gerarMultiplicacao()
    if resultado >=10:
        strResultado = str(resultado)
        strResultado = strResultado[:1]
        pergunta_atual = f"{num1} x {num2} = {strResultado}?"
    else:
        pergunta_atual = f"{num1} x {num2} = 0?"
    resposta_correta = resultado
    digito_unidade = unidade
    acertou = False
    
    return render_template('contadorDedosView.html')

@contarDedos_bp.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def generate_frames():
    global pergunta_atual, resposta_correta, digito_unidade, acertou
    
    cap = cv2.VideoCapture(0)
    
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=2) as hands:

        while True:
            success, image = cap.read()
            if not success:
                continue

            # Espelhar para visualização
            image = cv2.flip(image, 1)
            
            # Converter para RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)

            finger_count = 0
            handedness_text = ""

            if results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    # Determinar mão esquerda/direita
                    hand_label = handedness.classification[0].label
                    handedness_text = hand_label

                    # Desenhar landmarks
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

                    # Contar dedos
                    finger_count += count_fingers(hand_landmarks, hand_label)

            # Verificar se acertou o ÚLTIMO DÍGITO da multiplicação
            if finger_count == digito_unidade and not acertou:
                acertou = True
                # Gerar nova pergunta após 2 segundos
                def nova_pergunta():
                    global pergunta_atual, resposta_correta, digito_unidade, acertou
                    num1, num2, resultado, unidade = gerarMultiplicacao()
                    if resultado >=10:
                        strResultado = str(resultado)
                        strResultado = strResultado[:1]
                        pergunta_atual = f"{num1} x {num2} = {strResultado}?"
                    else:
                        pergunta_atual = f"{num1} x {num2} = 0?"
                    resposta_correta = resultado
                    digito_unidade = unidade
                    acertou = False
                
                # Usar thread ou timer para não travar o fluxo de vídeo
                import threading
                threading.Timer(2.0, nova_pergunta).start()

            # Adicionar textos na imagem
            # Pergunta
            cv2.putText(image, pergunta_atual, (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Contador de dedos
            cv2.putText(image, f'Dedos: {finger_count}', (10, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

            # Resposta completa e dígito da unidade (para debug/ajuda)
            cv2.putText(image, f'Resposta: {resposta_correta}', (10, 110), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(image, f'Mostre: {digito_unidade} (ultimo digito)', (10, 140), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2, cv2.LINE_AA)

            # Mensagem de acerto
            if acertou:
                cv2.putText(image, "CORRETO! 👍", (image.shape[1]//2 - 100, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_AA)
            elif finger_count > 0 and finger_count != digito_unidade:
                cv2.putText(image, "Tente novamente!", (image.shape[1]//2 - 100, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

            if handedness_text:
                cv2.putText(image, f'Maos: {handedness_text}', (10, 170), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

            # Codificar como JPEG
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            # Stream no formato MJPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')