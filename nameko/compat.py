from gevent.event import AsyncResult


class Event(object):
    def __init__(self):
        self._asyncresult = AsyncResult()

    def send(self, value=None, exception=None):
        if exception is None:
            self._asyncresult.set(value)
        elif isinstance(exception, tuple):
            exc_info = exception
            exc = exc_info[1]
            self._asyncresult.set_exception(exc, exc_info)
        else:
            self.send_exception(exception)

    def send_exception(self, exc):
        self._asyncresult.set_exception(exc)

    def wait(self):
        self._asyncresult.get()

    def ready(self):
        self._asyncresult.ready()
