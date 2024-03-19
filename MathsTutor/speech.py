import pyttsx3

class Speech:
    def __init__(self):
        self.engine = pyttsx3.init()  # Initialize pyttsx3 engine
    
    def say(self, text):
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()  # Ensure speech finishes before continuing

    def set_speech_rate(self, speech_rate):
        # pyttsx3 doesn't have a direct speech_rate property, but you can adjust rate
        if 0 <= speech_rate <= 100:
            # Adjust rate based on speech_rate (example)
            self.engine.setProperty('rate', speech_rate * 1.5)  # Increase rate for faster speech


