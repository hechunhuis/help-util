from threading import Thread

class MyThread(Thread):
    '''
    自定义多线程支持返回值
    '''
    def __init__(self, func, args) -> None:
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
    def run(self):
        self.result = self.func(*self.args)
    def getResult(self):
        try:
            return self.result
        except Exception:
            return None