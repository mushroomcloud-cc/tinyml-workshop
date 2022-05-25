import time

class PerformanceCounter:
    def __init__(self):
        self.Reset()


    def Reset(self):
        self.Count = 0
        self.LastTick = time.perf_counter()


    def Frame(self):
        self.Count = self.Count + 1

        tick = time.perf_counter()
        dt = tick - self.LastTick
        self.LastTick = tick

        return [self.Count, dt]