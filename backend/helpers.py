from datetime import datetime


class InMemoryCallCache:
    def __init__(self, max=100):
        self._max = max
        self._index = 0
        self._queue = list()

    @property
    def queue(self):
        """the queue"""
        return self._queue

    @property
    def size(self):
        """the queue"""
        return self._max

    @property
    def index(self):
        """the queue"""
        return self._index - 1

    def put(self, element):
        self._queue.append(element)
        self._index += 1

    def pop(self, index):
        element = self._queue.pop(index)
        self._index -= 1
        return element

    def inspect(self, index):
        element = self._queue[index]
        return element

    def full(self):
        return self._index == self._max


class IPCache(InMemoryCallCache):
    def __init__(self, max_size=50, timeout=5):
        self._timeout = timeout
        super().__init__(max_size)

    @property
    def timeout(self):
        return self._timeout

    def _valid_call(self, ip):
        now = datetime.utcnow()
        if self.full():
            # if the older element in a full queue is older then timeout
            # we can proceed with the new request and delete the older element
            first_element = self.inspect(0)
            t_delta = now - first_element['date']
            print(f"{ip}: seconds = {t_delta.seconds}")
            if t_delta.seconds < self.timeout:
                return False
            else:
                self.pop(0)
        for i in self.queue:

            t_delta = now - i['date']
            if i['ip'] == ip and t_delta.seconds < self.timeout:
                return False
        return True

    def put(self, ip):
        if self._valid_call(ip):
            element = {'date': datetime.utcnow(), 'ip': ip}
            super().put(element)
            return True
        else:
            return False
