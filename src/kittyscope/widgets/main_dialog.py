from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QHeaderView,
    QLabel,
    QProgressBar,
    QMenuBar,
    QMenu,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from kittyscope.models.finder import Finder
from kittyscope.models.analyzer import Analyzer
from kittyscope.models.research_router import ResearchRouter
from kittyscope.utils.static_texts import ABOUT
from kittyscope.widgets.table import TableResults
from kittyscope.widgets.q_lines import PathLine, SearchInput
from kittyscope.widgets.chart_builder import BarChartBuilder
import os


class Dialog(QDialog):
    """
    A dialog window for displaying file information and performing actions.

    Attributes:
        _menu_bar (QMenuBar): The menu bar for the dialog.
        _search_box (QGroupBox): The search box for selecting a folder.
        _table_box (QGroupBox): The table box for displaying file information.
        _actions_box (QGroupBox): The actions box for performing actions.
        _table (TableResults): The table for displaying file information.
        _path_line (PathLine): The path line for displaying the selected folder.
    """

    def __init__(self):
        """
        Initializes the dialog window.
        """
        super().__init__()

        self._analyzer = Analyzer()
        self.chart_builder: BarChartBuilder | None = None
        self.create_menu()
        self.create_search_box()
        self.create_table_box()
        self.create_stat_box()

        self._progress_bar = QProgressBar()
        self._progress_bar.setHidden(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._menu_bar)
        main_layout.addWidget(self._search_box)
        main_layout.addWidget(self._progress_bar)
        main_layout.addWidget(self._table_box)
        main_layout.addWidget(self._stat_box)

        self._table_box.setHidden(True)
        self._stat_box.setHidden(True)

        self.setLayout(main_layout)
        self.resize(800, 900)

    def create_menu(self):
        """
        Creates the menu bar for the dialog.
        """
        self._menu_bar = QMenuBar()

        self._program_menu = QMenu("&Program", self)
        self._about_action = self._program_menu.addAction("&About")
        self._menu_bar.addMenu(self._program_menu)

        self._about_action.triggered.connect(self.show_about)

    def create_search_box(self):
        """
        Creates the search box for selecting a folder.
        """
        self._search_box = QGroupBox("Main pannel")
        layout = QHBoxLayout()

        choose_path_button = QPushButton("Choose path")
        choose_path_button.setAutoDefault(False)
        choose_path_button.clicked.connect(self.open_search_folder_dialog)

        layout.addWidget(choose_path_button)

        self._search_box.setLayout(layout)

    def create_table_box(self):
        """
        Creates the table box for displaying file information.
        """
        self._table_box = QGroupBox("Results")
        layout = QVBoxLayout()

        self._table = TableResults()
        self._table.cellDoubleClicked.connect(self.display_file_info)
        header = self._table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self._path_line = PathLine()

        search_input_layout = QHBoxLayout()
        self.search_input_label = QLabel("Search: ")

        self._search_input = SearchInput()
        self._search_input.textChanged.connect(self._table.search)
        self._search_input.returnPressed.connect(self.step_through_results)

        search_input_layout.addWidget(self.search_input_label)
        search_input_layout.addWidget(self._search_input)

        self._csv_download_button = QPushButton("Download CSV")
        self._csv_download_button.clicked.connect(self.open_csv_folder_dialog)
        self._csv_download_button.setAutoDefault(False)

        layout.addLayout(search_input_layout)
        layout.addWidget(self._table)
        layout.addWidget(self._path_line)
        layout.addWidget(self._csv_download_button)

        self._table_box.setLayout(layout)
        self.__set_style_classes()

    def create_stat_box(self):
        """
        Creates the box for displaying statistics.

        Attributes:
            _stat_box (QGroupBox): The box for displaying statistics.
        """
        self._stat_box = QGroupBox("Stats")

    def display_stat(self, stat_data: dict):
        """
        Displays statistics in a chart format.

        Args:
            stat_data (dict): A dictionary containing the statistics data.
        """
        layout = QVBoxLayout()

        if not self.chart_builder:
            self.chart_builder = BarChartBuilder()
            self.chart = self.chart_builder.build(stat_data)
            layout.addWidget(self.chart)
        else:
            self.chart_builder.update(stat_data)

        self._stat_box.setLayout(layout)

    def show_error(self, title: str, message: str):
        """
        Shows an error message.

        Args:
            title (str): The title of the error message.
            message (str): The error message.
        """
        error_modal = QMessageBox()
        error_modal.setFixedSize(400, 200)
        error_modal.setWindowTitle("KittyScope")
        error_modal.setInformativeText(message)
        error_modal.setText(title)

        error_modal.setIcon(QMessageBox.Critical)
        error_modal.exec()

    def show_about(self):
        """
        Shows info about program.
        """
        about_modal = QMessageBox()
        about_modal.setFixedSize(400, 200)
        about_modal.setWindowTitle("KittyScope")
        about_modal.setInformativeText(ABOUT)
        about_modal.setText("About KittyScope")

        icon = QPixmap(
            "/Users/a-/Documents/Study/Магистратура/ПАНДАН/6_MODULE/технологии_программирования/kittyscope/src/kittyscope/assets/icons/cute-cat-deborkader.gif"
        ).scaled(64, 64, Qt.KeepAspectRatio)
        about_modal.setIconPixmap(icon)
        about_modal.exec()

    def show_csv_saved(self):
        """
        Shows a message box with the text "CSV file saved" when the user downloads a CSV file.

        This function is called by the CSV download button in the main dialog window.
        """
        csv_saved_modal = QMessageBox()
        csv_saved_modal.setFixedSize(400, 200)
        csv_saved_modal.setWindowTitle("KittyScope")
        csv_saved_modal.setInformativeText("CSV file saved")
        csv_saved_modal.setText("CSV file saved")
        csv_saved_modal.setIcon(QMessageBox.Information)
        csv_saved_modal.exec()

    def open_csv_folder_dialog(self):
        """
        Opens a dialog for selecting a folder to save the CSV file.
        """
        folder_path = QFileDialog.getExistingDirectory(self, "Choose Directory")
        if folder_path:
            file_name = "kittyscope_results.csv"
            folder_path = os.path.join(folder_path, file_name)
            self._finder.save_to_csv(folder_path)
            self.show_csv_saved()

    def open_search_folder_dialog(self):
        """
        Opens a dialog for selecting a folder to search.
        """
        folder_path = QFileDialog.getExistingDirectory(self, "Choose Directory")
        if folder_path:
            try:
                self.__hide_ui(True)
                self._finder = Finder(folder_path)
                table_data = self._finder.get_results()
                self.display_results(table_data)

                stat_data = self._analyzer.get_file_type_stat(
                    self._finder.results_table
                )
                self.display_stat(stat_data)

                self.__hide_ui(False)
            except Exception as e:
                self.show_error(title="Invalid path", message=e.__str__())
            self._path_line.setText(folder_path)

    def display_file_info(self, row, column):
        """
        Displays the file information for the selected file.

        Args:
            row (int): The row of the selected file.
            column (int): The column of the selected file.
        """
        file_name = self._table.item(row, column).text()
        file_path = os.path.join(self._path_line.text(), file_name)

        research_router = ResearchRouter()
        try:
            tag, file_info = research_router.get_file_info(file_path)
            file_info_dialog = QDialog()
            file_info_dialog.setWindowTitle("KittyScope")
            main_layout = QVBoxLayout()

            match tag:
                case "pdf":
                    self.__display_pdf_info(file_info, main_layout)
                case "image":
                    self.__display_image_info(file_info, main_layout)
                case "video":
                    self.__display_video_info(file_info, main_layout)
                case "audio":
                    self.__display_audio_info(file_info, main_layout)
                case _:
                    ...

            file_info_dialog.setLayout(main_layout)
            file_info_dialog.exec()
        except Exception:
            self.show_error(title="Invalid path", message="Unsupported file type")

    def __display_pdf_info(self, file_info, main_layout):
        """
        Displays the PDF file information.

        Args:
            file_info (dict): The PDF file information.
            layout (QVBoxLayout): The layout to add the widgets to.
        """
        layout = QVBoxLayout()
        common_info_box = QGroupBox("Common info")
        author: str = file_info["author"] if file_info["author"] else "-"
        title = file_info.get("title", "-")
        pages_count = file_info.get("pages_count", "-")
        subject = file_info.get("subject", "-")
        creator = file_info.get("creator", "-")
        producer = file_info.get("producer", "-")

        layout.addWidget(QLabel("<b>Author:</b> " + author))
        layout.addWidget(QLabel("<b>Title:</b> " + title))
        layout.addWidget(QLabel("<b>Pages count:</b> " + str(pages_count)))
        layout.addWidget(QLabel("<b>Subject:</b> " + subject))
        layout.addWidget(QLabel("<b>Creator:</b> " + creator))
        layout.addWidget(QLabel("<b>Producer:</b> " + producer))
        common_info_box.setLayout(layout)
        main_layout.addWidget(common_info_box)

    def __display_image_info(self, file_info, main_layout):
        """
        Displays the image file information.

        Args:
            file_info (dict): The image file information.
            layout (QVBoxLayout): The layout to add the widgets to.
        """
        layout = QVBoxLayout()
        common_info_box = QGroupBox("Common info")

        width = file_info["common_info"]["width"]
        height = file_info["common_info"]["height"]
        format_ = file_info["common_info"]["format"]
        color_mode = file_info["common_info"]["color_mode"]

        layout.addWidget(QLabel("<b>Width:</b> " + width))
        layout.addWidget(QLabel("<b>Height:</b> " + height))
        layout.addWidget(QLabel("<b>Format:</b> " + format_))
        layout.addWidget(QLabel("<b>Color mode:</b> " + color_mode))

        common_info_box.setLayout(layout)
        main_layout.addWidget(common_info_box)

        if file_info["exif_info"]:
            exif_info_box = QGroupBox("Exif info")
            layout = QVBoxLayout()
            for key, value in file_info["exif_info"].items():
                layout.addWidget(QLabel("<b>" + key + "</b>: " + str(value)))
            exif_info_box.setLayout(layout)
            main_layout.addWidget(exif_info_box)

    def __display_video_info(self, file_info, main_layout):
        """
        Displays the video file information.

        Args:
            file_info (dict): The video file information.
            layout (QVBoxLayout): The layout to add the widgets to.
        """
        layout = QVBoxLayout()
        common_info_box = QGroupBox("Common info")

        bit_rate = file_info["bit_rate"]
        duration = file_info["duration"]
        file_name = file_info["filename"]
        format_long_name = file_info["format_long_name"]
        format_name = file_info["format_name"]
        nb_programs = file_info["nb_programs"]
        nb_streams = file_info["nb_streams"]
        size = file_info["size"]
        probe_score = file_info["probe_score"]

        layout.addWidget(QLabel("<b>Bit rate:</b> " + bit_rate))
        layout.addWidget(QLabel("<b>Duration:</b> " + duration))
        layout.addWidget(QLabel("<b>File name:</b> " + file_name))
        layout.addWidget(QLabel("<b>Format long name:</b> " + format_long_name))
        layout.addWidget(QLabel("<b>Format name:</b> " + format_name))
        layout.addWidget(QLabel("<b>Nb programs:</b> " + str(nb_programs)))
        layout.addWidget(QLabel("<b>Nb streams:</b> " + str(nb_streams)))
        layout.addWidget(QLabel("<b>Size:</b> " + size))
        layout.addWidget(QLabel("<b>Probe score:</b> " + str(probe_score)))

        common_info_box.setLayout(layout)
        main_layout.addWidget(common_info_box)

        if file_info["tags"]:
            exif_info_box = QGroupBox("Tags info")
            layout = QVBoxLayout()
            for key, value in file_info["tags"].items():
                layout.addWidget(QLabel("<b>" + key + "</b>: " + str(value)))
            exif_info_box.setLayout(layout)
            main_layout.addWidget(exif_info_box)

    def __display_audio_info(self, file_info, main_layout):
        """
        Displays the audio file information.

        Args:
            file_info (dict): The audio file information.
            layout (QVBoxLayout): The layout to add the widgets to.
        """
        self.__display_video_info(file_info, main_layout)

    def step_through_results(self):
        """
        Steps through the search results.

        Increments the search step counter and attempts to display the next result.
        If there are no more results, resets the counter and displays the first result.
        """
        self._search_input.add_search_step()
        step = self._search_input._search_steps
        try:
            self._table.step_through_results(step)
        except IndexError:
            self._table.step_through_results(0)
            self._search_input.drop_steps()

    def display_results(self, table_data: dict[str, list]):
        """
        Displays the file information for the given folder.

        Hides the table and progress bar, displays the progress bar, displays the table data, hides the progress bar, and displays the table again.

        Args:
            table_data (dict[str, list]): A dictionary of file and folder information.
        """
        self._progress_bar.setHidden(False)
        self._table.setHidden(True)
        self._table.display_results(table_data, self._progress_bar)
        self._progress_bar.setHidden(True)
        self._table.setHidden(False)

    def __hide_ui(self, flag: bool):
        """
        Hides or shows the main UI elements.

        Args:
            flag (bool): If True, hides the elements. Otherwise, shows them.
        """
        self._search_box.setHidden(flag)
        self._table_box.setHidden(flag)
        self._stat_box.setHidden(flag)

    def __set_style_classes(self):
        """
        Sets the style class for the main UI elements.

        This method is called to set the style class for the main UI elements when the dialog is initialized.
        """
        self._search_box.setProperty("class", "main_style")
        self._table_box.setProperty("class", "main_style")
        self.setProperty("class", "main_style")
