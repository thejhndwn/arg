from picamera2 import Picamera2
import numpy as np
from modes import GestureInterpreter
from helpers import ModeOrchestrator
from helpers import DisplayManager


print("starting up...")
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={'size': (640, 480)}))
picam2.start()

mode_orchestrator = ModeOrchestrator()
gesture_interpreter = GestureInterpreter(mode_orchestrator.gesture_intake)
display_manager = DisplayManager()
display_manager.display_text('Jingang')


frame_count = 0

print("starting the loop")
while True:
    image = picam2.capture_array()
    gesture_interpreter.process_frame(image)


display_manager.close()
gesture_interpreter.close()
cv2.destroyAllWindows()
picam2.stop()
