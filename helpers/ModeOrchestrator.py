from helpers import GestureConfirmationSystem
import mediapipe as mp
from mediapipe.tasks.python import vision
import time
from helpers import DisplayManager
from modes import DisplayInterpreter



class ModeOrchestrator:
    def __init__(self):
        self.current_mode_index = 1
        self.main_menu_selection = 1
        self.main_menu_proc = False
        self.menu = ['Menu Mode', 'Display Mode', 'Chess Mode', 'Classifier Mode']
        self.gesture_confirmation_system = GestureConfirmationSystem()
        self.display_manager = DisplayManager()
        self.display_interpreter = DisplayInterpreter()
        self.display_index = 0

        self.last_gesture_time = None

    def gesture_intake(self, result: vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms:int):
        

        if result.gestures:
            gesture_object = result.gestures[0] 
            # TODO check the above works, the index should be wrong
            # for the above, somehow it grabs by the hand_index...idk
            #  gesture = recognition_result_list[0].gestures[hand_index]

            gesture = gesture_object[0].category_name
            aggregated_gesture = self.gesture_confirmation_system.add_gesture_observation(gesture, timestamp_ms)

            self.handle_gesture(aggregated_gesture)
        else:
            print("no hand found")
            # no gesture was found but it might be that we're looking
            # for a chessboard or an object to classify
            pass

    def gen_main_menu(self, menu_list, selection, marker = ">"):
        menu_list = menu_list[1:]

        if 0 <= selection < len(menu_list):
            menu_list[selection] = f"{marker}{menu_list[selection]}"
        
        return "\n".join(menu_list)
        

    def handle_gesture(self, gesture):
        current_time = time.time()
        if self.last_gesture_time:
            if current_time - self.last_gesture_time > .500:
                self.last_gesture_time = current_time
            else:
                return
        else: 
            self.last_gesture_time = current_time

        print("received the gesture after timing stuff: ", gesture)



        # TODO: add frame and gesture debouncing
        if gesture == 'ILoveYou':
            self.main_menu_proc = True
            self.display_manager.display_text("main menu proc sign")

        elif gesture == 'Victory' and self.main_menu_proc:
            self.main_menu_proc = False
            self.current_mode_index = 0

            menu_str = self.gen_main_menu(self.menu, self.main_menu_selection)
            print(menu_str)
            self.display_manager.display_text(menu_str)
        
        elif self.current_mode_index == 0:
            # we are in the main menu and need to process the gestures
            if gesture == 'Thumb_Up':
                # move the selection up
                self.main_menu_selection -=1 
                if self.main_menu_selection == 0:
                    self.main_menu_selection = 3
                self.display_manager.display_text(self.gen_main_menu(self.menu, self.main_menu_selection))

            elif gesture == 'Thumb_Down':
                # move the selection down
                self.main_menu_selection +=1
                if self.main_menu_selection == len(self.menu):
                    self.main_menu_selection = 1
                self.display_manager.display_text(self.gen_main_menu(self.menu, self.main_menu_selection))

            elif gesture == 'Victory':
                # confirm
                self.current_mode_index = self.main_menu_selection
                self.display_manager.display_text(self.menu[self.current_mode_index])

        # TODO: figure out the display logic
        # just doing a simple static display for now, so nothing has to happen here
        # STATIC DISPLAY
        elif self.current_mode_index == 1:
            # do some checks for display mode
            if gesture == 'Thumb_Up':
                self.display_index +=1
                if self.display_index == len(self.display_interpreter.display_strings):
                    self.display_index = 0
                self.display_manager.display_text(self.display_interpreter.display_string(self.display_index))
            if gesture == 'Thumb_Down': 
                # should cycle through the displays
                if self.display_index == -1:
                    self.display_index = len(self.display_interpreter.display_strings) - 1
                self.display_manager.display_text(self.display_interpreter.display_string(self.display_index))
        
        # CHESS MODE
        elif self.current_mode_index == 2:
            if gesture == 'Pointing_Up':
                self.display_manager.display_text("chess mode proc'd")
                pass

        # OBJECT RECOGNITION
        elif self.current_mode_index == 3:
            if gesture == 'Pointing_Up':
                self.display_manager.display_text("object mode proc'd")
                pass

