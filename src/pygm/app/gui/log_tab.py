#!/usr/bin/env python3

"""
Log tab widget.

This module provides a sidebar tab for application logs and clipboard copying.
"""

from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class LogTab(QWidget):
    """
    Widget for displaying application logs.
    """

    def __init__(self) -> None:
        """
        Initialize the log tab.
        """
        super().__init__()
        self._log_text: QTextEdit
        self._copy_button: QPushButton
        self._setup_ui()

    def append_text(self, text: str) -> None:
        """
        Append text to the log output.
        :param text: The text to append.
        :return: None.
        """
        if text:
            cursor = self._log_text.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            cursor.insertText(text)
            self._log_text.setTextCursor(cursor)
            self._log_text.ensureCursorVisible()

    def get_text(self) -> str:
        """
        Get the current log text.
        :return: The current log text.
        """
        return self._log_text.toPlainText()

    def _setup_ui(self) -> None:
        """
        Create and wire the tab widgets.
        :return: None.
        """
        layout = QVBoxLayout(self)
        self._log_text = QTextEdit()
        self._log_text.setReadOnly(True)
        self._log_text.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

        self._copy_button = QPushButton("Copy")
        self._copy_button.clicked.connect(self._copy_log_to_clipboard)

        layout.addWidget(self._log_text, 1)
        layout.addWidget(self._copy_button)

    def _copy_log_to_clipboard(self) -> None:
        """
        Copy the current log text to the clipboard.
        :return: None.
        """
        QApplication.clipboard().setText(self.get_text())
