from flask import Blueprint, render_template, Response, jsonify
from model.contadorDedosModel import count_fingers
import cv2
import os
import mediapipe as mp
import random
import threading
import time

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'view'))
contarDedos_bp = Blueprint("contador", __name__, template_folder=template_dir)

# --- estado global visível ao front ---
pergunta_atual = None
resposta_correta = None
digito_unidade = None
acertou = False

# status expostos
current_finger_count = 0
current_status_text = "Aguardando..."
stream_ready = False
frame_count = 0

# MediaPipe helpers
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def gerarMultiplicacao():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    resultado = num1 * num2
    unidade = resultado % 10
    return num1, num2, resultado, unidade

def nova_pergunta():
    global pergunta_atual, resposta_correta, digito_unidade, acertou
    num1, num2, resultado, unidade = gerarMultiplicacao()
    if resultado >= 10:
        pergunta_atual = f"{num1} x {num2} = {str(resultado)[:1]}?"
    else:
        pergunta_atual = f"{num1} x {num2} = 0?"
    resposta_correta = resultado
    digito_unidade = unidade
    acertou = False

@contarDedos_bp.route('/')
def cont_dedo():
    nova_pergunta()
    return render_template('contadorDedosView.html')

@contarDedos_bp.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@contarDedos_bp.route('/status')
def status():
    # retorna JSON com o estado atual para o front-end
    return jsonify({
        "pergunta": pergunta_atual,
        "dedos": current_finger_count,
        "status": current_status_text,
        "stream_ready": stream_ready,
        "frame_count": frame_count
    })

def generate_frames():
    global pergunta_atual, resposta_correta, digito_unidade, acertou
    global current_finger_count, current_status_text, stream_ready, frame_count

    cap = cv2.VideoCapture(0)
    # opcional: reduzir resolução para performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=2) as hands:

        while True:
            success, image = cap.read()
            if not success:
                # pequena pausa pra evitar busy loop se falhar
                time.sleep(0.05)
                continue

            # marcamos que o stream já entregou um frame
            stream_ready = True
            frame_count += 1

            image = cv2.flip(image, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)

            finger_count = 0
            handedness_text = ""

            if results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    hand_label = handedness.classification[0].label
                    handedness_text = hand_label

                    # desenho (pode comentar se quiser performance)
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

                    finger_count += count_fingers(hand_landmarks, hand_label)

            # atualiza variáveis públicas usadas pelo front
            current_finger_count = finger_count

            # Lógica de status textual
            if finger_count == digito_unidade and not acertou:
                acertou = True
                current_status_text = "CORRETO!"
                # agenda nova pergunta sem travar o loop
                threading.Timer(3.5, nova_pergunta).start()
            elif acertou:
                current_status_text = "CORRETO!"
            elif finger_count > 0 and finger_count != digito_unidade:
                current_status_text = "Tente novamente!"
            else:
                current_status_text = "Aguardando..."

            # ** não desenhe texto dentro da imagem se você quer mostrar fora **
            # Se quiser manter, comente as linhas abaixo.
            # cv2.putText(image, f'Dedos: {finger_count}', (10, 70),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

            # Codificar como JPEG
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # se o with terminar, libera camera
    cap.release()
