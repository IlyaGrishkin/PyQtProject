import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow


class Notification(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("notification.ui", self)


class StartTestBase(QWidget):
    def __init__(self, topic):
        super().__init__()
        uic.loadUi("startTestBase.ui", self)
        self.topic = topic
        self.topicLabel.setText(self.topic)
        self.startButton.clicked.connect(self.handleTestStart)
        self.tasksInitUI()
        self.timerInitUI()

    def timerInitUI(self):
        pass

    def tasksInitUI(self):
        self.tasks.setMinimum(3)
        self.tasks.setMaximum(30)
        self.tasks.setValue(10)

    def handleTestStart(self):
        print(self.tasks.value())
        print(str(self.timer.time().toPyTime()))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("testMainScreen.ui", self)
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
