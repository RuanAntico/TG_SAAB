import cv2
import mediapipe as mp


# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def count_fingers(hand_landmarks, hand_label):
    """
    Conta quantos dedos estão levantados com base nos landmarks da mão
    """
    finger_tips = [mp_hands.HandLandmark.INDEX_FINGER_TIP, 
                   mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                   mp_hands.HandLandmark.RING_FINGER_TIP,
                   mp_hands.HandLandmark.PINKY_TIP]
    
    finger_pips = [mp_hands.HandLandmark.INDEX_FINGER_PIP, 
                   mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
                   mp_hands.HandLandmark.RING_FINGER_PIP,
                   mp_hands.HandLandmark.PINKY_PIP]
    
    thumb_tip = mp_hands.HandLandmark.THUMB_TIP
    thumb_ip = mp_hands.HandLandmark.THUMB_IP
    
    count = 0
    
    # Verificar polegar
    if hand_label == "Left":
        if hand_landmarks.landmark[thumb_tip].x > hand_landmarks.landmark[thumb_ip].x:
            count += 1
    else:
        if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_ip].x:
            count += 1
    
    # Verificar outros dedos
    for tip, pip in zip(finger_tips, finger_pips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            count += 1
    
    return count

