import sys
import webbrowser
import pygame
import gettext
import os
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QCheckBox, QMainWindow,QWidget,QBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import pyttsx3

# Adjust the path according to your project structure
#from qt import preferences
import global_var

import os

import preferences
from PyQt6 import QtCore
from PyQt6 import QtWidgets
from PyQt6 import QtGui
#from PyQt5.QtWidgets import QBoxLayout

# Default directory for preferences file
DEFAULT_PREFS_DIR = 'D:\shadil\zendalona\qt\MathsTutor\preferences.py'

# Try to get the 'HOME' environment variable, use the default directory if not available
home_dir = os.environ.get('HOME', DEFAULT_PREFS_DIR)

# Determine the user's preferences directory based on the platform
if sys.platform.startswith('win'):
    # On Windows, use the AppData directory
    app_data_dir = os.getenv('APPDATA')
    if app_data_dir is None:
        app_data_dir = os.path.expanduser("~")
    prefs_dir = os.path.join(app_data_dir, 'maths-tutor')
else:
    # On Unix-like systems, use the home directory
    prefs_dir = os.path.expanduser("~/.maths-tutor")

# Ensure the preferences directory exists
os.makedirs(prefs_dir, exist_ok=True)

# Construct the path to the preferences file
user_preferences_file_path = os.path.join(prefs_dir, 'prefs.cfg')

gettext.bindtextdomain(global_var.app_name, global_var.locale_dir)
gettext.textdomain(global_var.app_name)
_ = gettext.gettext


class LanguageSelectionDialog(QDialog):
    def __init__(self, parent=None, language=0):
        super().__init__(parent)
        self.setWindowTitle("Maths-Tutor")
        language_dict = {"en": "English", "fr": "French", "es": "Spanish"}  # Define the language_dict variable

        self.setWindowIcon(QIcon("path/to/icon.png"))
        self.resize(200, 150)

        # Create a ComboBox with language options
        label_language = QLabel("Select Language")
        self.combobox = QComboBox()
        for item in language_dict.values():
            self.combobox.addItem(item)
        self.combobox.setCurrentIndex(language)  # Set the default selection
        hbox1 = QHBoxLayout()
        hbox1.addWidget(label_language)
        hbox1.addWidget(self.combobox)

        # Create a CheckButton with remember option
        self.remember_checkbox = QCheckBox("Remember Selection")

        # Create a layout to organize widgets
        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addWidget(self.remember_checkbox)

        self.setLayout(layout)


class SelectGame(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Load and play the background music
        pygame.mixer.music.load(os.path.join(global_var.data_dir, 'sounds', 'backgroundmusic.ogg'))
        # Set the volume
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)  # -1 will loop the music indefinitely

        # User Preferences
        self.pref = preferences.Preferences()
        self.pref.load_preferences_from_file(global_var.user_preferences_file_path)
        
        # Store the previous language for checking if a speech synthesizer
        # or language change is needed.
        previous_language = self.pref.language
        
        if self.pref.language == -1:
            self.pref.language = 0

        if self.pref.remember_language == 1:
            language_dict = {"en": "English", "fr": "French", "es": "Spanish"}  # Define the language_dict variable
            selected_language = list(language_dict)[self.pref.language]
        else:
            # Create and show the language selection dialog
            lang_dialog = LanguageSelectionDialog(self, self.pref.language)
            response = lang_dialog.exec()

            if response == 1:  # Accepted
                # Retrieve the selected language from the ComboBox
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

        # Checking if a speech synthesizer or speech language change is needed.
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
         # Create a HeaderBar
        header_bar = QLabel("Maths-Tutor")
        header_bar.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(header_bar)

        # Horizontal box for Show/Hide Settings, About, User-Guide, and Quit
        hbox2 = QBoxLayout(QBoxLayout.LeftToRight)
        hbox2.setSpacing(5)
        hbox2.setContentsMargins(20, 20, 20, 20)

        # Create settings button
        self.show_controls_button = QPushButton("Show Settings")
        self.show_controls_button.setFixedSize(100, 30)

        hbox2.addWidget(self.show_controls_button)

        # Create about button
        about_button = QPushButton("About")
        about_button.setFixedSize(100, 30)
        hbox2.addWidget(about_button)

        # Create user guide button
        user_guide_button = QPushButton("Help")
        user_guide_button.setFixedSize(100, 30)
        hbox2.addWidget(user_guide_button)

        # Creating quit button
        quit_button = QPushButton("Quit")
        quit_button.setFixedSize(100, 30)
        hbox2.addWidget(quit_button)

        # Create a VBox to organize components vertically
        self.vbox_controls = QVBoxLayout()
        self.vbox_controls.setSpacing(10)
        self.vbox_controls.setContentsMargins(20, 20, 20, 20)

         # Set layout for the main window
        layout = QVBoxLayout()
        layout.addLayout(hbox2)
        #layout.addLayout(operator_box)
        layout.addLayout(self.vbox_controls)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        operator_box = QHBoxLayout()
        select_operator_label = QLabel("Select Operation:")
        select_operator_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        operator_box.addWidget(select_operator_label)
                
        self.operator_combobox = QComboBox()
        for operator in self.operator_mapping.keys():
         self.operator_combobox.addItem(operator)

        self.operator_combobox.currentIndexChanged.connect(self.on_oprator_combobox_changed)
        operator_box.addWidget(self.operator_combobox)
        select_operator_label.setBuddy(self.operator_combobox)

            # Create a variable to store the selected operator
        self.selected_operator = "" 
            # Create a HBox for the level labels and ComboBox
        level_box = QHBoxLayout()
        select_mode_label = QLabel("Select Difficulty Level:")
        select_mode_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        level_box.addWidget(select_mode_label)

        self.mode_combobox = QComboBox()
        level_box.addWidget(self.mode_combobox)

        select_mode_label.setBuddy(self.mode_combobox)

        self.operator_combobox.setCurrentIndex(self.pref.operator)
        self.mode_combobox.setCurrentIndex(self.pref.level)

        # Create a variable to store the selected level
        self.selected_level = ""

        # Add operator_box and level_box to vbox_controls
        self.vbox_controls.addWidget(operator_box)
        self.vbox_controls.addWidget(level_box)

        # Create the Start button
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.on_start_button_clicked)
        start_button.setProperty("class", "button")  # Set a CSS class for styling

        # Create the Load Questions button
        load_button = QPushButton("Load Questions")
        load_button.clicked.connect(self.on_load_button_clicked)
        load_button.setProperty("class", "button")  # Set a CSS class for styling
        
        # Add Start and Load Questions buttons to vbox_controls
        self.vbox_controls.addWidget(start_button)
        self.vbox_controls.addWidget(load_button)
        
        # Assuming speech is a module or class containing Speech functionality
        
        # Create an instance of the pyttsx3 engine
        self.engine = pyttsx3.init()

        # Retrieve the list of available voices
        voices = self.engine.getProperty('voices')

        # Create a label for the speech synthesizer selection
        label_speech_synthesizer = QLabel("Speech Synthesizer")

        # Create a ComboBox for selecting the speech synthesizer
        self.combobox_speech_synthesizer = QComboBox()
        for voice in voices:
            self.combobox_speech_synthesizer.addItem(voice.name)

        # Connect the ComboBox's 'currentIndexChanged' signal to the appropriate method
        self.combobox_speech_synthesizer.currentIndexChanged.connect(self.on_speech_synthesizer_changed)

        # Set mnemonic widget for label_speech_synthesizer
        label_speech_synthesizer.setBuddy(self.combobox_speech_synthesizer)

        # Create a QHBoxLayout to organize the label and ComboBox horizontally
        hbox_speech_synthesizer = QHBoxLayout()
        hbox_speech_synthesizer.addWidget(label_speech_synthesizer)
        hbox_speech_synthesizer.addWidget(self.combobox_speech_synthesizer)

        # Add the QHBoxLayout containing the label and ComboBox to vbox_controls
        self.vbox_controls.addLayout(hbox_speech_synthesizer)

        # Create a label for selecting the speech language (not applicable for pyttsx3)

        # Create a label for selecting the speech person (not applicable for pyttsx3)

    def on_operator_combobox_changed(self, index):
                # Implement your logic here
                pass
    
    def on_start_button_clicked(self):
                # Implement your logic here
                pass

    def on_load_button_clicked(self):
                # Implement your logic here
                pass

    def on_speech_synthesizer_changed(self, index):
                # Implement your logic here
                pass
    def on_speech_language_changed(self):
        # Disconnecting to prevent function calls while clearing
        # combobox_speech_language or adding each language to the same
        try:
            self.combobox_speech_person.currentIndexChanged.disconnect(self.on_speech_person_changed)
        except TypeError:
            pass

        self.combobox_speech_person.clear()

        if len(self.speech_language_person_dict.keys()) == 0:
            self.combobox_speech_person.addItem(_("Default"))
            self.pref.speech_person = 0
            return

        index_language = self.combobox_speech_language.currentIndex()
        language = list(self.speech_language_person_dict.keys())[index_language]
        self.pref.speech_language = index_language

        for item in self.speech_language_person_dict[language]:
            self.combobox_speech_person.addItem(item)

        if self.pref.speech_person >= len(self.speech_language_person_dict[language]):
            self.pref.speech_person = 0

        self.combobox_speech_person.currentIndexChanged.connect(self.on_speech_person_changed)

        self.speech.set_language(language)
        self.combobox_speech_person.setCurrentIndex(self.pref.speech_person)

    def on_speech_person_changed(self):
        index_language = self.combobox_speech_language.currentIndex()
        language = list(self.speech_language_person_dict.keys())[index_language]

        index_person = self.combobox_speech_person.currentIndex()
        if index_person == -1:
            index_person = 0
        voice = self.speech_language_person_dict[language][index_person]

        self.pref.speech_person = index_person

        self.speech.set_synthesis_voice(voice)

    def on_start_button_clicked(self, button):
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

    def on_oprator_combobox_changed(self, index):
        self.mode_combobox.clear()

        active = index
        for difficulty in self.operator_mapping[list(self.operator_mapping.keys())[active]].keys():
            self.mode_combobox.addItem(difficulty)

        self.mode_combobox.setCurrentIndex(0)

    def on_load_button_clicked(self):
        # Create a file dialog to choose a file
        dialog = QtWidgets.QFileDialog(self)
        dialog.setWindowTitle(_("Please choose a lesson file"))
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
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
        about_dialog = QtWidgets.QMessageBox.about(
            self,
            _("About"),
            _("Your About Message Here")
        )

    def show_about_dialog(self):
        about_dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, _("About"), "")
        about_dialog.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(global_var.data_dir+"/icon.png")))
        about_dialog.setIconPixmap(QtGui.QPixmap(global_var.data_dir+"/icon.png"))
        about_dialog.setText("Maths-Tutor")
        about_dialog.setInformativeText(
            "Maths-Tutor is a game designed to enhance one's calculation abilities in mathematics and enable them to self-assess."
        )
        about_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
        about_dialog.setDetailedText(
            "License: GNU General Public License - GPL-2.0\n"
            "Website: http://wwww,zendalona.com/maths-tutor\n"
            "Copyright (C) 2022-2023 Roopasree A P <roopasreeap@gmail.com>\n"
            "Copyright (C) 2022-2023 Greeshna Sarath <greeshnamohan001@gmail.com>\n"
            "Supervised by Zendalona(2022-2024)\n"
            "Authors: Roopasree A P, Greeshna Sarath\n"
            "Documenters: Roopasree A P, Greeshna Sarath\n"
            "Artists: Nalin Sathyan, Dr. Saritha Namboodiri, K. Sathyaseelan, Mukundhan Annamalai, Ajayakumar A, Subha I N, Bhavya P V, Abhirami T, Ajay Kumar M, Saheed Aslam M, Dr. Rajakrishnan V. K., Girish KK, Suresh S"
        )
        about_dialog.exec()

    def on_help_clicked(self):
        url = global_var.user_guide_file_path
        try:
            webbrowser.get("firefox").open(url, new=2)
        except webbrowser.Error:
            webbrowser.open(url, new=2)

    def on_quit_clicked(self):
        self.pref.speech_rate = self.speech.get_speech_rate()
        self.pref.save_preferences_to_file(global_var.user_preferences_file_path)
        self.speech.close()
        self.game_bin.on_quit()
        QtWidgets.QApplication.quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = SelectGame()
    win.show()
    app.exec()


