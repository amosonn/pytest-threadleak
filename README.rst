=================
pytest-threadleak
=================

.. image:: https://travis-ci.org/nirs/pytest-threadleak.svg?branch=master
    :target: https://travis-ci.org/nirs/pytest-threadleak
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/nirs/pytest-threadleak?branch=master
    :target: https://ci.appveyor.com/project/nirs/pytest-threadleak/branch/master
    :alt: See Build Status on AppVeyor

Detects tests leaking threads
=============================

Installation
------------

You can install "pytest-threadleak" via `pip`_ from `PyPI`_::

    $ pip install pytest-threadleak


Usage
-----

The threadleak pytest plugin will fail leaking threads. This can be an issue in
the test, or in the tested code.

Here is an example leaking test::

    $ cat leak_test.py
    import threading
    import time

    def test_leak():
        threading.Thread(target=time.sleep, args=(1,)).start()

Here is an example run with thread leak plugin enabled::

    $ pytest --threadleak leak_test.py
    ...
    leak_test.py::test_leak FAILED
    ...
    >   ???
    E   Failed: Test leaked [<Thread(Thread-1, started 139762716391168)>]

If you want to enable thread leak by default, you can enable it in your
pytest.ini or tox.ini::

    [pytest]
    threadleak = True


Contributing
------------

Running the tests::

    $ tox


License
-------

Distributed under the terms of the `MIT`_ license, "pytest-threadleak" is free
and open source software


Credits
-------

This `Pytest`_ plugin was generated with `Cookiecutter`_ along with
`@hackebrot`_'s `Cookiecutter-pytest-plugin`_ template.


.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
