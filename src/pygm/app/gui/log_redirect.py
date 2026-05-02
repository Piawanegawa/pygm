#!/usr/bin/env python3

"""
GUI log redirection helpers.

This module redirects console streams and unhandled exceptions to the GUI log.
"""

import sys
import traceback
from types import TracebackType

from PySide6.QtCore import QObject, Signal


class LogEmitter(QObject):
    """
    Signal bridge for writing log text from arbitrary code paths.
    """

    text_written = Signal(str)
    exception_written = Signal(str)


class LogStream:
    """
    File-like stream that forwards writes to a LogEmitter.
    """

    def __init__(self, emitter: LogEmitter, fallback_stream) -> None:
        """
        Initialize the log stream.
        :param emitter: The log emitter to receive text.
        :param fallback_stream: The original stream used as fallback.
        """
        self._emitter: LogEmitter = emitter
        self._fallback_stream = fallback_stream

    def write(self, text: str) -> int:
        """
        Write text to the log emitter.
        :param text: The text to write.
        :return: The written text length.
        """
        self._emitter.text_written.emit(text)
        if self._fallback_stream is not None:
            self._fallback_stream.write(text)
        return len(text)

    def flush(self) -> None:
        """
        Flush the fallback stream.
        :return: None.
        """
        if self._fallback_stream is not None:
            self._fallback_stream.flush()

    def isatty(self) -> bool:
        """
        Return whether this stream is an interactive TTY.
        :return: False.
        """
        return False


def install_gui_log_handlers(emitter: LogEmitter) -> None:
    """
    Install stdout, stderr, and exception redirection.
    :param emitter: The log emitter to receive text and exceptions.
    :return: None.
    """
    sys.stdout = LogStream(emitter, sys.__stdout__)
    sys.stderr = LogStream(emitter, sys.__stderr__)
    sys.excepthook = _create_exception_hook(emitter)


def _create_exception_hook(emitter: LogEmitter):
    """
    Create an exception hook that logs tracebacks without closing the app.
    :param emitter: The log emitter to receive exceptions.
    :return: The exception hook function.
    """

    def exception_hook(
        exception_type: type[BaseException],
        exception: BaseException,
        trace: TracebackType | None,
    ) -> None:
        formatted_exception = "".join(
            traceback.format_exception(exception_type, exception, trace)
        )
        emitter.exception_written.emit(formatted_exception)

    return exception_hook
