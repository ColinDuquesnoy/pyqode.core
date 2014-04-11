"""
This module contains the client API.
"""
import sys


class NotConnectedError(Exception):
    """
    Raised if the client is not connected to the server when an operation is
    requested.
    """
    def __init__(self):
        super(NotConnectedError, self).__init__(
            'Client socket not connected or server not started')


def start_server(editor, script, interpreter=sys.executable, args=None):
    """
    Starts a pyqode server, specific to a editor instance.

    The server is a python script that starts a
    :class:`pyqode.core.server.JsonServer`. You (the user) must write
    the server script so that you can apply your own configuration
    server side.

    The script can be run with a custom interpreter. The default is to use
    sys.executable.

    :param: editor: editor instance
    :param str script: Path to the server main script.
    :param str interpreter: The python interpreter to use to run the server
        script. If None, sys.executable is used unless we are in a frozen
        application (cx_Freeze). The executable is not used if the
        executable scripts ends with '.exe' on Windows
    :param list args: list of additional command line args to use to start
        the server process.
    """
    editor._client.start(script, interpreter=interpreter, args=args)


def stop_server(editor):
    """
    Stops the server process for a specific editor and closes the
    associated client socket.

    You have to explicitly call this method when you're done with the editor
    widget, just before calling del on the widget.

    :param: editor: editor instance
    """
    try:
        if editor._client:
            editor._client.close()
    except RuntimeError:
        pass


def request_work(editor, worker_class_or_function, args, on_receive=None):
    """
    Requests some work on the server process of a specific editor instance.

    :param: editor: editor instance
    :param worker_class_or_function: Worker class or function
    :param args: worker args, any Json serializable objects
    :param on_receive: an optional callback executed when we receive the
        worker's results. The callback will be called with two arguments:
        the status (bool) and the results (object)

    :raise: NotConnectedError if the server cannot be reached.

    """
    editor._client.request_work(worker_class_or_function, args,
                                on_receive=on_receive)


def connected_to_server(editor):
    """
    Cheks if the client socket is connected to a server
    """
    return editor._client.is_connected