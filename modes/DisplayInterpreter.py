class DisplayInterpreter():
    def __init__(self):
        self.display_index = 0
        self.display_strings = [
            "It's over 9000",
            "Believe it!",
            "Bazinga"
        ]
    def display_string(self, index):
        return self.display_strings[index]
