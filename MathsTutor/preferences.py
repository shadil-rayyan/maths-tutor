import sys
from PySide6 import QtCore, QtWidgets
import configparser

class Preferences(QtCore.QObject):

    def __init__(self):
        super().__init__()
        self.set_default_preferences()

    def set_default_preferences(self):
        self.operator = 0
        self.level = 0
        self.language = -1
        self.remember_language = 0
        self.speech_synthesizer = -1
        self.speech_language = -1
        self.speech_person = 0
        self.speech_rate = 50

    def load_preferences_from_file(self, filename):
        try:
            cp = configparser.ConfigParser()
            cp.read(filename)

            self.operator = int(cp.get('general', "operator"))
            self.level = int(cp.get('general', "level"))
            self.language = int(cp.get('general', "language"))
            self.remember_language = int(cp.get('general', "remember_language"))

            self.speech_synthesizer = int(cp.get('speech', "synthesizer"))
            self.speech_language = int(cp.get('speech', "language"))
            self.speech_person = int(cp.get('speech', "person"))
            self.speech_rate = int(cp.get('speech', "rate"))

            print(
                f"\n\n### Preferences loaded from {filename} ###\n"
                f"operator: {self.operator}\n"
                f"level: {self.level}\n"
                f"language: {self.language}\n"
                f"remember_language: {self.remember_language}\n"
                f"speech_synthesizer: {self.speech_synthesizer}\n"
                f"speech_language: {self.speech_language}\n"
                f"speech_person: {self.speech_person}\n"
                f"speech_rate: {self.speech_rate}\n\n"
            )

        except Exception as e:
            print("Configuration reading error:", e)
            self.set_default_preferences()

    def save_preferences_to_file(self, filename):
        cp = configparser.ConfigParser()

        cp.add_section('general')
        cp.add_section('speech')

        cp.set('general', "language", str(int(self.language)))
        cp.set('general', "operator", str(int(self.operator)))
        cp.set('general', "level", str(int(self.level)))
        cp.set('general', "remember_language", str(int(self.remember_language)))

        cp.set('speech', "synthesizer", str(int(self.speech_synthesizer)))
        cp.set('speech', "language", str(int(self.speech_language)))
        cp.set('speech', "person", str(int(self.speech_person)))
        cp.set('speech', "rate", str(int(self.speech_rate)))

        with open(filename, 'w') as configfile:
            cp.write(configfile)

        print(
            f"\n\n### Preferences saved to {filename} ###\n"
            f"operator: {self.operator}\n"
            f"level: {self.level}\n"
            f"language: {self.language}\n"
            f"remember_language: {self.remember_language}\n"
            f"speech_synthesizer: {self.speech_synthesizer}\n"
            f"speech_language: {self.speech_language}\n"
            f"speech_person: {self.speech_person}\n"
            f"speech_rate: {self.speech_rate}\n\n"
        )
