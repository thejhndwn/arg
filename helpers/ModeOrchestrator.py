from helpers import GestureConfirmationSystem
import mediapipe as mp
from mediapipe.tasks.python import vision
import time



class ModeOrchestrator:
    def __init__(self):
        self.current_mode_index = 1
        self.main_menu = False
        self.main_menu_selection = 1
        self.main_menu_proc = False
        self.modes = ['Menu Mode', 'Display Mode', 'Chess Mode', 'Classifier Mode']
        self.gesture_confirmation_system = GestureConfirmationSystem()

        self.last_gesture_time = None

    def gesture_intake(self, result: vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms:int):
        

        if result.gestures:
            gesture_object = result.gestures[0] 
            # TODO check the above works, the index should be wrong
            # for the above, somehow it grabs by the hand_index...idk
            #  gesture = recognition_result_list[0].gestures[hand_index]

            gesture = gesture_object[0].category_name
            aggregated_gesture = self.gesture_confirmation_system.add_gesture_observation(gesture, timestamp_ms)
            print("aggregated gesture: ", aggregated_gesture, "and normal: ", gesture)

            self.handle_gesture(aggregated_gesture)
        else:
            print("no hand found")
            # no gesture was found but it might be that we're looking
            # for a chessboard or an object to classify
            pass
        

    def handle_gesture(self, gesture):
        current_time = time.time()

        if self.last_gesture_time:
            if current_time - self.last_gesture_time > 1:
                self.last_gesture_time = current_time
            else:
                return
        else: 
            self.last_gesture_time = current_time



        # TODO: add frame and gesture debouncing
        if gesture == 'Love':
            self.main_menu_proc = True
            # TODO: display the main menu proc sign

        elif gesture == 'Victory' and self.main_menu_proc:
            self.main_menu = True 
            self.main_menu_proc = False
            self.current_mode_index = 0
            # TODO: open the Main menu
        
        elif self.current_mode_index == 0:
            # we are in the main menu and need to process the gestures
            if gesture == 'Thumb Up':
                # move the selection up
                self.main_menu_selection -=1 
                if self.main_menu_selection == 0:
                    self.main_menu_selection = 3
            if gesture == 'Thumb Down':
                # move the selection down
                self.main_menu_selection +=1
                if self.main_menu_selection == len(self.modes):
                    self.main_menu_selection = 1
            if gesture == 'Victory':
                # confirm
                self.current_mode_index = self.main_menu_selection
                # TODO: handle change to current mode

        # TODO: figure out the display logic
        # just doing a simple static display for now, so nothing has to happen here
        # STATIC DISPLAY
        elif self.current_mode_index == 1:
            # do some checks for display mode
            if gesture == 'Thumb Up':
                # should cycle through the displays
                #
                pass
            if gesture == 'Thumb Down': 
                # should cycle through the displays
                pass
        
        # CHESS MODE
        elif self.current_mode_index == 2:
            if gesture == 'Point Up':
                # chess analyzer is proc'ed
                pass

        # OBJECT RECOGNITION
        elif self.current_mode_index == 3:
            if gesture == 'Point Up':
                # classifer is proc'ed
                pass

