import sys
import webbrowser
import os
import threading
import pygame
import pyttsx3
import gettext
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QCheckBox, QMainWindow, QWidget, QBoxLayout, QMessageBox, QFileDialog
from PySide6.QtGui import QIcon, QPixmap
from PySide6 import QtGui, QtCore
import global_var
import preferences
#import Qt

DEFAULT_PREFS_DIR = 'D:\shadil\zendalona\qt\MathsTutor\preferences.py'

home_dir = os.environ.get('HOME', DEFAULT_PREFS_DIR)

if sys.platform.startswith('win'):
    app_data_dir = os.getenv('APPDATA')
    if app_data_dir is None:
        app_data_dir = os.path.expanduser("~")
    prefs_dir = os.path.join(app_data_dir, 'maths-tutor')
else:
    prefs_dir = os.path.expanduser("~/.maths-tutor")

os.makedirs(prefs_dir, exist_ok=True)

user_preferences_file_path = os.path.join(prefs_dir, 'prefs.cfg')

class LanguageSelectionDialog(QDialog):
    def __init__(self, parent=None, language=0):
        super().__init__(parent)
        self.setWindowTitle("Maths-Tutor")
        language_dict = {"en": "English", "fr": "French", "es": "Spanish"}  

        self.setWindowIcon(QIcon("path/to/icon.png"))
        self.resize(200, 150)

        label_language = QLabel("Select Language")
        self.combobox = QComboBox()
        for item in language_dict.values():
            self.combobox.addItem(item)
        self.combobox.setCurrentIndex(language)  
        hbox1 = QHBoxLayout()
        hbox1.addWidget(label_language)
        hbox1.addWidget(self.combobox)

        self.remember_checkbox = QCheckBox("Remember Selection")

        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addWidget(self.remember_checkbox)

        self.setLayout(layout)

class SelectGame(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Start pygame in a separate thread
        pygame_thread = threading.Thread(target=self.initialize_pygame)
        pygame_thread.start()

        # User Preferences
        self.pref = preferences.Preferences()
        self.pref.load_preferences_from_file(global_var.user_preferences_file_path)

        # Store the previous language for checking if a speech synthesizer
        # or language change is needed.
        previous_language = self.pref.language

        if self.pref.language == -1:
            self.pref.language = 0

        if self.pref.remember_language == 1:
            language_dict = {"en": "English", "fr": "French", "es": "Spanish"} 
            selected_language = list(language_dict)[self.pref.language]
        else:
            lang_dialog = LanguageSelectionDialog(self, self.pref.language)
            response = lang_dialog.exec()

            if response == 1:  
                active = lang_dialog.combobox.currentIndex()
                selected_language = list(language_dict)[active]
                self.pref.language = active
                if lang_dialog.remember_checkbox.isChecked():
                    self.pref.remember_language = 1
            else:
                return

            lang_dialog.close()

        try:
            lang1 = gettext.translation(global_var.app_name, languages=[selected_language])
            lang1.install()
            global _;
            _ = lang1.gettext
        except:
            self.pref.language = 0

        if previous_language != self.pref.language:
            self.pref.speech_language = -1

        self.operator_mapping = {
            _('Addition (+)'): {
                _('Simple'): 'add_simple.txt',
                _('Easy'): 'add_easy.txt',
                _('Medium'): 'add_med.txt',
                _('Hard'): 'add_hard.txt',
                _('Challenging'): 'add_chlg.txt',
            },
            _('Subtraction (-)'): {
                _('Simple'): 'sub_simple.txt',
                _('Easy'): 'sub_easy.txt',
                _('Medium'): 'sub_med.txt',
                _('Hard'): 'sub_hard.txt',
                _('Challenging'): 'sub_chlg.txt',
            },
            _('Multiplication (*)'): {
                _('Simple'): 'mul_simple.txt',
                _('Easy'): 'mul_easy.txt',
                _('Medium'): 'mul_med.txt',
                _('Hard'): 'mul_hard.txt',
                _('Challenging'): 'mul_chlg.txt',
            },
            _('Division (/)'): {
                _('Simple'): 'div_simple.txt',
                _('Easy'): 'div_easy.txt',
                _('Medium'): 'div_med.txt',
                _('Hard'): 'div_hard.txt',
                _('Challenging'): 'div_chlg.txt',
            },
            _('Percentage (%)'): {
                _('Simple'): 'per_simple.txt',
                _('Easy'): 'per_easy.txt',
                _('Medium'): 'per_med.txt',
            },
        }

        header_bar = QLabel("Maths-Tutor")
        header_bar.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(header_bar)

        hbox2 = QBoxLayout(QBoxLayout.LeftToRight)
        hbox2.setSpacing(5)
        hbox2.setContentsMargins(20, 20, 20, 20)

        self.show_controls_button = QPushButton("Show Settings")
        self.show_controls_button.setFixedSize(100, 30)
        hbox2.addWidget(self.show_controls_button)

        about_button = QPushButton("About")
        about_button.setFixedSize(100, 30)
        hbox2.addWidget(about_button)

        user_guide_button = QPushButton("Help")
        user_guide_button.setFixedSize(100, 30)
        hbox2.addWidget(user_guide_button)

        quit_button = QPushButton("Quit")
        quit_button.setFixedSize(100, 30)
        hbox2.addWidget(quit_button)

        vbox_controls = QVBoxLayout()
        vbox_controls.setSpacing(10)
        vbox_controls.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        layout.addLayout(hbox2)
        layout.addLayout(vbox_controls)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        operator_box = QHBoxLayout()
        select_operator_label = QLabel("Select Operation:")
        select_operator_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        operator_box.addWidget(select_operator_label)
                
        self.operator_combobox = QComboBox()
        for operator in self.operator_mapping.keys():
            self.operator_combobox.addItem(operator)

        self.operator_combobox.currentIndexChanged.connect(self.on_operator_combobox_changed)
        operator_box.addWidget(self.operator_combobox)
        select_operator_label.setBuddy(self.operator_combobox)

        self.selected_operator = "" 

        level_box = QHBoxLayout()
        select_mode_label = QLabel("Select Difficulty Level:")
        select_mode_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        level_box.addWidget(select_mode_label)

        self.mode_combobox = QComboBox()
        level_box.addWidget(self.mode_combobox)

        select_mode_label.setBuddy(self.mode_combobox)

        self.operator_combobox.setCurrentIndex(self.pref.operator)
        self.mode_combobox.setCurrentIndex(self.pref.level)

        self.selected_level = ""

        vbox_controls.addWidget(operator_box)
        vbox_controls.addWidget(level_box)

        start_button = QPushButton("Start")
        start_button.clicked.connect(self.on_start_button_clicked)
        start_button.setProperty("class", "button")

        load_button = QPushButton("Load Questions")
        load_button.clicked.connect(self.on_load_button_clicked)
        load_button.setProperty("class", "button")

        vbox_controls.addWidget(start_button)
        vbox_controls.addWidget(load_button)
        
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')

        label_speech_synthesizer = QLabel("Speech Synthesizer")

        self.combobox_speech_synthesizer = QComboBox()
        for voice in voices:
            self.combobox_speech_synthesizer.addItem(voice.name)

        self.combobox_speech_synthesizer.currentIndexChanged.connect(self.on_speech_synthesizer_changed)

        label_speech_synthesizer.setBuddy(self.combobox_speech_synthesizer)

        hbox_speech_synthesizer = QHBoxLayout()
        hbox_speech_synthesizer.addWidget(label_speech_synthesizer)
        hbox_speech_synthesizer.addWidget(self.combobox_speech_synthesizer)

        vbox_controls.addLayout(hbox_speech_synthesizer)

        self.show()

    def initialize_pygame(self):
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(global_var.data_dir, 'sounds', 'backgroundmusic.ogg'))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def on_operator_combobox_changed(self, index):
        self.mode_combobox.clear()

        active = index
        for difficulty in self.operator_mapping[list(self.operator_mapping.keys())[active]].keys():
            self.mode_combobox.addItem(difficulty)

        self.mode_combobox.setCurrentIndex(0)

    def on_start_button_clicked(self):
        selected_operator = self.operator_combobox.currentText()
        self.pref.operator = self.operator_combobox.currentIndex()

        selected_mode = self.mode_combobox.currentText()
        self.pref.level = self.mode_combobox.currentIndex()

        file_path = self.operator_mapping.get(selected_operator, {}).get(selected_mode)
        self.start_game(global_var.data_dir + "/lessons/" + file_path)

    def start_game(self, file_path):
        self.game_bin.load_question_file(file_path)
        self.vbox_controls.hide()
        self.game_bin.show()
        self.show_controls_button.setText(_("Show Settings"))
        self.update()

    def on_load_button_clicked(self):
        dialog = QFileDialog(self)
        dialog.setWindowTitle(_("Please choose a lesson file"))
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter(_("Text files (*.txt)"))
        if dialog.exec():
            selected_files = dialog.selectedFiles()
            if selected_files:
                selected_file = selected_files[0]
                self.start_game(selected_file)

    def show_controls(self):
        if self.vbox_controls.isVisible():
            self.vbox_controls.hide()
            self.game_bin.show()
            self.game_bin.setFocus()
            self.show_controls_button.setText(_("Show Settings"))
        else:
            self.show_controls_button.setText(_("Hide Settings"))
            self.vbox_controls.show()
            self.game_bin.hide()
            self.operator_combobox.setFocus()
        self.update()

    def show_about_dialog(self):
        about_dialog = QMessageBox(QMessageBox.Information, _("About"), "")
        about_dialog.setWindowIcon(QIcon(QtGui.QPixmap(global_var.data_dir+"/icon.png")))
        about_dialog.setIconPixmap(QtGui.QPixmap(global_var.data_dir+"/icon.png"))
        about_dialog.setText(_("Your About Message Here"))
        about_dialog.exec()

    def on_speech_language_changed(self, index):
        # Handle the change in speech language
        pass

    def on_speech_person_changed(self, index):
        # Handle the change in speech person
        pass

    def on_play_speech_button_clicked(self):
        # Retrieve the selected text from the ComboBox
        selected_text = self.combobox_speech_synthesizer.currentText()
        # Use pyttsx3 to speak the selected text
        self.engine.say(selected_text)
        self.engine.runAndWait()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SelectGame()
    win.show()
    sys.exit(app.exec())
