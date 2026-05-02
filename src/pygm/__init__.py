#!/usr/bin/env python3

"""
pygm - Gamemaster Toolbox.

This package provides tools for tabletop RPG game masters, including
AI-powered generation of plot hooks, NPC descriptions, scene descriptions,
random encounters, secrets, puzzles, loot, and battlemaps.
"""

import sys

from PySide6.QtWidgets import QApplication

from pygm.app.gui.log_redirect import LogEmitter, install_gui_log_handlers
from pygm.app.gui.main_window import MainWindow
from pygm.utils.ai.ai_client_factory import create_openrouter_ai_client


def main() -> None:
    """
    Run the pygm desktop GUI.
    :return: None.
    """
    app = QApplication(sys.argv)
    log_emitter = LogEmitter()
    window = MainWindow(create_openrouter_ai_client)
    log_emitter.text_written.connect(window.append_log_text)
    log_emitter.exception_written.connect(window.append_exception_text)
    install_gui_log_handlers(log_emitter)
    window.show()
    sys.exit(app.exec())
