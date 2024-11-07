from threading import Timer


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


t = Test(3, '00:05:00')
t.start()
t.update('1', 3)
t.update('2', 1)
