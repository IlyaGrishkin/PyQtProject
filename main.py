import sys
from threading import Timer

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow


class Notification(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("templates/notification.ui", self)


class TestScreen(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("templates/test_screen.ui", self)


class Test:
    def __init__(self, questions_quantity, time):
        self.qq = questions_quantity
        self.answers = dict()
        self.time = int(time.split(':')[0]) * 60 + int(time.split(':')[1])

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
        self.timerInitUI()
        self.test_screen = TestScreen()

    def timerInitUI(self):
        pass

    def tasksInitUI(self):
        self.tasks.setMinimum(3)
        self.tasks.setMaximum(30)
        self.tasks.setValue(10)

    def handleTestStart(self):
        questions_quantity = self.tasks.value()
        time = str(self.timer.time().toPyTime())
        test = Test(questions_quantity, time)
        test.start()
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
