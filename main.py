from picamera2 import Picamera2
import cv2
# from modes.display_mode import activate_display_mode
# from modes.chess_mode import activate_chess_mode
# from modes.object_classifier_mode import classify_object

# Initialize PiCamera2
print("starting up...")
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={'size': (640, 480)}))
picam2.start()

# current_mode = "idle"
# mode_functions = {
#     "display_mode": activate_display_mode,
#     "chess_mode": activate_chess_mode,
#     "object_classify_mode": classify_object,
# }

print("starting the loop")
while True:
    frame = picam2.capture_array()

    cv2.imshow("Captured Frame", frame)

    # intake the frame
    # frame should go through the interpreter of the chosen mode + the hand gesture model
    # results should be sent to the display generator
    # complete the loop





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