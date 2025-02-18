from picamera2 import Picamera2
import time
import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


print("starting up...")
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={'size': (640, 480)}))
picam2.start()

# Global variables to calculate FPS
COUNTER, FPS = 0, 0 # Visualization parameters
row_size = 50  # pixels
left_margin = 24  # pixels
text_color = (0, 0, 0)  # black
font_size = 1
font_thickness = 1
fps_avg_frame_count = 10

# Label box parameters
label_text_color = (255, 255, 255)  # white
label_font_size = 1
label_thickness = 2

START_TIME = time.time()
recognition_frame = None
recognition_result_list = []
def save_result(result: vision.GestureRecognizerResult,
                  unused_output_image: mp.Image, timestamp_ms: int):
      global FPS, COUNTER, START_TIME

      # Calculate the FPS
      if COUNTER % fps_avg_frame_count == 0:
          FPS = fps_avg_frame_count / (time.time() - START_TIME)
          START_TIME = time.time()

      recognition_result_list.append(result)
      COUNTER += 1

base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options,
                                        running_mode=vision.RunningMode.LIVE_STREAM,
                                        num_hands=1,
                                          min_hand_detection_confidence=0.5,
                                          min_hand_presence_confidence=0.5,
                                          min_tracking_confidence=0.5,
                                        result_callback=save_result)
recognizer = vision.GestureRecognizer.create_from_options(options)


current_mode = "idle"

print("starting the loop")
while True:
    image = picam2.capture_array()

    # Convert the image from BGR to RGB as required by the TFLite model
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)    

    # we should always be doing the hand checking
    # hand checking overrides everythinig
    # TODO: add hand-checking stuff here
    hand_recognition_result = recognizer.recognize_async(mp_image, time.time_ns() // 1_000_000)
    
    print(hand_recognition_result)
    
    
    # Show the FPS
    fps_text = 'FPS = {:.1f}'.format(FPS)
    text_location = (left_margin, row_size)
    current_frame = image
    cv2.putText(current_frame, fps_text, text_location, cv2.FONT_HERSHEY_DUPLEX,
                font_size, text_color, font_thickness, cv2.LINE_AA)

    if recognition_result_list:
      # Draw landmarks and write the text for each hand.
      for hand_index, hand_landmarks in enumerate(
          recognition_result_list[0].hand_landmarks):
        # Calculate the bounding box of the hand
        x_min = min([landmark.x for landmark in hand_landmarks])
        y_min = min([landmark.y for landmark in hand_landmarks])
        y_max = max([landmark.y for landmark in hand_landmarks])

        # Convert normalized coordinates to pixel values
        frame_height, frame_width = current_frame.shape[:2]
        x_min_px = int(x_min * frame_width)
        y_min_px = int(y_min * frame_height)
        y_max_px = int(y_max * frame_height)

        # Get gesture classification results
        if recognition_result_list[0].gestures:
          gesture = recognition_result_list[0].gestures[hand_index]
          category_name = gesture[0].category_name
          score = round(gesture[0].score, 2)
          result_text = f'{category_name} ({score})'

          # Compute text size
          text_size = \
          cv2.getTextSize(result_text, cv2.FONT_HERSHEY_DUPLEX, label_font_size,
                          label_thickness)[0]
          text_width, text_height = text_size

          # Calculate text position (above the hand)
          text_x = x_min_px
          text_y = y_min_px - 10  # Adjust this value as needed

          # Make sure the text is within the frame boundaries
          if text_y < 0:
            text_y = y_max_px + text_height

          # Draw the text
          cv2.putText(current_frame, result_text, (text_x, text_y),
                      cv2.FONT_HERSHEY_DUPLEX, label_font_size,
                      label_text_color, label_thickness, cv2.LINE_AA)

        # Draw hand landmarks on the frame
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
          landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y,
                                          z=landmark.z) for landmark in
          hand_landmarks
        ])
        try:
            mp_drawing.draw_landmarks(
              current_frame,
              hand_landmarks_proto,
              mp_hands.HAND_CONNECTIONS,
              mp_drawing_styles.get_default_hand_landmarks_style(),
              mp_drawing_styles.get_default_hand_connections_style())
        except:
            print("failure, showing image")
            cv2.imshow('failed image', current_frame)

      recognition_frame = current_frame
      print(recognition_result_list)
      recognition_result_list.clear()

    if recognition_frame is not None:
        cv2.imshow('gesture_recognition', recognition_frame)

    # Stop the program if q key is pressed
    if cv2.waitKey(0) == ord('q'):
        break
        
recognizer.close()
cv2.destroyAllWindows()
picam2.stop()
