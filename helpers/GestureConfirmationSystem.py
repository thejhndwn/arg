from collections import Counter

class GestureConfirmationSystem:
    def __init__(self):
        self.gesture_history = []
        self.history_duration = 500  # seconds to track
        self.confirmation_threshold = 0.7  # percentage that must show target gesture
        
    def add_gesture_observation(self, detected_gesture, timestamp):
        current_time = timestamp
        
        # Update history - remove old entries
        self.gesture_history = [
            (g, t) for g, t in self.gesture_history 
            if current_time - t <= self.history_duration
        ]
        
        # Add new observation if not None
        # if detected_gesture:
        self.gesture_history.append((detected_gesture, current_time))
        
        # Calculate the majority gesture in the recent history
        if len(self.gesture_history) >= 3:  # Require at least a few observations
            gestures = [g for g, _ in self.gesture_history]
            gesture_counts = Counter(gestures)
            most_common = gesture_counts.most_common(1)[0]
            majority_gesture, count = most_common
            
            # Check if we have a clear majority
            if count / len(gestures) >= self.confirmation_threshold:
                 return majority_gesture
        
        return None
    
    def reset(self):
        self.gesture_history = []