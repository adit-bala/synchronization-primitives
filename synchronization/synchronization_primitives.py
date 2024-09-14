import threading
from collections import deque

# TODO: implement priority scheduler

class Semaphore:
    def __init__(self, value):
        self.value = value
        # don't need a thread-safe queue since we will always have a lock when modifying _waiters
        self.waiters = deque()
        # need to maintain a lock for the critical section since we are not disabling interrupts
        self._lock = threading.Lock()
        # cannot disable interrupts in user space so need a way to atomically sleep and release _lock
        self._condition = threading.Condition(self._lock)

    def sema_down(self):
        # entire section is a critical section
        with self._condition:
            # Need a while loop due to spurious wake ups
            while self.value == 0:
                current_thread = threading.current_thread()
                self.waiters.append(current_thread)
                # Before we block we need to release lock to critical section
                self._condition.wait()
                # Once we wake up
                self.waiters.popleft()
            self.value -= 1
    
    def sema_up(self):
        # lock since _value is a shared variable
        with self._condition:
            self.value += 1
            # notify one waiter
            self._condition.notify()

class Lock:
    def __init__(self):
        self.holder = None
        self.semaphore = threading.Semaphore(1)

    def acquire(self):
        self.semaphore.sema_down()
        self.holder = threading.current_thread()

    def release(self):
        self.holder = None
        self.semaphore.sema_up()

class Barrier:
    def __init__(self, size):
        self.semaphore = Semaphore(0)
        self.mutex = Lock()
        self.size = size
        self.count = 0

    def wait(self):
        with self.mutex:
            self.count += 1
        if self.count == self.size:
            self.semaphore.release()
        self.semaphore.acquire()
        self.semaphore.release()
        
            


class RW:
    def __init__(self):
        self._lock = threading.Lock()
        self._read_condition = threading.Condition(self._lock)
        self._write_condition = threading.Condition(self._lock)
        self.AR = self.WR = self.AW = self.WW = 0

    def rw_lock_acquire(self, is_reader):
        # activate guard lock
        with self._lock:
            if (is_reader):
                # block while there are active or waiting writers
                while (self.AW + self.WW > 0):
                    self.WR += 1
                    self._read_condition.wait()
                    self.WR -= 1
                # we are now an active reader
                self.AR += 1
            else:
                while (self.AR + self.AW > 0):
                    self.WW += 1
                    self._write_condition.wait()
                    self.WW -= 1
                # we are now an active writer
                self.AW += 1

    def rw_lock_release(self, is_reader):
        with self._lock:
            if is_reader:
                self.AR -= 1
                # if we are the last active reader, try to wake up writer
                if (self.AR == 0 and self.WW > 0):
                    self._write_condition.notify()
            else:
                self.AW -= 1
                # prioritize waking up writers
                if (self.WW > 0):
                    self._write_condition.notify()
                # if no writers we can awake all readers
                else:
                    self._read_condition.notify_all()







