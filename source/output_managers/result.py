from multiprocessing import Queue


class Result:
    def __init__(self):
        self.results = Queue()

