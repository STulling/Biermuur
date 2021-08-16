from threading import Thread
import display


class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.daemon = True

    """Thread work loop calling the function with the params"""

    def run(self):
        # keep running until told to abort
        while True:
            func, arg1, arg2 = self.queue.get()
            display.primary.value = display.wheel(int(arg2 * 255))
            func(arg1, arg2)
