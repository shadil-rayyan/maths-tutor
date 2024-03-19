import os
import threading
import math
import random
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QWidget, QSizePolicy, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QMainWindow, QPushButton
from PySide6.QtGui import QPixmap, QFont, QKeyEvent
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtCore import QUrl
import time
import global_var
from gettext import gettext as _


listing_symbol = ","
range_symbol = ":"
multiplier_symbol = ";"

class MathsTutorBin(QWidget):
    def __init__(self, speech_object, gettext):
        super().__init__()
        self.speech = speech_object
        self._ = gettext

        # Create layout
        vbox = QVBoxLayout(self)
        vbox.setSpacing(6)

        vbox2 = QVBoxLayout()

        # Create label
        self.label = QLabel()
        font = QFont("Sans", 40)
        self.label.setFont(font)
        vbox2.addWidget(self.label)

        hbox = QHBoxLayout()

        fix1 = QWidget()
        fix1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        hbox.addWidget(fix1)

        self.entry = QLineEdit()
        self.entry.returnPressed.connect(self.on_entry_activated)
        self.entry.keyPressEvent = self.on_key_press
        hbox.addWidget(self.entry)

        fix2 = QWidget()
        fix2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        hbox.addWidget(fix2)

        vbox2.addLayout(hbox)

        self.image = QGraphicsView()
        self.scene = QGraphicsScene()
        self.image.setScene(self.scene)
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setFixedSize(200, 200)
        vbox2.addWidget(self.image)

        vbox.addLayout(vbox2)

        self.current_question_index = -1
        self.wrong = False
        self.current_performance_rate = 0
        self.final_score = 0
        self.incorrect_answer_count = 0
        self.number_of_questions_attended = 0

        self.player = QMediaPlayer()

    def grab_focus_on_entry(self):
        self.entry.setFocus()

    def connect_game_over_callback_function(self, function):
        self.game_over_callback_function = function

    def play_file(self, name, rand_range=1):
        if rand_range == 1:
            file_path_and_name = f'file:///{global_var.data_dir}/sounds/{name}.ogg'
        else:
            value = str(random.randint(1, rand_range))
            file_path_and_name = f'file:///{global_var.data_dir}/sounds/{name}-{value}.ogg'
        url = QUrl.fromLocalFile(file_path_and_name)  # Use QUrl here
        self.player.setMedia(url)
        self.player.play()

    def on_entry_activated(self):
        pass

    def next_question(self):
        pass

    def get_randome_number(self, value1, value2):
        pass

    def make_question(self, question):
        pass

    def announce_question_using_thread(self, verbose=False):
        pass

    def announce_question(self, question, make_sound, announcing_question_index, verbose):
        pass

    def on_quit(self):
        pass

    def keyPressEvent(self, event: QKeyEvent):
        keyval = event.key()
        if keyval == Qt.Key_Space:
            self.announce_question_using_thread()
        elif keyval in (Qt.Key_Shift, Qt.Key_Shift + Qt.Key_Shift):
            self.announce_question_using_thread(True)
        elif keyval == Qt.Key_Semicolon:
            self.speech.set_speech_rate(int(self.speech.get_speech_rate()) - 10)
            self.announce_question_using_thread()
        elif keyval == Qt.Key_Apostrophe:
            self.speech.set_speech_rate(int(self.speech.get_speech_rate()) + 10)
            self.announce_question_using_thread()

    def on_key_press(self, event):
        pass

    def set_image(self, name, rand_range):
        value = str(random.randint(1, rand_range))
        pixmap = QPixmap(global_var.data_dir + "/images/" + name + "-" + value + ".gif")
        item = QGraphicsPixmapItem(pixmap)
        self.scene.clear()
        self.scene.addItem(item)

    def speak(self, text, enqueue=False):
        if not enqueue:
            self.speech.cancel()
        self.speech.speak(text)

    def load_question_file(self, file_path):
        self.list = []
        self.current_question_index = -1
        self.wrong = False
        self.number_of_questions_attended = 0

        with open(file_path, "r") as file:
            for line in file:
                stripped_line = line.strip()
                self.list.append(stripped_line)

        self.label.setText(self.welcome_message)
        self.set_image("welcome", 3)
        self.play_file('welcome')
        self.speak(self.welcome_message)
        self.entry.setFocus()
        self.game_over = False

    def convert_signs(self, text):
        return text.replace("+", " " + _("plus") + " ") \
                   .replace("-", " " + _("minus") + " ") \
                   .replace("*", " " + _("multiply") + " ") \
                   .replace("/", " " + _("divided by") + " ") \
                   .replace("%", " " + _("percentage of") + " ")

    def convert_to_verbose(self, text):
        return ", ".join(text)

    def on_entry_activated(self):
        if self.game_over:
            self.game_over_callback_function()
        elif self.current_question_index == -1:
            self.starting_time = time.time()
            self.wrong = False
            self.current_performance_rate = 0
            self.final_score = 0
            self.incorrect_answer_count = 0
            self.next_question()
        else:
            answer = self.entry.text()
            correct_answer = self.answer

            if answer == correct_answer:
                time_end = time.time()
                time_taken = time_end - self.time_start
                time_alotted = int(self.list[self.current_question_index].split("===")[1])

                print(
                    f"\n### Time Allotted ###\n"
                    f"Excellent: {time_alotted - (time_alotted * 50) / 100}\n"
                    f"Very Good: {time_alotted - (time_alotted * 25) / 100}\n"
                    f"Good: {time_alotted}\n"
                    f"Fair: {time_alotted + (time_alotted * 25) / 100}\n"
                    f"### Time Taken: {time_taken}\n\n"
                )

                self.incorrect_answer_count = 0
                appreciation_index = random.randint(0, 4)

                if time_taken < time_alotted - ((time_alotted * 50) / 100):
                    self.current_performance_rate += 4
                    self.final_score += 50
                    text = self.appreciation_dict["Excellent"][appreciation_index]
                    self.set_image("excellent", 3)
                    self.play_file("excellent", 3)
                elif time_taken < time_alotted - ((time_alotted * 25) / 100):
                    self.current_performance_rate += 2
                    self.final_score += 40
                    text = self.appreciation_dict["Very good"][appreciation_index]
                    self.set_image("very-good", 3)
                    self.play_file("very-good", 3)
                elif time_taken < time_alotted:
                    self.current_performance_rate += 1
                    self.final_score += 30
                    text = self.appreciation_dict["Good"][appreciation_index]
                    self.set_image("good", 3)
                    self.play_file("good", 3)
                elif time_taken < time_alotted + ((time_alotted * 25) / 100):
                    self.final_score += 20
                    text = self.appreciation_dict["Fair"][appreciation_index]
                    self.set_image("not-bad", 3)
                    self.play_file('not-bad', 3)
                else:
                    self.current_performance_rate -= 1
                    self.final_score += 10
                    text = self.appreciation_dict["Okay"][appreciation_index]
                    self.set_image("okay", 3)
                    self.play_file('okay', 3)
                text = text + "!"
                self.speak(text)
                self.label.setText(text)
            else:
                self.wrong = True
                self.current_performance_rate -= 3
                self.final_score -= 10
                self.incorrect_answer_count = self.incorrect_answer_count + 1
                if self.incorrect_answer_count == 3:
                    self.set_image("wrong-anwser-repeted", 2)
                    self.play_file("wrong-anwser-repeted", 3)
                    self.incorrect_answer_count = 0
                    text = _("Sorry! The correct answer is ")
                    self.label.setText(text + self.answer)
                    if len(self.answer.split(".")) > 1:
                        li = list(self.answer.split(".")[1])
                        self.speak(text + self.answer.split(".")[0] + " " + _("point") + " " + " ".join(li))
                    else:
                        self.speak(text + self.answer)
                else:
                    text = _("Sorry! Let's try again")
                    self.label.setText(text)
                    self.speak(text)
                    self.set_image("wrong-anwser", 3)
                    self.play_file("wrong-anwser", 3)
            QTimer.singleShot(3000, self.next_question)
            self.entry.setText("")

    def next_question(self):
        self.time_start = time.time()
        self.entry.setFocus()

        if self.wrong:
            self.label.setText(self.question)
            self.announce_question_using_thread()
            self.set_image("wrong-anwser", 3)
            self.wrong = False
        else:
            print("Current Performance Rate = " + str(self.current_performance_rate) +
                  " Question index shift = " + str(math.floor(self.current_performance_rate / 10) + 1))
            next_question = self.current_question_index + math.floor(self.current_performance_rate / 10) + 1
            if next_question >= 0:
                self.current_question_index = next_question

            if self.current_question_index < len(self.list) - 1:
                question_to_pass = self.list[self.current_question_index].split("===")[0]
                self.question = self.make_question(question_to_pass)
                question_to_evaluate = self.question
                if "%" in self.question:
                    digit_one, digit_two = self.question.split("%")
                    question_to_evaluate = "(" + digit_one + "*" + digit_two + ")/100"

                number = eval(question_to_evaluate)
                if number == math.trunc(number):
                    self.answer = str(math.trunc(number))
                else:
                    num = round(eval(str(number)), 2)
                    self.answer = str(num)

                self.make_sound = self.list[self.current_question_index].split("===")[2]
                self.label.setText(self.question)
                self.announce_question_using_thread()

                self.entry.setText("")
                self.set_image("question", 2)

                self.number_of_questions_attended += 1
            else:
                minute, seconds = divmod(round(time.time() - self.starting_time), 60)
                score = round((self.final_score * 100) / (50 * self.number_of_questions_attended))
                text = _("Successfully finished! Your mark is ") + str(score) + \
                       "!\n" + _("Time taken ") + str(minute) + " " + _("minutes and") + " " + str(
                    seconds) + " " + _("seconds!")
                self.speak(text)
                self.label.setText(text)
                self.set_image("finished", 3)
                self.play_file("finished", 3)
                self.game_over = True

class MathsTutorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel()
        self.layout.addWidget(self.label)

        self.entry = QPushButton("Enter")
        self.entry.clicked.connect(self.on_entry_clicked)
        self.layout.addWidget(self.entry)

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Maths Tutor')
        self.show()

    def on_entry_clicked(self):
        # Handle entry button click event here
        pass

    # Add other methods here...

if __name__ == "__main__":
    app = QApplication([])
    win = MathsTutorWindow()
    app.exec()