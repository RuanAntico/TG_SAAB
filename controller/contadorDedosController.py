from flask import Blueprint, render_template, Response
from model.contadorDedosModel import count_fingers
import cv2
import os
import mediapipe as mp

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'view'))
contarDedos_bp = Blueprint("contador", __name__, template_folder = template_dir)

@contarDedos_bp.route('/')
def cont_dedo():
    return render_template('contadorDedosView.html')

@contarDedos_bp.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def generate_frames():
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

            # Adicionar texto
            cv2.putText(image, f'Dedos: {finger_count}', (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            if handedness_text:
                cv2.putText(image, f'Maos: {handedness_text}', (10, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            # Espelhar para visualização
            image = cv2.flip(image, 1)

            # Codificar como JPEG
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            # Stream no formato MJPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')