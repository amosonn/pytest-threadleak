import operator
import threading
import pytest
import sys

from threading import Thread

class ErrorCollectingThread(Thread):

    def start(self):
        inner_run = self.run
        def _run():
            try:
                inner_run()
            except:
                collect_exc(sys.exc_info())
                raise
        self.run = _run
        super().start()
        self.run = inner_run

threading.Thread = ErrorCollectingThread

def pytest_addoption(parser):
    group = parser.getgroup('threadleak')
    group.addoption(
        '--threadleak',
        action='store_true',
        dest='threadleak',
        default=False,
        help='Detect tests leaking threads')
    group.addoption(
        '--threadexception',
        action='store_true',
        dest='threadexception',
        default=False,
        help='Detect tests in which threads had raised exceptions')
    parser.addini(
        'threadleak',
        'Detect thread leak (default: False)',
        type="bool",
        default=False)
    parser.addini(
        'threadexception',
        'Detect thread exceptions (default: False)',
        type="bool",
        default=False)

exc_infos = set()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    global exc_infos
    exc_infos = set()
    start_threads = None
    if is_enabled(item):
        start_threads = current_threads()
    yield
    if start_threads:
        leaked_threads = current_threads() - start_threads
        if leaked_threads:
            pytest.fail("Test leaked %s" % sorted_by_name(leaked_threads))
        if is_enabled_exceptions(item) and exc_infos:
            exc_info = exc_infos.pop()
            raise exc_info[1]

def collect_exc(exc_info):
    global exc_infos
    exc_infos.add(exc_info)

def is_enabled(item):
    return (item.config.getoption("threadleak") or
            item.config.getini("threadleak"))

def is_enabled_exceptions(item):
    return (item.config.getoption("threadexception") or
            item.config.getini("threadexception"))


def current_threads():
    return frozenset(threading.enumerate())


def sorted_by_name(threads):
    return sorted(threads, key=operator.attrgetter("name"))
