import mediapipe as mp
from mediapipe.tasks.python import vision



class ModeOrchestrator:
    def __init__(self):
        self.current_mode_index = 1
        self.main_menu = False
        self.main_menu_selection = 1
        self.main_menu_proc = False
        self.modes = ['Menu Mode', 'Display Mode', 'Chess Mode', 'Classifier Mode']


    def gesture_intake(self, result: vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms:int):
        
        print("callback activation")
        print(result)

        if result.gestures:
            print("found some gestures")
            gesture = result.gestures[0] 
            # TODO check the above works, the index should be wrong
            # for the above, somehow it grabs by the hand_index...idk
            #  gesture = recognition_result_list[0].gestures[hand_index]

            category_name = gesture[0].category_name

            print(category_name)
        
        print("exiting the callback")

    def handle_gesture(self, gesture):
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
        if self.current_mode_index == 1:
            # do some checks for display mode
            if gesture == 'Thumb Up':
                # should cycle through the displays
                #
                pass
            if gesture == 'Thumb Down': 
                # should cycle through the displays
                pass
        
        if self.current_mode_index == 2:
            if gesture == 'Point Up':

                pass

        if self.current_mode_index == 3:
            pass