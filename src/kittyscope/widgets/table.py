from PySide6.QtWidgets import (
    QTableWidget,
    QAbstractItemView,
    QTableWidgetItem,
    QProgressBar,
    QApplication,
)
from PySide6.QtCore import Qt, QDateTime
import time


class TableResults(QTableWidget):
    """
    A table widget for displaying file information.

    Attributes:
        _finder (Finder): The Finder object used to retrieve file information.

    Methods:
        display_results(self, folder_path: str): Displays the file information for the given folder.
    """

    def __init__(self):
        super().__init__()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSortingEnabled(True)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(
            [
                "Name",
                "Type",
                "Size (bytes)",
                "Extension",
                "Last access",
                "Last modification",
            ]
        )
        self._search_items = []

    def display_results(
        self, table_data: dict[str, list], progress_bar: QProgressBar
    ) -> None:
        """
        Displays the file information for the given folder.

        Args:
            folder_path (str): The path to the folder containing the files.
        """
        self.setRowCount(0)
        table_params = list(table_data.keys())
        table_rows = len(table_data["name"])

        for i in range(table_rows):
            self.insertRow(i)

        progress_bar.setMaximum(table_rows * len(table_params))
        progress_bar_counter = 0
        for param, values in table_data.items():
            for i, value in enumerate(values):
                item = QTableWidgetItem()
                param_index = table_params.index(param)

                if isinstance(value, int) | isinstance(value, QDateTime):
                    item.setData(Qt.DisplayRole, value)
                else:
                    item.setText(value)

                if param_index != 0:
                    item.setFlags(
                        item.flags() & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable
                    )

                self.setItem(i, param_index, item)

                progress_bar_counter += 1
                progress_bar.setValue(progress_bar_counter)
                QApplication.processEvents()
                time.sleep(0.001)

        self.setColumnWidth(0, 150)

        for column in range(1, self.columnCount()):
            self.resizeColumnToContents(column)

    def search(self, text: str) -> None:
        """
        Searches the table for the given text and sets the current item to the first found item.

        Args:
            text (str): The text to search for.
        """
        self._search_items = self.findItems(text, Qt.MatchContains)
        if self._search_items:
            item = self._search_items[0]
            self.setCurrentItem(item)

    def step_through_results(self, step: int) -> None:
        """
        Steps through the search results and sets the current item to the item at the given step.

        Args:
            step (int): The step to move to in the search results.
        """
        if self._search_items:
            self.setCurrentItem(self._search_items[step])
