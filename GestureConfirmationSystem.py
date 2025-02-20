class GestureConfirmationSystem:
    def __init__(self):
        self.gesture_history = []
        self.history_duration = 0.5  # seconds to track
        self.confirmation_threshold = 0.7  # percentage of frames that must show target gesture
        self.timeout_duration = 5.0  # seconds to look for the sustained gesture
        
        self.current_gesture = None
        self.gesture_start_time = None
        self.timeout_start_time = None
    
    def add_gesture_observation(self, detected_gesture, timestamp):
        current_time = timestamp
        
        # Initialize timeout period if this is a new gesture detection session
        if self.timeout_start_time is None:
            self.timeout_start_time = current_time
        
        # Check if we've exceeded the timeout window
        if current_time - self.timeout_start_time > self.timeout_duration:
            self.reset()
            return None
        
        # Update history - remove old entries
        self.gesture_history = [
            (g, t) for g, t in self.gesture_history 
            if current_time - t <= self.history_duration
        ]
        
        # Add new observation
        self.gesture_history.append((detected_gesture, current_time))
        
        # Calculate the majority gesture in the recent history
        if len(self.gesture_history) >= 3:  # Require at least a few observations
            gestures = [g for g, _ in self.gesture_history]
            gesture_counts = Counter(gestures)
            most_common = gesture_counts.most_common(1)[0]
            majority_gesture, count = most_common
            
            # Check if we have a clear majority
            if count / len(gestures) >= self.confirmation_threshold:
                duration = current_time - min([t for g, t in self.gesture_history if g == majority_gesture])
                
                # Check if held for required duration
                if duration >= self.history_duration:
                    self.reset()
                    return majority_gesture
        
        return None
    
    def reset(self):
        self.gesture_history = []
        self.timeout_start_time = None


# ### proposed usage in main

# gesture_system = GestureConfirmationSystem()
# last_processed_time = 0
# process_interval = 0.1  # seconds between gesture processing (frame skipping)

# while True:
#     frame = camera.read()
#     current_time = time.time()
    
#     # Skip some frames for efficiency
#     if current_time - last_processed_time < process_interval:
#         continue
    
#     last_processed_time = current_time
#     detected_gesture = gesture_recognizer.detect(frame)
    
#     # Add to our confirmation system
#     confirmed_gesture = gesture_system.add_gesture_observation(detected_gesture, current_time)
    
#     if confirmed_gesture:
#         print(f"Confirmed gesture: {confirmed_gesture}")
#         # Take action based on confirmed gesture
#         if confirmed_gesture == "CAPTURE_CHESS":
#             process_chess_board(frame)