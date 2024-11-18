import sys

from PyQt6 import uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QListWidget, QTableWidgetItem, QLabel

from database import add_new_attempt, create_database, get_attempts, add_new_stress, get_stress, RUSSIAN_TOPICS, \
    get_adverb


class Notification(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("templates/notification.ui", self)


class AccentAddForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("templates/stressAddWord.ui", self)
        self.addBtn.clicked.connect(self.handleSubmit)

    def handleSubmit(self):
        word = self.input.text()
        is_rigth = self.checkBox.isChecked()
        add_new_stress(word, is_rigth)


class AddWord(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("templates/addWordsNav.ui", self)
        self.initUI()

    def initUI(self):
        self.accentButton.clicked.connect(self.accentHandler)
        self.adverbButton.clicked.connect(self.adverbHandler)
        self.pronounButton.clicked.connect(self.pronounHandler)

    def accentHandler(self):
        self.addWordScreen = AccentAddForm()
        self.addWordScreen.show()

    def adverbHandler(self):
        self.addWordScreen = StartTestBase("Наречия")
        self.addWordScreen.show()

    def pronounHandler(self):
        self.addWordScreen = StartTestBase("Местоимения")
        self.addWordScreen.show()


class Statistics(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("templates/statistic.ui", self)
        data = get_attempts()
        data.reverse()
        for i in range(min(len(data), 10)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(data[i][0]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(data[i][1]))


class TestResult(QWidget):
    def __init__(self, questions_quantity, correct_answers, mistakes):
        super().__init__()
        uic.loadUi("templates/testResult.ui", self)
        self.result.setText(f"Ваш результат {correct_answers} из {questions_quantity}")

        if correct_answers == questions_quantity:
            self.mistakesLabel.setText("Отлично! У вас нет ни одной ошибки!")
        else:
            self.listWidget = QListWidget()
            self.listWidget.addItems(mistakes)
            self.verticalLayout.addWidget(self.listWidget)


class TrueFalseTestScreen(QWidget):
    def __init__(self, test):
        super().__init__()
        uic.loadUi("templates/TrueFalseTestScreen.ui", self)
        self.test = test
        if self.test.topic == 'adverb':
            self.true_btn.setText('Слитно')
            self.false_btn.setText('Раздельно')

        self.time = test.time
        self.show_time = str(self.test.qt_time.toPyTime())[:5]
        self.timeLabel.setText(f'До конца теста осталось:  {self.show_time}')

        self.timer = QTimer()
        self.timer.timeout.connect(self.timing)
        self.timer.start(1000)

        self.cur_index = 0
        self.data = test.data
        self.db_word = self.data[self.cur_index][0]
        self.is_rigth = self.data[self.cur_index][1]
        self.true_btn.clicked.connect(self.handleAnswer)
        self.false_btn.clicked.connect(self.handleAnswer)
        self.word.setText(self.db_word)
        self.nextButton.clicked.connect(self.nextBtn)
        self.nextButton.setEnabled(False)
        self.clicked = False

        self.testResult = None
        self.correct_count = 0
        self.mistakes = []

    def handleAnswer(self):
        sender = self.sender().text()
        if sender in ("Верно", 'Слитно') and self.is_rigth:
            self.word.setStyleSheet("* {color: green }")
            self.true_btn.setStyleSheet("* {color: green }")
            self.test.correct += 1
        elif sender in ("Неверно", 'Раздельно') and (not self.is_rigth):
            self.word.setStyleSheet("* {color: green }")
            self.false_btn.setStyleSheet("* {color: green }")
            self.test.correct += 1
        else:
            self.word.setStyleSheet("* {color: red }")
            self.mistakes.append(self.db_word)
            if sender in ("Верно", 'Слитно'):
                self.true_btn.setStyleSheet("* {color: red }")
            else:
                self.false_btn.setStyleSheet("* {color: red }")

        self.true_btn.setEnabled(False)
        self.false_btn.setEnabled(False)
        self.nextButton.setEnabled(True)

    def changeShowTime(self, time: int):
        return ("0" * (2 - len(str(time // 60))) + str(time // 60) + ':'
                + "0" * (2 - len(str(time % 60))) + str(time % 60))

    def timing(self):
        self.time -= 1
        self.show_time = self.changeShowTime(self.time)
        self.timeLabel.setText(f'До конца теста осталось:  {self.show_time}')
        if self.time <= 0:
            self.finish()

    def finish(self):
        self.timer.stop()

        self.testResult = TestResult(self.test.qq, self.test.correct, self.mistakes)
        add_new_attempt(f'{self.test.correct}/{self.test.qq}', self.test.topic, self.mistakes)

        self.testResult.show()
        self.hide()

    def nextBtn(self):
        if int(self.test.qq) - 1 == self.cur_index:
            self.finish()
        else:
            self.cur_index += 1
            self.db_word = self.data[self.cur_index][0]
            self.is_rigth = self.data[self.cur_index][1]
            self.word.setText(self.db_word)

            self.clicked = False

            self.true_btn.setEnabled(True)
            self.false_btn.setEnabled(True)
            self.nextButton.setEnabled(False)

            self.true_btn.setStyleSheet("* {}")
            self.false_btn.setStyleSheet("* {}")
            self.word.setStyleSheet("* {}")


class Test:
    def __init__(self, questions_quantity, time, qt_time, topic):
        self.qq = questions_quantity
        self.answers = dict()
        self.correct = 0

        self.time = int(time.split(':')[0]) * 60 + int(time.split(':')[1])
        self.qt_time = qt_time

        self.topic = topic
        self.data = None

        if topic == 'stress':
            self.data = get_stress(self.qq)
        elif topic == 'adverb':
            self.data = get_adverb(self.qq)

    def get_answers(self):
        return self.correct


class StartTestBase(QWidget):
    def __init__(self, topic):
        super().__init__()
        uic.loadUi("templates/startTestBase.ui", self)
        self.topic = topic
        self.topicLabel.setText(f'Вы собираетесь начать тест по теме {self.topic.lower()}')
        self.startButton.clicked.connect(self.handleTestStart)
        self.tasksInitUI()
        self.test_screen = None

    def tasksInitUI(self):
        self.tasks.setMinimum(3)
        self.tasks.setMaximum(30)
        self.tasks.setValue(10)

    def handleTestStart(self):
        questions_quantity = int(self.tasks.value())
        time = str(self.timer.time().toPyTime())
        test = Test(questions_quantity, time, self.timer.time(), RUSSIAN_TOPICS[self.topic.lower()])
        self.test_screen = TrueFalseTestScreen(test)
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
        self.attemptsBtn.clicked.connect(self.attemptsHandler)
        self.addWordsBtn.clicked.connect(self.addWordHandler)

    def accentHandler(self):
        self.startWidget = StartTestBase("Ударения")
        self.startWidget.show()

    def adverbHandler(self):
        self.startWidget = StartTestBase("Наречия")
        self.startWidget.show()

    def pronounHandler(self):
        self.startWidget = StartTestBase("Местоимения")
        self.startWidget.show()

    def attemptsHandler(self):
        self.statisticScreen = Statistics()
        self.statisticScreen.show()

    def addWordHandler(self):
        self.addWordNav = AddWord()
        self.addWordNav.show()


if __name__ == '__main__':
    create_database()
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
