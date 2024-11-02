from PySide6.QtWidgets import QLineEdit


class PathLine(QLineEdit):
    """
    A read-only line edit for displaying the current path.

    Methods:
        __init__(self): Initializes the PathLine widget.
    """

    def __init__(self):
        """
        Initializes the PathLine widget.

        Sets the line edit to read-only mode.
        """
        super().__init__()
        self.setReadOnly(True)


class SearchInput(QLineEdit):
    def __init__(self):
        """
        Initializes the SearchInput widget.

        Sets the placeholder text to "search by name" and initializes the search steps counter to 0.
        """
        super().__init__()
        self.setPlaceholderText("search by name")

        self._search_steps: int = 0

    def add_search_step(self):
        """
        Increments the search steps counter.

        This method increments the search steps counter which is used to navigate through search results.
        """
        self._search_steps += 1

    def drop_steps(self):
        """
        Resets the search steps counter to 0.

        This method resets the search steps counter to 0 which is used to navigate through search results.
        """
        self._search_steps = 0
