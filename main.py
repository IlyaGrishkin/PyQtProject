import sys
from threading import Timer
from random import sample

import psycopg2
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow


class Notification(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("templates/notification.ui", self)


class TestScreen(QWidget):
    def __init__(self, test):
        super().__init__()
        uic.loadUi("templates/TrueFalseTestScreen.ui", self)
        self.test = test
        self.cur_index = 0
        self.data = test.data
        self.db_word = self.data[self.cur_index][0]
        self.is_rigth = self.data[self.cur_index][1]
        self.true_btn.clicked.connect(self.handleAnswer)
        self.false_btn.clicked.connect(self.handleAnswer)
        self.word.setText(self.db_word)
        self.clicked = False

    def handleAnswer(self):
        sender = self.sender().text()
        # if not self.clicked:
        if sender == "Верно" and self.is_rigth:
            self.word.setStyleSheet("* {color: green }")
            self.true_btn.setStyleSheet("* {color: green }")
        elif sender == "Неверно" and (not self.is_rigth):
            self.word.setStyleSheet("* {color: green }")
            self.false_btn.setStyleSheet("* {color: green }")
        else:
            self.word.setStyleSheet("* {color: red }")
            if sender == "Верно":
                self.true_btn.setStyleSheet("* {color: red }")
            else:
                self.false_btn.setStyleSheet("* {color: red }")

        self.true_btn.setEnabled(False)
        self.false_btn.setEnabled(False)
        # self.clicked = True

    def nextBtn(self):
        self.cur_index += 1
        self.db_word = self.data[self.cur_index][0]
        self.is_rigth = self.data[self.cur_index][1]
        self.word.setText(self.db_word)


class Test:
    def __init__(self, questions_quantity, time, topic):
        self.qq = questions_quantity
        self.answers = dict()
        self.time = int(time.split(':')[0]) * 60 + int(time.split(':')[1])
        if topic == 'stress':
            self.stress()

    def stress(self):
        conn = psycopg2.connect(dbname='words', user='postgres', password='Uhbirf55', host='localhost')
        cursor = conn.cursor()

        nums = sample(range(1, 249), 10)
        cursor.execute(f"SELECT word, is_rigth FROM stress WHERE word_id IN {tuple(nums)}")
        data = cursor.fetchall()
        conn.commit()
        self.data = data

    def start(self):
        timer = Timer(self.time, self.finish)
        timer.start()

    def update(self, question_id: str, answer):
        self.answers[str(question_id)] = answer

    def get_answers(self):
        return self.answers

    def write(self):
        """writes current test state into database"""
        pass

    def finish(self):
        """finish test attempt"""
        print(self.get_answers())
        return self.get_answers()


class StartTestBase(QWidget):
    def __init__(self, topic):
        super().__init__()
        uic.loadUi("templates/startTestBase.ui", self)
        self.topic = topic
        self.topicLabel.setText(self.topic)
        self.startButton.clicked.connect(self.handleTestStart)
        self.tasksInitUI()
        self.test_screen = None

    def tasksInitUI(self):
        self.tasks.setMinimum(3)
        self.tasks.setMaximum(30)
        self.tasks.setValue(10)

    def handleTestStart(self):
        questions_quantity = self.tasks.value()
        time = str(self.timer.time().toPyTime())
        test = Test(questions_quantity, time, 'stress')
        test.start()
        self.test_screen = TestScreen(test)
        self.hide()
        self.test_screen.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("templates/testMainScreen.ui", self)
        self.initUI()
        self.n = Notification()

    def initUI(self):
        self.accentButton.clicked.connect(self.accentHandler)
        self.adverbButton.clicked.connect(self.adverbHandler)
        self.pronounButton.clicked.connect(self.pronounHandler)

    def accentHandler(self):
        self.startWidget = StartTestBase("Ударения")
        self.startWidget.show()

    def adverbHandler(self):
        self.startWidget = StartTestBase("Наречия")
        self.startWidget.show()

    def pronounHandler(self):
        self.startWidget = StartTestBase("Местоимения")
        self.startWidget.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
