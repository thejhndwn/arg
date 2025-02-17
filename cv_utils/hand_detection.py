import cv2
import mediapipe as mp

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

def detect_hand_gesture(frame):
    # Convert the image to RGB (MediaPipe uses RGB)
    print("start detecting hands?")
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame and detect hands
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on the hand
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Analyze the hand (e.g., detect closed fist or fingers)
            # For now, just print the number of fingers (we'll add the logic next)
            fingers_up = count_fingers(hand_landmarks)
            cv2.putText(frame, f"Fingers: {fingers_up}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    return frame, fingers_up

def count_fingers(hand_landmarks):
    """ Count the number of fingers raised (very simple approach) """
    finger_tips = [8, 12, 16, 20]  # Index tips
    base = [5, 9, 13, 17]  # Base joints
    
    raised_fingers = 0
    for i, tip in enumerate(finger_tips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[base[i]].y:
            raised_fingers += 1
    return raised_fingers
