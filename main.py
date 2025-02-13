import cv2
from cv_utils.hand_detection import detect_hand_gesture
from modes.display_mode import activate_display_mode
from modes.chess_mode import activate_chess_mode
from modes.object_classify_mode import classify_object

# Initialize video capture
cap = cv2.VideoCapture(0)
current_mode = "idle"
mode_functions = {
    "display_mode": activate_display_mode,
    "chess_mode": activate_chess_mode,
    "object_classify_mode": classify_object,
}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect hand gestures and get the number of fingers raised
    frame, fingers_up = detect_hand_gesture(frame)

    if fingers_up == 0:
        current_mode = "main_menu"
    
    if current_mode == "main_menu":
        print("Main Menu: Show fingers to select mode.")
        if fingers_up == 1:
            current_mode = "display_mode"
        elif fingers_up == 2:
            current_mode = "chess_mode"
        elif fingers_up == 3:
            current_mode = "object_classify_mode"

    # Activate the selected mode
    frame = mode_functions.get(current_mode, lambda x: x)(frame)

    # Show the video feed with overlay
    cv2.imshow('Gesture Controlled Glasses', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
