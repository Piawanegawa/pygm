#!/usr/bin/env python3

"""
Plothook generator tab.

This module provides the PySide6 widget used to generate and insert plothooks.
"""

from collections.abc import Callable

from PySide6.QtCore import QObject, QRect, QSize, Qt, QThread, Signal, Slot
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListView,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from pygm.app.gui.plothook_tools import (
    append_plothook_to_markdown,
    build_plothook_prompt,
    parse_plothooks,
)
from pygm.utils.ai.ai_client import AIClient


class PlothookWorker(QObject):
    """
    Worker for generating plothooks in the background.
    """

    success = Signal(list)
    failure = Signal(str)
    finished = Signal()

    def __init__(
        self,
        ai_client_factory: Callable[[], AIClient],
        restriction: str,
        count: int,
    ) -> None:
        """
        Initialize the worker.
        :param ai_client_factory: Factory for creating AI clients.
        :param restriction: The plothook restriction.
        :param count: The number of plothooks to generate.
        """
        super().__init__()
        self._ai_client_factory: Callable[[], AIClient] = ai_client_factory
        self._restriction: str = restriction
        self._count: int = count

    @Slot()
    def run(self) -> None:
        """
        Generate plothooks and emit the result.
        :return: None.
        """
        try:
            ai_client = self._ai_client_factory()
            response = ai_client.send_prompt(build_plothook_prompt(self._restriction, self._count))
            if response.get_error():
                self.failure.emit(response.get_error())
            else:
                self._emit_plothooks(response.get_content())
        except Exception as error:
            self.failure.emit(str(error))
        self.finished.emit()

    def _emit_plothooks(self, response_content: str) -> None:
        """
        Parse and emit generated plothooks.
        :param response_content: The raw AI response content.
        :return: None.
        """
        plothooks = parse_plothooks(response_content)
        if plothooks:
            self.success.emit(plothooks)
        else:
            self.failure.emit("The AI response did not contain any plothooks.")


class PlothookGeneratorTab(QWidget):
    """
    Tab widget for generating and inserting plothooks.
    """

    def __init__(
        self,
        markdown_editor: QPlainTextEdit,
        ai_client_factory: Callable[[], AIClient],
    ) -> None:
        """
        Initialize the plothook generator tab.
        :param markdown_editor: The Markdown editor receiving selected plothooks.
        :param ai_client_factory: Factory for creating AI clients.
        """
        super().__init__()
        self._markdown_editor: QPlainTextEdit = markdown_editor
        self._ai_client_factory: Callable[[], AIClient] = ai_client_factory
        self._thread: QThread | None = None
        self._worker: PlothookWorker | None = None
        self._restriction_input: QTextEdit
        self._count_combo: QComboBox
        self._generate_button: QPushButton
        self._result_list: QListWidget
        self._use_button: QPushButton
        self._status_label: QLabel
        self._setup_ui()

    def _setup_ui(self) -> None:
        """
        Create and wire the tab widgets.
        :return: None.
        """
        layout = QVBoxLayout(self)
        self._restriction_input = QTextEdit()
        self._restriction_input.setPlaceholderText("Plothook eingrenzen...")
        self._restriction_input.setFixedHeight(96)

        controls_layout = QHBoxLayout()
        self._generate_button = QPushButton("Generate")
        self._generate_button.clicked.connect(self._on_generate_clicked)
        self._count_combo = QComboBox()
        for count in range(1, 6):
            self._count_combo.addItem(str(count), count)
        controls_layout.addWidget(self._generate_button, 1)
        controls_layout.addWidget(self._count_combo)

        self._result_list = QListWidget()
        self._result_list.setWordWrap(True)
        self._result_list.setUniformItemSizes(False)
        self._result_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._result_list.setResizeMode(QListView.ResizeMode.Adjust)
        self._result_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._result_list.setSpacing(6)
        self._result_list.itemSelectionChanged.connect(self._on_selection_changed)
        self._use_button = QPushButton("Use")
        self._use_button.setEnabled(False)
        self._use_button.clicked.connect(self._on_use_clicked)
        self._status_label = QLabel("")

        layout.addWidget(QLabel("Eingrenzung"))
        layout.addWidget(self._restriction_input)
        layout.addLayout(controls_layout)
        layout.addWidget(self._result_list, 1)
        layout.addWidget(self._use_button)
        layout.addWidget(self._status_label)

    @Slot()
    def _on_generate_clicked(self) -> None:
        """
        Start generating plothooks.
        :return: None.
        """
        restriction = self._restriction_input.toPlainText()
        count = int(self._count_combo.currentData())
        self._set_generating_state()
        self._thread = QThread(self)
        self._worker = PlothookWorker(self._ai_client_factory, restriction, count)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.success.connect(self._on_generation_success)
        self._worker.failure.connect(self._on_generation_failure)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.finished.connect(self._clear_worker_refs)
        self._thread.start()

    @Slot(list)
    def _on_generation_success(self, plothooks: list[str]) -> None:
        """
        Populate the result list after successful generation.
        :param plothooks: The generated plothooks.
        :return: None.
        """
        self._result_list.clear()
        for plothook in plothooks:
            self._add_plothook_item(plothook)
        self._status_label.setText("")
        self._generate_button.setEnabled(True)

    def _add_plothook_item(self, plothook: str) -> None:
        """
        Add a wrapped plothook item to the result list.
        :param plothook: The plothook text.
        :return: None.
        """
        item = QListWidgetItem(plothook)
        item.setToolTip(plothook)
        item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self._result_list.addItem(item)
        self._update_item_size(item)

    def _update_item_size(self, item: QListWidgetItem) -> None:
        """
        Update the list item height for wrapped text.
        :param item: The list item.
        :return: None.
        """
        item_width = max(self._result_list.viewport().width() - 20, 80)
        text_bounds = self._result_list.fontMetrics().boundingRect(
            QRect(0, 0, item_width, 10_000),
            Qt.TextFlag.TextWordWrap,
            item.text(),
        )
        item_height = max(text_bounds.height() + 16, 32)
        item.setSizeHint(QSize(item_width, item_height))

    def resizeEvent(self, event) -> None:
        """
        Update wrapped list item heights after resizing.
        :param event: The resize event.
        :return: None.
        """
        super().resizeEvent(event)
        self._refresh_item_sizes()

    def _refresh_item_sizes(self) -> None:
        """
        Refresh all wrapped list item heights.
        :return: None.
        """
        for index in range(self._result_list.count()):
            item = self._result_list.item(index)
            self._update_item_size(item)

    @Slot(str)
    def _on_generation_failure(self, error_message: str) -> None:
        """
        Show a generation error.
        :param error_message: The error message.
        :return: None.
        """
        self._status_label.setText("Generation failed.")
        self._generate_button.setEnabled(True)
        QMessageBox.warning(self, "Plothook generation failed", error_message)

    @Slot()
    def _clear_worker_refs(self) -> None:
        """
        Clear thread and worker references after shutdown.
        :return: None.
        """
        self._thread = None
        self._worker = None

    @Slot()
    def _on_selection_changed(self) -> None:
        """
        Update the Use button state.
        :return: None.
        """
        self._use_button.setEnabled(bool(self._result_list.selectedItems()))

    @Slot()
    def _on_use_clicked(self) -> None:
        """
        Insert the selected plothook into the Markdown editor.
        :return: None.
        """
        selected_items = self._result_list.selectedItems()
        if selected_items:
            updated_markdown = append_plothook_to_markdown(
                self._markdown_editor.toPlainText(),
                selected_items[0].text(),
            )
            self._markdown_editor.setPlainText(updated_markdown)

    def _set_generating_state(self) -> None:
        """
        Set the UI state for an active generation.
        :return: None.
        """
        self._generate_button.setEnabled(False)
        self._use_button.setEnabled(False)
        self._result_list.clear()
        self._status_label.setText("Generating...")
