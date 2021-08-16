from threading import Thread

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.daemon = True
        self.start()

    """Thread work loop calling the function with the params"""

    def run(self):
        # keep running until told to abort
        while True:
            try:
                # get a task and raise immediately if none available
                func, arg1, arg2 = self.queue.get()
            except:
                continue

            try:
                # the function may raise
                func(arg1, arg2)
            except Exception as e:
                # so we move on and handle it in whatever way the caller wanted
                print(e)
