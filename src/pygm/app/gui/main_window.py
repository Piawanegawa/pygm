#!/usr/bin/env python3

"""
Main PySide6 window.

This module provides the main pygm desktop window.
"""

from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QSplitter,
    QTabWidget,
)

from pygm.app.gui.document_store import (
    MARKDOWN_FILE_FILTER,
    get_active_markdown_file,
    read_markdown_file,
    set_active_markdown_file,
    write_markdown_file,
)
from pygm.app.gui.log_tab import LogTab
from pygm.app.gui.plothook_generator_tab import PlothookGeneratorTab
from pygm.utils.ai.ai_client import AIClient


class MainWindow(QMainWindow):
    """
    Main window for the pygm GUI.
    """

    def __init__(self, ai_client_factory: Callable[[], AIClient]) -> None:
        """
        Initialize the main window.
        :param ai_client_factory: Factory for creating AI clients.
        """
        super().__init__()
        self._ai_client_factory: Callable[[], AIClient] = ai_client_factory
        self._markdown_editor: QPlainTextEdit
        self._generator_tabs: QTabWidget
        self._log_tab: LogTab
        self._active_markdown_file: Path | None = None
        self._setup_ui()
        self._setup_shortcuts()
        self._load_persisted_markdown_file()

    def append_log_text(self, text: str) -> None:
        """
        Append text to the Log tab.
        :param text: The text to append.
        :return: None.
        """
        self._log_tab.append_text(text)

    def append_exception_text(self, text: str) -> None:
        """
        Append exception text and activate the Log tab.
        :param text: The exception text to append.
        :return: None.
        """
        self._log_tab.append_text(text)
        self._generator_tabs.setCurrentWidget(self._log_tab)

    def save_markdown(self) -> None:
        """
        Save the Markdown document.
        :return: None.
        """
        try:
            self._save_markdown()
        except Exception as error:
            self._show_file_error("Could not save Markdown file.", error)

    def _save_markdown(self) -> None:
        """
        Save the Markdown document.
        :return: None.
        """
        target_file = self._active_markdown_file
        if target_file is None:
            selected_file = self._select_markdown_save_file()
            if selected_file is None:
                return
            target_file = selected_file.resolve()
        write_markdown_file(target_file, self._markdown_editor.toPlainText())
        self._set_active_markdown_file(target_file)

    def load_markdown(self) -> None:
        """
        Load a Markdown document through a file chooser.
        :return: None.
        """
        selected_file = self._select_markdown_open_file()
        if selected_file is not None:
            self._load_markdown_file(selected_file)

    def _setup_ui(self) -> None:
        """
        Create the main UI.
        :return: None.
        """
        self.setWindowTitle("pygm")
        self.resize(1200, 800)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self._markdown_editor = QPlainTextEdit()
        self._markdown_editor.setPlaceholderText("Markdown schreiben...")

        self._generator_tabs = QTabWidget()
        self._generator_tabs.addTab(
            PlothookGeneratorTab(self._markdown_editor, self._ai_client_factory),
            "PlothookGenerator",
        )
        self._log_tab = LogTab()
        self._generator_tabs.addTab(self._log_tab, "Log")

        splitter.addWidget(self._markdown_editor)
        splitter.addWidget(self._generator_tabs)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        self.setCentralWidget(splitter)

    def _setup_shortcuts(self) -> None:
        """
        Create keyboard shortcuts.
        :return: None.
        """
        save_shortcut = QShortcut(QKeySequence.StandardKey.Save, self)
        save_shortcut.activated.connect(self.save_markdown)

        load_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        load_shortcut.activated.connect(self.load_markdown)

    def _load_persisted_markdown_file(self) -> None:
        """
        Load the persisted Markdown file on startup.
        :return: None.
        """
        active_file = get_active_markdown_file()
        if active_file is not None and active_file.exists():
            self._load_markdown_file(active_file)
        elif active_file is not None:
            self._set_active_markdown_file(active_file)

    def _load_markdown_file(self, file_path: Path) -> None:
        """
        Load a Markdown file into the editor.
        :param file_path: The Markdown file path.
        :return: None.
        """
        try:
            self._markdown_editor.setPlainText(read_markdown_file(file_path))
            self._set_active_markdown_file(file_path)
        except Exception as error:
            self._show_file_error("Could not load Markdown file.", error)

    def _set_active_markdown_file(self, file_path: Path) -> None:
        """
        Set and persist the active Markdown file.
        :param file_path: The active Markdown file path.
        :return: None.
        """
        self._active_markdown_file = file_path.resolve()
        set_active_markdown_file(self._active_markdown_file)
        self._update_window_title()

    def _update_window_title(self) -> None:
        """
        Update the window title with the active file path.
        :return: None.
        """
        if self._active_markdown_file is None:
            self.setWindowTitle("pygm")
        else:
            self.setWindowTitle(f"pygm - {self._active_markdown_file}")

    def _select_markdown_save_file(self) -> Path | None:
        """
        Select a Markdown file for saving.
        :return: The selected file path or None.
        """
        selected_file, _ = QFileDialog.getSaveFileName(
            self,
            "Save Markdown",
            "",
            MARKDOWN_FILE_FILTER,
        )
        return self._to_optional_path(selected_file)

    def _select_markdown_open_file(self) -> Path | None:
        """
        Select a Markdown file for loading.
        :return: The selected file path or None.
        """
        selected_file, _ = QFileDialog.getOpenFileName(
            self,
            "Load Markdown",
            "",
            MARKDOWN_FILE_FILTER,
        )
        return self._to_optional_path(selected_file)

    def _show_file_error(self, message: str, error: Exception) -> None:
        """
        Show and log a file operation error.
        :param message: The user-facing message.
        :param error: The raised exception.
        :return: None.
        """
        self.append_exception_text(f"{message}\n{error}\n")
        QMessageBox.warning(self, "Markdown file error", f"{message}\n\n{error}")

    @staticmethod
    def _to_optional_path(file_path: str) -> Path | None:
        """
        Convert a file chooser result to an optional Path.
        :param file_path: The selected file path string.
        :return: The selected path or None.
        """
        if not file_path:
            return None
        return Path(file_path)
