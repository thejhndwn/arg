from picamera2 import Picamera2
import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


print("starting up...")
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={'size': (640, 480)}))
picam2.start()

base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)


current_mode = "idle"

print("starting the loop")
while True:
    frame = picam2.capture_array()

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    cv2.imshow("Captured Frame", frame)

    # we should always be doing the hand checking
    # hand checking overrides everythinig
    # TODO: add hand-checking stuff here
    hand_recognition_result = recognizer.recognize(mp_image)
    print(hand_recognition_result)



    # otherwise we feed through to whatever the given mode is
    # TODO: add mode-specific checking here

    # results should be sent to the display generator
    # TODO: add results here





#     cv2.imshow("camera feed", frame)
    
#     # Detect hand gestures and get the number of fingers raised
#     # frame, fingers_up = detect_hand_gesture(frame)

#     if fingers_up == 0:
#         current_mode = "main_menu"
    
#     if current_mode == "main_menu":
#         print("Main Menu: Show fingers to select mode.")
#         if fingers_up == 1:
#             current_mode = "display_mode"
#         elif fingers_up == 2:
#             current_mode = "chess_mode"
#         elif fingers_up == 3:
#             current_mode = "object_classify_mode"
    
#     # Activate the selected mode
#     frame = mode_functions.get(current_mode, lambda x: x)(frame)

#     # Show the video feed with overlay
#     cv2.imshow('Gesture Controlled Glasses', frame)
    
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

cv2.destroyAllWindows()
picam2.stop()