import sys

from PySide6.QtWidgets import QApplication

from kittyscope.widgets.main_dialog import Dialog


class App:
    """
    The main application class.

    This class is responsible for initializing and running the application.
    """

    def __init__(self):
        """
        Initializes the application.

        Creates a new instance of the Dialog class, which is the main window of the application.
        """
        self.main_window: Dialog

    def run(self):
        """
        Runs the application.

        Creates a new instance of the QApplication class, sets the stylesheet, and shows the main dialog.
        """
        qt_app = QApplication(sys.argv)
        with open(
            "/Users/a-/Documents/Study/Магистратура/ПАНДАН/6_MODULE/технологии_программирования/kittyscope/src/kittyscope/assets/styles/styles.qss",
            "r",
        ) as f:
            stylesheet = f.read()
        qt_app.setStyleSheet(stylesheet)

        dialog = Dialog()

        dialog.show()

        sys.exit(qt_app.exec())
