import mediapipe as mp
import time
import cv2

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# here we actually get the result and we need to somehow
    # use this to return the recognized gestures
    
    # we might be passing the function from the main.py and picking it up there
def callback(result: vision.GestureRecognizerResult, 
             output_image: mp.Image, timestamp_ms:int):

    if result.gestures:
        gesture = result.gestures[0] 
        # TODO check the above works, the index should be wrong
        # for the above, somehow it grabs by the hand_index...idk
        #  gesture = recognition_result_list[0].gestures[hand_index]

        category_name = gesture[0].category_name
    

class GestureInterpreter():
    def __init__(self, gesture_intake_function, interval = 1):
        self.interval = interval

        base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
        options = vision.GestureRecognizerOptions(base_options=base_options,
                                        running_mode=vision.RunningMode.LIVE_STREAM,
                                        num_hands=1,
                                          min_hand_detection_confidence=0.5,
                                          min_hand_presence_confidence=0.5,
                                          min_tracking_confidence=0.5,
                                        result_callback=gesture_intake_function)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    def process_frame(self, image):
        # TODO: add frame skipping logic here

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)    
        self.recognizer.recognize_async(mp_image, time.time_ns() // 1_000_000)
        self.generate_display()

    def generate_display(self):
        pass

    def close(self):
        self.recognizer.close()


