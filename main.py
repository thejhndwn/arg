from picamera2 import Picamera2
import numpy as np
from modes import GestureInterpreter


print("starting up...")
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={'size': (640, 480)}))
picam2.start()

gesture_interpreter = GestureInterpreter()




current_mode = "idle"

print("starting the loop")
while True:
    image = picam2.capture_array()
    gesture_interpreter.process_frame(image)

    print("restarting the loop")

    
cv2.destroyAllWindows()
picam2.stop()
