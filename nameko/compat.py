import socket
import sys

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


# from eventlet.convenience

def listen(addr, family=socket.AF_INET, backlog=50):
    """Convenience function for opening server sockets.  This
    socket can be used in :func:`~eventlet.serve` or a custom ``accept()``
    loop.

    Sets SO_REUSEADDR on the socket to save on annoyance.

    :param addr: Address to listen on.  For TCP sockets, this is a (host, port)
    tuple.  :param family: Socket family, optional.  See :mod:`socket`
    documentation for available families.  :param backlog:

        The maximum number of queued connections. Should be at least 1; the
        maximum value is system-dependent.

    :return: The listening green socket object.
    """
    sock = socket.socket(family, socket.SOCK_STREAM)
    if sys.platform[:3] != "win":
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(backlog)
    return sock


# monkey-patches. TODO: better solution

gevent.Greenlet.wait = gevent.Greenlet.get
gevent.pool.Pool.waitall = gevent.pool.Pool.join
gevent.pool.Pool.free = gevent.pool.Pool.free_count

sleep = gevent.sleep
