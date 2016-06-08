import gevent
import gevent.pool
from gevent.event import AsyncResult


class Event(object):
    def __init__(self):
        self.reset()

    def send(self, value=None, exception=None):
        if exception is None:
            return self._asyncresult.set(value)
        elif isinstance(exception, tuple):
            exc_info = exception
            exc = exc_info[1]
            return self._asyncresult.set_exception(exc, exc_info)
        else:
            return self.send_exception(exception)

    def send_exception(self, exc):
        return self._asyncresult.set_exception(exc)

    def wait(self):
        return self._asyncresult.get()

    def ready(self):
        return self._asyncresult.ready()

    def reset(self):
        self._asyncresult = AsyncResult()


# monkey-patches. TODO: better solution

gevent.Greenlet.wait = gevent.Greenlet.get
gevent.pool.Pool.waitall = gevent.pool.Pool.join

sleep = gevent.sleep
