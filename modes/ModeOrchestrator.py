import mediapipe as mp
from mediapipe.tasks.python import vision



class ModeOrchestrator:
    def __init__(self):
        self.current_mode_index = 1
        self.main_menu = False
        self.proc = False
        self.modes = ['Display Mode', 'Chess Mode', 'Classifier Mode']


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

        
        

    # def process_gesture(self, gesture):
    #     if self.state == 'string_display_mode':
    #         self.handle_string_display_mode(gesture)
    #     elif self.state == 'chess_analysis_mode':
    #         self.handle_chess_analysis_mode(gesture)
    #     elif self.state == 'object_classification_mode':
    #         self.handle_object_classification_mode(gesture)
    #     elif self.state == 'menu_mode':
    #         self.handle_menu_mode(gesture)

    # def handle_string_display_mode(self, gesture):
    #     if gesture == 'fist':
    #         self.transition_to('menu_mode')
    #     elif gesture == 'victory':
    #         print("Confirm action in String Display Mode")

    # def handle_chess_analysis_mode(self, gesture):
    #     if gesture == 'fist':
    #         self.transition_to('menu_mode')
    #     elif gesture == 'victory':
    #         print("Confirm action in Chess Analysis Mode")

    # def handle_object_classification_mode(self, gesture):
    #     if gesture == 'fist':
    #         self.transition_to('menu_mode')
    #     elif gesture == 'victory':
    #         print("Confirm action in Object Classification Mode")

    # def handle_menu_mode(self, gesture):
    #     if gesture == 'down':
    #         self.scroll_menu('down')
    #     elif gesture == 'up':
    #         self.scroll_menu('up')
    #     elif gesture == 'victory':
    #         self.select_menu_option()

    # def transition_to(self, new_state):
    #     print(f"Transitioning to {new_state}")
    #     self.state = new_state

    # def scroll_menu(self, direction):
    #     if direction == 'down':
    #         self.selected_option = (self.selected_option + 1) % len(self.menu)
    #     elif direction == 'up':
    #         self.selected_option = (self.selected_option - 1) % len(self.menu)
    #     print(f"Menu Scrolled: {self.menu[self.selected_option]}")

    # def select_menu_option(self):
    #     print(f"Selected: {self.menu[self.selected_option]}")

# Example usage
# glasses = GlassesStateMachine()
# gestures = ['fist', 'down', 'down', 'victory']  # Simulated gestures
# for gesture in gestures:
#     glasses.process_gesture(gesture)
